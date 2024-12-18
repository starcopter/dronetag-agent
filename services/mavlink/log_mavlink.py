import asyncio
import gzip
import json
import socket
import time
from datetime import datetime, timezone
from pathlib import Path

import libmav

from async_libmav import AsyncLibmavConnection

try:
    skynode = Path("/etc/skynode").read_text().strip()
except FileNotFoundError:
    skynode = None


def message_to_json(msg: libmav.Message) -> str:
    timestamp_us = time.time_ns() // 1000
    message_dict = {k: v for k, v in msg.to_dict().items() if not k.startswith("_")}
    header_dict = {
        "magic": msg.header.magic,
        "length": msg.header.len,
        "incompat_flags": msg.header.incompat_flags,
        "compat_flags": msg.header.compat_flags,
        "sequence": msg.header.seq,
        "system_id": msg.header.system_id,
        "component_id": msg.header.component_id,
        "message_id": msg.header.message_id,
        "dtype": msg.name,
    }

    json_str = json.dumps(
        {
            "timestamp": timestamp_us,
            "header": header_dict,
            "message": message_dict,
        }
    )

    return json_str


async def main():
    now = datetime.now(tz=timezone.utc)
    now_str = now.strftime("%Y-%m-%d.%H-%M-%S.%Z")

    if skynode:
        logfile = Path("/data", f"mavlink-{skynode}.{now_str}.jsonl.gz")
    else:
        logfile = Path(f"mavlink-{socket.gethostname()}.{now_str}.jsonl.gz")

    print(logfile)

    message_set = libmav.MessageSet("mavlink/common.xml")

    heartbeat = message_set.create("HEARTBEAT").set_from_dict(
        {
            "type": message_set.enum("MAV_TYPE_LOG"),
            "autopilot": message_set.enum("MAV_AUTOPILOT_INVALID"),
            "base_mode": 0,
            "custom_mode": 0,
            "system_status": message_set.enum("MAV_STATE_ACTIVE"),
        }
    )

    if skynode:
        conn_phy = libmav.TCPClient("172.17.0.1", 5790)
    else:
        conn_phy = libmav.Serial("/dev/ttyUSB0", 115200, False)

    conn = AsyncLibmavConnection(conn_phy, message_set, heartbeat=heartbeat)
    conn.start()

    try:
        with gzip.open(logfile, "wb") as f:
            async for msg in conn:
                f.write(message_to_json(msg).encode() + b"\n")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
        pass

    conn.stop()


if __name__ == "__main__":
    asyncio.run(main())
