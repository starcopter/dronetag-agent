---
hide: toc
---

# Messages Reference

The Dronetag Agent uses the [Open Drone ID](https://mavlink.io/en/services/opendroneid.html) MAVLink microservice
to relay information from flight management unit (FMU) and the Agent to the DRI module.

## Messages

The ASTM, EN 4709-002 and MAVLink messages are listed below.

| ASTM                          | EN 4709-002           | MAVLink            | Purpose                                                                                                                                                                                                                                                                                   |
| ----------------------------- | --------------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Basic ID](basic-id.md)       | 5.2.3 Basic ID        | [ODID_BASIC_ID]    | Provides an ID for the UA, characterizes the type of ID and identifies the type of UA.                                                                                                                                                                                                    |
| [Location](location.md)       | 5.2.4 Location/Vector | [ODID_LOCATION]    | Provides location, altitude, direction, and speed of the UA.                                                                                                                                                                                                                              |
| [Self-ID](self-id.md)         | 5.2.5 Self-ID         | [ODID_SELF_ID]     | Optional plain text message that can be used by operators to identify themselves and the purpose of an operation. Can also be used to provide optional additional clarification in an emergency/remote ID system failure situation.                                                       |
| [System](system.md)           | 5.2.6 System          | [ODID_SYSTEM]      | Includes the operator location/altitude, multiple aircraft information (group/swarm, if applicable), full timestamp and possible category/class information.                                                                                                                              |
| [Operator ID](operator-id.md) | 5.2.7 Operator ID     | [ODID_OPERATOR_ID] | Provides the operator ID.                                                                                                                                                                                                                                                                 |
| [ARM Status](arm-status.md)   |                       | [ODID_ARM_STATUS]  | Sent by RID transmitter/receiver components to indicate that the RID system is "ready to use". This should be used as an arming condition for the flight stack. Note that this differs from the HEARTBEAT which indicates that the component is "alive" but not necessarily ready to use. |

[ODID_BASIC_ID]: https://mavlink.io/en/messages/common.html#OPEN_DRONE_ID_BASIC_ID
[ODID_LOCATION]: https://mavlink.io/en/messages/common.html#OPEN_DRONE_ID_LOCATION
[ODID_SELF_ID]: https://mavlink.io/en/messages/common.html#OPEN_DRONE_ID_SELF_ID
[ODID_SYSTEM]: https://mavlink.io/en/messages/common.html#OPEN_DRONE_ID_SYSTEM
[ODID_OPERATOR_ID]: https://mavlink.io/en/messages/common.html#OPEN_DRONE_ID_OPERATOR_ID
[ODID_ARM_STATUS]: https://mavlink.io/en/messages/common.html#OPEN_DRONE_ID_ARM_STATUS
