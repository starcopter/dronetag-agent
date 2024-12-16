import libmav
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import socket
from functools import partial


try:
    skynode = Path("/etc/skynode").read_text().strip()
except FileNotFoundError:
    skynode = None


def log_message(msg: libmav.Message, logfile: Path):
    timestamp_us = time.time_ns() // 1000
    message_dict = msg.to_dict()
    header_dict = {
        "magic": msg.header.magic,
        "length": msg.header.len,
        "incompat_flags": msg.header.incompat_flags,
        "compat_flags": msg.header.compat_flags,
        "sequence": msg.header.seq,
        "system_id": msg.header.system_id,
        "component_id": msg.header.component_id,
        "message_id": msg.header.message_id,
    }

    json_str = json.dumps(
        {
            "timestamp": timestamp_us,
            "header": header_dict,
            "message": message_dict,
        }
    )

    with logfile.open("a") as f:
        f.write(json_str + "\n")


def main():
    now = datetime.now(tz=timezone.utc)
    now_str = now.strftime("%Y-%m-%d.%H-%M-%S.%Z")

    if skynode:
        logfile = Path("/data", f"mavlink-{skynode}.{now_str}.jsonl")
    else:
        logfile = Path(f"mavlink-{socket.gethostname()}.{now_str}.jsonl")

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

    system_id = 1
    mavlink_identifier = libmav.Identifier(
        system_id, message_set.enum("MAV_COMP_ID_USER1")
    )

    if skynode:
        conn_phy = libmav.TCPClient("172.17.0.1", 5790)
    else:
        conn_phy = libmav.Serial("/dev/ttyUSB0", 115200, False)

    conn_runtime = libmav.NetworkRuntime(
        mavlink_identifier, message_set, heartbeat, conn_phy
    )

    conn = conn_runtime.await_connection(5000)
    conn.add_message_callback(partial(log_message, logfile=logfile))

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            break


if __name__ == "__main__":
    main()
