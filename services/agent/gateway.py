import asyncio
import logging
import time

import libmav

from async_libmav import AsyncLibmavConnection
from mavlink_messages import odid, other
from settings import Settings

logger = logging.getLogger(__name__)

UNIX_TIMESTAMP_2019_01_01 = 1546300800


class DronetagGateway:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.message_set = libmav.MessageSet("mavlink/common.xml")

        fmu_heartbeat = self.message_set.create("HEARTBEAT").set_from_dict(
            {
                "type": self.message_set.enum("MAV_TYPE_ODID"),
                "autopilot": self.message_set.enum("MAV_AUTOPILOT_INVALID"),
                "base_mode": 0,
                "custom_mode": 0,
                "system_status": self.message_set.enum("MAV_STATE_UNINIT"),
            }
        )
        dri_heartbeat = self.message_set.create("HEARTBEAT").set_from_dict(
            {
                "type": self.message_set.enum("MAV_TYPE_ONBOARD_CONTROLLER"),
                "autopilot": self.message_set.enum("MAV_AUTOPILOT_INVALID"),
                "base_mode": 0,
                "custom_mode": 0,
                "system_status": self.message_set.enum("MAV_STATE_UNINIT"),
            }
        )

        self.fmu_conn = AsyncLibmavConnection(
            self.mavlink_tcp_client(),
            message_set=self.message_set,
            system_id=self.settings.fmu_system_id,
            component_id=self.settings.fmu_component_id,
            heartbeat=fmu_heartbeat,
        )
        self.dri_conn = AsyncLibmavConnection(
            self.mavlink_tcp_client(),
            message_set=self.message_set,
            system_id=self.settings.dri_system_id,
            component_id=self.settings.dri_component_id,
            heartbeat=dri_heartbeat,
        )

        self.fmu_system_time: other.SystemTime | None = None
        self.fmu_gps_raw_int: other.GpsRawInt | None = None
        self.fmu_global_position_int: other.GlobalPositionInt | None = None
        self.fmu_altitude: other.Altitude | None = None
        self.fmu_home_position: other.HomePosition | None = None
        self.fmu_odid_location: odid.Location | None = None
        self.dri_odid_arm_status: odid.ArmStatusMsg | None = None

    def mavlink_tcp_client(self) -> libmav.TCPClient:
        try:
            return libmav.TCPClient(str(self.settings.mavlink_endpoint_ip), self.settings.mavlink_endpoint_port)
        except RuntimeError as e:
            raise ConnectionError(f"Failed to create TCP client: {e}") from e

    async def forward_message(self, message: libmav.Message, conn: AsyncLibmavConnection):
        new_message = self.message_set.create(message.name).set_from_dict(message.to_dict())
        await conn.send(new_message)

    async def process_fmu_messages(self):
        async for message in self.fmu_conn:
            if not (message.header.system_id == 1 and message.header.component_id == 1):
                continue

            match message.name:
                case "SYSTEM_TIME":
                    self.fmu_system_time = other.SystemTime.from_mavlink(message)
                    await self.forward_message(message, self.dri_conn)
                case "GPS_RAW_INT":
                    self.fmu_gps_raw_int = other.GpsRawInt.from_mavlink(message)
                    await self.forward_message(message, self.dri_conn)
                case "GLOBAL_POSITION_INT":
                    self.fmu_global_position_int = other.GlobalPositionInt.from_mavlink(message)
                    await self.forward_message(message, self.dri_conn)
                case "ALTITUDE":
                    self.fmu_altitude = other.Altitude.from_mavlink(message)
                    await self.forward_message(message, self.dri_conn)
                case "HOME_POSITION":
                    self.fmu_home_position = other.HomePosition.from_mavlink(message)
                case "OPEN_DRONE_ID_LOCATION":
                    self.fmu_odid_location = odid.Location.from_mavlink(message)
                    await self.send_odid_location()
                case _:
                    continue

            logger.debug(f"FMU: {message.id:5d} {message.name}")

    async def process_dri_messages(self):
        async for message in self.dri_conn:
            if not (message.header.system_id == 2 and message.header.component_id == 236):
                continue

            logger.debug(f"DRI: {message.id:5d} {message.name}")

            if message.name == "OPEN_DRONE_ID_ARM_STATUS":
                await self.forward_message(message, self.fmu_conn)
                arm_status = odid.ArmStatusMsg.from_mavlink(message)
                if arm_status != self.dri_odid_arm_status:
                    # only log if the status has changed
                    self.dri_odid_arm_status = arm_status
                    if arm_status.status == odid.ArmStatus.MAV_ODID_ARM_STATUS_GOOD_TO_ARM:
                        logger.info("ARM_STATUS: OK")
                    else:
                        logger.warning(f"ARM_STATUS: {arm_status.error}")

    async def send_odid_basic_id(self):
        uas_id = self.settings.uas_id or ""
        id_type = odid.IDType.MAV_ODID_ID_TYPE_SERIAL_NUMBER if uas_id else odid.IDType.MAV_ODID_ID_TYPE_NONE

        message = self.message_set.create("OPEN_DRONE_ID_BASIC_ID").set_from_dict(
            {
                "id_type": id_type,
                "ua_type": self.settings.uas_type,
                "uas_id": list(uas_id.encode("ascii")),
            }
        )
        await self.dri_conn.send(message)

    async def send_odid_system(self):
        if self.fmu_home_position is None:
            return

        if self.fmu_system_time is None:
            now = time.time()
        else:
            now = self.fmu_system_time.time_unix_usec / 1e6

        message = self.message_set.create("OPEN_DRONE_ID_SYSTEM").set_from_dict(
            {
                "operator_location_type": odid.OperatorLocationType.MAV_ODID_OPERATOR_LOCATION_TYPE_TAKEOFF,
                "classification_type": odid.ClassificationType.MAV_ODID_CLASSIFICATION_TYPE_EU,
                "operator_latitude": self.fmu_home_position.latitude,
                "operator_longitude": self.fmu_home_position.longitude,
                "operator_altitude_geo": self.fmu_home_position.altitude / 1000,
                "area_count": 1,
                "area_radius": 0,
                "area_ceiling": -1000,
                "area_floor": -1000,
                "category_eu": odid.CategoryEU.MAV_ODID_CATEGORY_EU_OPEN,
                "class_eu": odid.ClassEU.MAV_ODID_CLASS_EU_CLASS_3,
                "timestamp": int(now - UNIX_TIMESTAMP_2019_01_01),
            }
        )
        await self.dri_conn.send(message)

    async def send_odid_operator_id(self):
        oprn = self.settings.oprn

        message = self.message_set.create("OPEN_DRONE_ID_OPERATOR_ID").set_from_dict(
            {
                "operator_id_type": self.message_set.enum("MAV_ODID_OPERATOR_ID_TYPE_CAA"),
                "operator_id": oprn.public_part if oprn else "",
            }
        )
        await self.dri_conn.send(message)

    async def send_odid_location(self, location: odid.Location | None = None):
        location = location or self.fmu_odid_location
        if location is None:
            return

        location = location.model_copy()

        # EN 4709-002:2023, 5.1 Data Directory, Track Direction:
        # > If the aircraft is not moving horizontally, use the “Unknown” value.
        # > Special values as invalid, no value, or unknown are coded with 361 deg.
        if location.speed_horizontal < self.settings.odid_course_speed_threshold:
            location.direction = 36100

        message = self.message_set.create("OPEN_DRONE_ID_LOCATION").set_from_dict(location.to_dict())
        await self.dri_conn.send(message)

    async def send_odid_messages(self, period: float = 0.5):
        while True:
            await asyncio.sleep(period)

            await self.send_odid_basic_id()
            await self.send_odid_system()
            await self.send_odid_operator_id()

    async def run(self):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.fmu_conn.run())
            tg.create_task(self.dri_conn.run())

            tg.create_task(self.process_fmu_messages())
            tg.create_task(self.process_dri_messages())
            tg.create_task(self.send_odid_messages())
