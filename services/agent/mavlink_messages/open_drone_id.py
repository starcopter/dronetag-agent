from .base import MavlinkMessage
from .enums import (
    ArmStatus,
    AuthType,
    CategoryEU,
    ClassEU,
    ClassificationType,
    DescType,
    HeightRef,
    HorizontalAccuracy,
    IDType,
    OperatorIDType,
    OperatorLocationType,
    SpeedAccuracy,
    Status,
    TimeAccuracy,
    UAType,
    VerticalAccuracy,
)

__all__ = [
    "BasicID",
    "Location",
    "Authentication",
    "SelfID",
    "System",
    "OperatorID",
    "MessagePack",
    "ArmStatusMsg",
    "SystemUpdate",
]


class BasicID(MavlinkMessage):
    """
    MAVlink OPEN_DRONE_ID_BASIC_ID (12900) message.

    Data for filling the OpenDroneID Basic ID message. This and the below messages are primarily meant for feeding data
    to/from an OpenDroneID implementation. E.g. https://github.com/opendroneid/opendroneid-core-c. These messages are
    compatible with the ASTM F3411 Remote ID standard and the ASD-STAN prEN 4709-002 Direct Remote ID standard.
    Additional information and usage of these messages is documented at https://mavlink.io/en/services/opendroneid.html.
    """

    target_system: int = 0
    """System ID (0 for broadcast)."""

    target_component: int = 0
    """Component ID (0 for broadcast)."""

    id_or_mac: list[int] = []
    """
    Only used for drone ID data received from other UAs.
    See detailed description at https://mavlink.io/en/services/opendroneid.html.
    """

    id_type: IDType
    """Indicates the format for the uas_id field of this message."""

    ua_type: UAType
    """Indicates the type of UA (Unmanned Aircraft)."""

    uas_id: list[int]
    """
    UAS (Unmanned Aircraft System) ID following the format specified by id_type.
    Shall be filled with nulls in the unused portion of the field.
    """


class Location(MavlinkMessage):
    """
    MAVlink OPEN_DRONE_ID_LOCATION (12901) message.

    Data for filling the OpenDroneID Location message. The float data types are 32-bit IEEE 754.
    The Location message provides the location, altitude, direction and speed of the aircraft.
    """

    target_system: int
    """System ID (0 for broadcast)."""

    target_component: int
    """Component ID (0 for broadcast)."""

    id_or_mac: list[int]
    """
    Only used for drone ID data received from other UAs.
    See detailed description at https://mavlink.io/en/services/opendroneid.html.
    """

    status: Status
    """Indicates whether the unmanned aircraft is on the ground or in the air."""

    direction: int
    """
    Direction over ground (not heading, but direction of movement) measured clockwise from true North: 0 - 35999 centi-degrees.
    If unknown: 36100 centi-degrees.
    """

    speed_horizontal: int
    """Ground speed. Positive only. If unknown: 25500 cm/s. If speed is larger than 25425 cm/s, use 25425 cm/s."""

    speed_vertical: int
    """
    The vertical speed. Up is positive. If unknown: 6300 cm/s. If speed is larger than 6200 cm/s, use 6200 cm/s.
    If lower than -6200 cm/s, use -6200 cm/s.
    """

    latitude: int
    """Current latitude of the unmanned aircraft. If unknown: 0 (both Lat/Lon)."""

    longitude: int
    """Current longitude of the unmanned aircraft. If unknown: 0 (both Lat/Lon)."""

    altitude_barometric: float
    """The altitude calculated from the barometric pressue. Reference is against 29.92inHg or 1013.2mb. If unknown: -1000 m."""

    altitude_geodetic: float
    """The geodetic altitude as defined by WGS84. If unknown: -1000 m."""

    height_reference: HeightRef
    """Indicates the reference point for the height field."""

    height: float
    """
    The current height of the unmanned aircraft above the take-off location or the ground as indicated by height_reference.
    If unknown: -1000 m.
    """

    horizontal_accuracy: HorizontalAccuracy
    """The accuracy of the horizontal position."""

    vertical_accuracy: VerticalAccuracy
    """The accuracy of the vertical position."""

    barometer_accuracy: VerticalAccuracy
    """The accuracy of the barometric altitude."""

    speed_accuracy: SpeedAccuracy
    """The accuracy of the horizontal and vertical speed."""

    timestamp: float
    """
    Seconds after the full hour with reference to UTC time. Typically the GPS outputs a time-of-week value in milliseconds.
    First convert that to UTC and then convert for this field using ((float) (time_week_ms % (60*60*1000))) / 1000.
    If unknown: 0xFFFF.
    """

    timestamp_accuracy: TimeAccuracy
    """The accuracy of the timestamps."""


