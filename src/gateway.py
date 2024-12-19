import asyncio
import logging
import time

import libmav

from async_libmav import AsyncLibmavConnection
from mavlink_messages import odid, other

logger = logging.getLogger(__name__)

UNIX_TIMESTAMP_2019_01_01 = 1546300800


class DronetagGateway:
    def __init__(
        self,
        mavlink_endpoint_ip: str,
        mavlink_endpoint_port: int = 5790,
        fmu_system_id: int = 1,
        fmu_component_id: int = 236,  # MAV_COMP_ID_ODID_TXRX_1
        dri_system_id: int = 2,
        dri_component_id: int = 1,  # MAV_COMP_ID_AUTOPILOT1
    ):
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
            libmav.TCPClient(mavlink_endpoint_ip, mavlink_endpoint_port),
            message_set=self.message_set,
            system_id=fmu_system_id,
            component_id=fmu_component_id,
            heartbeat=fmu_heartbeat,
        )
        self.dri_conn = AsyncLibmavConnection(
            libmav.TCPClient(mavlink_endpoint_ip, mavlink_endpoint_port),
            message_set=self.message_set,
            system_id=dri_system_id,
            component_id=dri_component_id,
            heartbeat=dri_heartbeat,
        )

        self.fmu_system_time: other.SystemTime | None = None
        self.fmu_gps_raw_int: other.GpsRawInt | None = None
        self.fmu_global_position_int: other.GlobalPositionInt | None = None
        self.fmu_altitude: other.Altitude | None = None
        self.fmu_home_position: other.HomePosition | None = None
        self.fmu_odid_basic_id: odid.BasicID | None = None
        self.fmu_odid_location: odid.Location | None = None

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
                case "OPEN_DRONE_ID_BASIC_ID":
                    self.fmu_odid_basic_id = odid.BasicID.from_mavlink(message)
                case "OPEN_DRONE_ID_LOCATION":
                    self.fmu_odid_location = odid.Location.from_mavlink(message)
                    # TODO: update emergency status
                    await self.forward_message(message, self.dri_conn)
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
                if message["status"] == odid.ArmStatus.MAV_ODID_ARM_STATUS_GOOD_TO_ARM:
                    logger.debug("ARM_STATUS: OK")
                else:
                    logger.warning(f"ARM_STATUS: {message['error']}")


    async def send_odid_basic_id(self):
        # TODO: use type from fmu_odid_basic_id, use actual serial number
        message = self.message_set.create("OPEN_DRONE_ID_BASIC_ID").set_from_dict(
            {
                "id_type": odid.IDType.MAV_ODID_ID_TYPE_SERIAL_NUMBER,
                "ua_type": odid.UAType.MAV_ODID_UA_TYPE_KITE,
                "uas_id": list("1715800000000".encode("ascii")),
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
        message = self.message_set.create("OPEN_DRONE_ID_OPERATOR_ID").set_from_dict(
            {
                "operator_id_type": self.message_set.enum("MAV_ODID_OPERATOR_ID_TYPE_CAA"),
                "operator_id": "FIN92hello3world",
            }
        )
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


async def main():
    # ip = "172.17.0.1" if get_skynode_serial_number() else "10.41.0.1"
    ip = "10.41.0.1"

    gateway = DronetagGateway(ip, 5790)
    await gateway.run()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
