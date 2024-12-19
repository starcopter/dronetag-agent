import asyncio

import libmav

from async_libmav import AsyncLibmavConnection


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
        self.phy = libmav.TCPClient(mavlink_endpoint_ip, mavlink_endpoint_port)
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
            self.phy,
            message_set=self.message_set,
            system_id=fmu_system_id,
            component_id=fmu_component_id,
            heartbeat=fmu_heartbeat,
        )
        self.dri_conn = AsyncLibmavConnection(
            self.phy,
            message_set=self.message_set,
            system_id=dri_system_id,
            component_id=dri_component_id,
            heartbeat=dri_heartbeat,
        )



    async def run(self):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.fmu_conn.run())
            tg.create_task(self.dri_conn.run())


async def main():
    # ip = "172.17.0.1" if get_skynode_serial_number() else "10.41.0.1"
    ip = "10.41.0.1"

    gateway = DronetagGateway(ip, 5790)
    await gateway.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