class Authentication(MavlinkMessage):
    """
    MAVlink OPEN_DRONE_ID_AUTHENTICATION (12902) message.

    Data for filling the OpenDroneID Authentication message. The Authentication Message defines a field that can provide
    a means of authenticity for the identity of the UAS (Unmanned Aircraft System). The Authentication message can have
    two different formats. For data page 0, the fields PageCount, Length and TimeStamp are present and AuthData is only
    17 bytes. For data page 1 through 15, PageCount, Length and TimeStamp are not present and the size of AuthData is 23 bytes.
    """

    target_system: int
    """System ID (0 for broadcast)."""

    target_component: int
    """Component ID (0 for broadcast)."""

    id_or_mac: list[int]
    """
    Only used for drone ID data received from other UAs.
    See detailed description at https://mavlink.io/en/services/opendroneid.html.
    """

    authentication_type: AuthType
    """Indicates the type of authentication."""

    data_page: int
    """Allowed range is 0 - 15."""

    last_page_index: int
    """
    This field is only present for page 0. Allowed range is 0 - 15.
    See the description of struct ODID_Auth_data at https://github.com/opendroneid/opendroneid-core-c/blob/master/libopendroneid/opendroneid.h.
    """

    length: int
    """
    This field is only present for page 0. Total bytes of authentication_data from all data pages.
    See the description of struct ODID_Auth_data at https://github.com/opendroneid/opendroneid-core-c/blob/master/libopendroneid/opendroneid.h.
    """

    timestamp: int
    """This field is only present for page 0. 32 bit Unix Timestamp in seconds since 00:00:00 01/01/2019."""

    authentication_data: list[int]
    """
    Opaque authentication data. For page 0, the size is only 17 bytes. For other pages, the size is 23 bytes.
    Shall be filled with nulls in the unused portion of the field.
    """


class SelfID(MavlinkMessage):
    """
    MAVlink OPEN_DRONE_ID_SELF_ID (12903) message.

    Data for filling the OpenDroneID Self ID message. The Self ID Message is an opportunity for the operator to
    (optionally) declare their identity and purpose of the flight. This message can provide additional information
    that could reduce the threat profile of a UA (Unmanned Aircraft) flying in a particular area or manner.
    This message can also be used to provide optional additional clarification in an emergency/remote ID system failure situation.
    """

    target_system: int
    """System ID (0 for broadcast)."""

    target_component: int
    """Component ID (0 for broadcast)."""

    id_or_mac: list[int]
    """
    Only used for drone ID data received from other UAs.
    See detailed description at https://mavlink.io/en/services/opendroneid.html.
    """

    description_type: DescType
    """Indicates the type of the description field."""

    description: str
    """Text description or numeric value expressed as ASCII characters. Shall be filled with nulls in the unused portion of the field."""


class System(MavlinkMessage):
    """
    MAVlink OPEN_DRONE_ID_SYSTEM (12904) message.

    Data for filling the OpenDroneID System message. The System Message contains general system information including
    the operator location/altitude and possible aircraft group and/or category/class information.
    """

    target_system: int
    """System ID (0 for broadcast)."""

    target_component: int
    """Component ID (0 for broadcast)."""

    id_or_mac: list[int]
    """
    Only used for drone ID data received from other UAs.
    See detailed description at https://mavlink.io/en/services/opendroneid.html.
    """

    operator_location_type: OperatorLocationType
    """Specifies the operator location type."""

    classification_type: ClassificationType
    """Specifies the classification type of the UA."""

    operator_latitude: int
    """Latitude of the operator. If unknown: 0 (both Lat/Lon)."""

    operator_longitude: int
    """Longitude of the operator. If unknown: 0 (both Lat/Lon)."""

    area_count: int
    """Number of aircraft in the area, group or formation (default 1). Used only for swarms/multiple UA."""

    area_radius: int
    """Radius of the cylindrical area of the group or formation (default 0). Used only for swarms/multiple UA."""

    area_ceiling: float
    """Area Operations Ceiling relative to WGS84. If unknown: -1000 m. Used only for swarms/multiple UA."""

    area_floor: float
    """Area Operations Floor relative to WGS84. If unknown: -1000 m. Used only for swarms/multiple UA."""

    category_eu: CategoryEU
    """When classification_type is MAV_ODID_CLASSIFICATION_TYPE_EU, specifies the category of the UA."""

    class_eu: ClassEU
    """When classification_type is MAV_ODID_CLASSIFICATION_TYPE_EU, specifies the class of the UA."""

    operator_altitude_geo: float
    """Geodetic altitude of the operator relative to WGS84. If unknown: -1000 m."""

    timestamp: int
    """32 bit Unix Timestamp in seconds since 00:00:00 01/01/2019."""


