# Self-ID

!!! info

    This message is optional and not implemented. Feel free to ignore this page and continue to the [System Message](system.md).

The Self-ID message corresponds to the MAVLink [ODID_SELF_ID] message.

[ODID_SELF_ID]: https://mavlink.io/en/messages/common.html#OPEN_DRONE_ID_SELF_ID

??? quote "5.2.5 Self-ID message"

    Self-ID message has type 0x3 value, static periodicity and it is optional.

    The self-ID message is optionally sent in case the remote pilot wishes to declare its identity, flight
    purpose or both. This may serve as mitigation of a perceived threat by a neighbouring person or public
    in case a UA is operating in the same close area.

## Fields

| Name             |  C3   | Description               |
| ---------------- | :---: | ------------------------- |
| Description Type | **O** | Type of Description field |
| Description      | **O** | ASCII description         |

### Description Type (O)

Type of Description field.

| Value   | Meaning                        |
| ------- | ------------------------------ |
| 0       | Text                           |
| 1-200   | Reserved                       |
| 201-255 | Available for experimental use |

### Description (O)

ASCII description text, null-padded to 23 characters.

## Implementation

The Self-ID message is optional, and PX4 does not publish it.
As this message is not needed, it is currently not implemented.