class OperatorID(MavlinkMessage):
    """
    MAVlink OPEN_DRONE_ID_OPERATOR_ID (12905) message.

    Data for filling the OpenDroneID Operator ID message, which contains the CAA (Civil Aviation Authority)
    issued operator ID.
    """

    target_system: int
    """System ID (0 for broadcast)."""

    target_component: int
    """Component ID (0 for broadcast)."""

    id_or_mac: list[int]
    """
    Only used for drone ID data received from other UAs.
    See detailed description at https://mavlink.io/en/services/opendroneid.html.
    """

    operator_id_type: OperatorIDType
    """Indicates the type of the operator_id field."""

    operator_id: str
    """Text description or numeric value expressed as ASCII characters. Shall be filled with nulls in the unused portion of the field."""


class MessagePack(MavlinkMessage):
    """
    MAVlink OPEN_DRONE_ID_MESSAGE_PACK (12915) message.

    An OpenDroneID message pack is a container for multiple encoded OpenDroneID messages (i.e. not in the format given
    for the above message descriptions but after encoding into the compressed OpenDroneID byte format).
    Used e.g. when transmitting on Bluetooth 5.0 Long Range/Extended Advertising or on WiFi Neighbor Aware Networking
    or on WiFi Beacon.
    """

    target_system: int
    """System ID (0 for broadcast)."""

    target_component: int
    """Component ID (0 for broadcast)."""

    id_or_mac: list[int]
    """
    Only used for drone ID data received from other UAs.
    See detailed description at https://mavlink.io/en/services/opendroneid.html.
    """

    single_message_size: int
    """This field must currently always be equal to 25 (bytes), since all encoded OpenDroneID messages are specified to have this length."""

    msg_pack_size: int
    """Number of encoded messages in the pack (not the number of bytes). Allowed range is 1 - 9."""

    messages: list[int]
    """Concatenation of encoded OpenDroneID messages. Shall be filled with nulls in the unused portion of the field."""


class ArmStatusMsg(MavlinkMessage):
    """
    MAVlink OPEN_DRONE_ID_ARM_STATUS (12918) message.

    Transmitter (remote ID system) is enabled and ready to start sending location and other required information.
    This is streamed by transmitter. A flight controller uses it as a condition to arm.
    """

    status: ArmStatus
    """Status level indicating if arming is allowed."""

    error: str
    """Text error message, should be empty if status is good to arm. Fill with nulls in unused portion."""


class SystemUpdate(MavlinkMessage):
    """
    MAVlink OPEN_DRONE_ID_SYSTEM_UPDATE (12919) message.

    Update the data in the OPEN_DRONE_ID_SYSTEM message with new location information. This can be sent to update
    the location information for the operator when no other information in the SYSTEM message has changed.
    This message allows for efficient operation on radio links which have limited uplink bandwidth while meeting
    requirements for update frequency of the operator location.
    """

    target_system: int
    """System ID (0 for broadcast)."""

    target_component: int
    """Component ID (0 for broadcast)."""

    operator_latitude: int
    """Latitude of the operator. If unknown: 0 (both Lat/Lon)."""

    operator_longitude: int
    """Longitude of the operator. If unknown: 0 (both Lat/Lon)."""

    operator_altitude_geo: float
    """Geodetic altitude of the operator relative to WGS84. If unknown: -1000 m."""

    timestamp: int
    """32 bit Unix Timestamp in seconds since 00:00:00 01/01/2019."""
