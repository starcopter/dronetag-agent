from enum import IntEnum

__all__ = [
    "IDType",
    "UAType",
    "Status",
    "HeightRef",
    "HorizontalAccuracy",
    "VerticalAccuracy",
    "SpeedAccuracy",
    "TimeAccuracy",
    "AuthType",
    "DescType",
    "OperatorLocationType",
    "ClassificationType",
    "CategoryEU",
    "ClassEU",
    "OperatorIDType",
    "ArmStatus",
]


class IDType(IntEnum):
    """MAVlink MAV_ODID_ID_TYPE values."""

    MAV_ODID_ID_TYPE_NONE = 0
    """No type defined."""

    MAV_ODID_ID_TYPE_SERIAL_NUMBER = 1
    """Manufacturer Serial Number (ANSI/CTA-2063 format)."""

    MAV_ODID_ID_TYPE_CAA_REGISTRATION_ID = 2
    """CAA (Civil Aviation Authority) registered ID. Format: [ICAO Country Code].[CAA Assigned ID]."""

    MAV_ODID_ID_TYPE_UTM_ASSIGNED_UUID = 3
    """UTM (Unmanned Traffic Management) assigned UUID (RFC4122)."""

    MAV_ODID_ID_TYPE_SPECIFIC_SESSION_ID = 4
    """
    A 20 byte ID for a specific flight/session.
    The exact ID type is indicated by the first byte of uas_id and these type values are managed by ICAO.
    """


class UAType(IntEnum):
    """MAVlink MAV_ODID_UA_TYPE values."""

    MAV_ODID_UA_TYPE_NONE = 0
    """No UA (Unmanned Aircraft) type defined."""

    MAV_ODID_UA_TYPE_AEROPLANE = 1
    """Aeroplane/Airplane. Fixed wing."""

    MAV_ODID_UA_TYPE_HELICOPTER_OR_MULTIROTOR = 2
    """Helicopter or multirotor."""

    MAV_ODID_UA_TYPE_GYROPLANE = 3
    """Gyroplane."""

    MAV_ODID_UA_TYPE_HYBRID_LIFT = 4
    """VTOL (Vertical Take-Off and Landing). Fixed wing aircraft that can take off vertically."""

    MAV_ODID_UA_TYPE_ORNITHOPTER = 5
    """Ornithopter."""

    MAV_ODID_UA_TYPE_GLIDER = 6
    """Glider."""

    MAV_ODID_UA_TYPE_KITE = 7
    """Kite."""

    MAV_ODID_UA_TYPE_FREE_BALLOON = 8
    """Free Balloon."""

    MAV_ODID_UA_TYPE_CAPTIVE_BALLOON = 9
    """Captive Balloon."""

    MAV_ODID_UA_TYPE_AIRSHIP = 10
    """Airship. E.g. a blimp."""

    MAV_ODID_UA_TYPE_FREE_FALL_PARACHUTE = 11
    """Free Fall/Parachute (unpowered)."""

    MAV_ODID_UA_TYPE_ROCKET = 12
    """Rocket."""

    MAV_ODID_UA_TYPE_TETHERED_POWERED_AIRCRAFT = 13
    """Tethered powered aircraft."""

    MAV_ODID_UA_TYPE_GROUND_OBSTACLE = 14
    """Ground Obstacle."""

    MAV_ODID_UA_TYPE_OTHER = 15
    """Other type of aircraft not listed earlier."""


class Status(IntEnum):
    """MAVlink MAV_ODID_STATUS values."""

    MAV_ODID_STATUS_UNDECLARED = 0
    """The status of the (UA) Unmanned Aircraft is undefined."""

    MAV_ODID_STATUS_GROUND = 1
    """The UA is on the ground."""

    MAV_ODID_STATUS_AIRBORNE = 2
    """The UA is in the air."""

    MAV_ODID_STATUS_EMERGENCY = 3
    """The UA is having an emergency."""

    MAV_ODID_STATUS_REMOTE_ID_SYSTEM_FAILURE = 4
    """The remote ID system is failing or unreliable in some way."""


class HeightRef(IntEnum):
    """MAVlink MAV_ODID_HEIGHT_REF values."""

    MAV_ODID_HEIGHT_REF_OVER_TAKEOFF = 0
    """The height field is relative to the take-off location."""

    MAV_ODID_HEIGHT_REF_OVER_GROUND = 1
    """The height field is relative to ground."""


class HorizontalAccuracy(IntEnum):
    """MAVlink MAV_ODID_HOR_ACC values."""

    MAV_ODID_HOR_ACC_UNKNOWN = 0
    """The horizontal accuracy is unknown."""

    MAV_ODID_HOR_ACC_10NM = 1
    """The horizontal accuracy is smaller than 10 Nautical Miles. 18.52 km."""

    MAV_ODID_HOR_ACC_4NM = 2
    """The horizontal accuracy is smaller than 4 Nautical Miles. 7.408 km."""

    MAV_ODID_HOR_ACC_2NM = 3
    """The horizontal accuracy is smaller than 2 Nautical Miles. 3.704 km."""

    MAV_ODID_HOR_ACC_1NM = 4
    """The horizontal accuracy is smaller than 1 Nautical Miles. 1.852 km."""

    MAV_ODID_HOR_ACC_0_5NM = 5
    """The horizontal accuracy is smaller than 0.5 Nautical Miles. 926 m."""

    MAV_ODID_HOR_ACC_0_3NM = 6
    """The horizontal accuracy is smaller than 0.3 Nautical Miles. 555.6 m."""

    MAV_ODID_HOR_ACC_0_1NM = 7
    """The horizontal accuracy is smaller than 0.1 Nautical Miles. 185.2 m."""

    MAV_ODID_HOR_ACC_0_05NM = 8
    """The horizontal accuracy is smaller than 0.05 Nautical Miles. 92.6 m."""

    MAV_ODID_HOR_ACC_30_METER = 9
    """The horizontal accuracy is smaller than 30 meter."""

    MAV_ODID_HOR_ACC_10_METER = 10
    """The horizontal accuracy is smaller than 10 meter."""

    MAV_ODID_HOR_ACC_3_METER = 11
    """The horizontal accuracy is smaller than 3 meter."""

    MAV_ODID_HOR_ACC_1_METER = 12
    """The horizontal accuracy is smaller than 1 meter."""


class VerticalAccuracy(IntEnum):
    """MAVlink MAV_ODID_VER_ACC values."""

    MAV_ODID_VER_ACC_UNKNOWN = 0
    """The vertical accuracy is unknown."""

    MAV_ODID_VER_ACC_150_METER = 1
    """The vertical accuracy is smaller than 150 meter."""

    MAV_ODID_VER_ACC_45_METER = 2
    """The vertical accuracy is smaller than 45 meter."""

    MAV_ODID_VER_ACC_25_METER = 3
    """The vertical accuracy is smaller than 25 meter."""

    MAV_ODID_VER_ACC_10_METER = 4
    """The vertical accuracy is smaller than 10 meter."""

    MAV_ODID_VER_ACC_3_METER = 5
    """The vertical accuracy is smaller than 3 meter."""

    MAV_ODID_VER_ACC_1_METER = 6
    """The vertical accuracy is smaller than 1 meter."""


class SpeedAccuracy(IntEnum):
    """MAVlink MAV_ODID_SPEED_ACC values."""

    MAV_ODID_SPEED_ACC_UNKNOWN = 0
    """The speed accuracy is unknown."""

    MAV_ODID_SPEED_ACC_10_METERS_PER_SECOND = 1
    """The speed accuracy is smaller than 10 meters per second."""

    MAV_ODID_SPEED_ACC_3_METERS_PER_SECOND = 2
    """The speed accuracy is smaller than 3 meters per second."""

    MAV_ODID_SPEED_ACC_1_METERS_PER_SECOND = 3
    """The speed accuracy is smaller than 1 meters per second."""

    MAV_ODID_SPEED_ACC_0_3_METERS_PER_SECOND = 4
    """The speed accuracy is smaller than 0.3 meters per second."""


class TimeAccuracy(IntEnum):
    """MAVlink MAV_ODID_TIME_ACC values."""

    MAV_ODID_TIME_ACC_UNKNOWN = 0
    """The timestamp accuracy is unknown."""

    MAV_ODID_TIME_ACC_0_1_SECOND = 1
    """The timestamp accuracy is smaller than or equal to 0.1 second."""

    MAV_ODID_TIME_ACC_0_2_SECOND = 2
    """The timestamp accuracy is smaller than or equal to 0.2 second."""

    MAV_ODID_TIME_ACC_0_3_SECOND = 3
    """The timestamp accuracy is smaller than or equal to 0.3 second."""

    MAV_ODID_TIME_ACC_0_4_SECOND = 4
    """The timestamp accuracy is smaller than or equal to 0.4 second."""

    MAV_ODID_TIME_ACC_0_5_SECOND = 5
    """The timestamp accuracy is smaller than or equal to 0.5 second."""

    MAV_ODID_TIME_ACC_0_6_SECOND = 6
    """The timestamp accuracy is smaller than or equal to 0.6 second."""

    MAV_ODID_TIME_ACC_0_7_SECOND = 7
    """The timestamp accuracy is smaller than or equal to 0.7 second."""

    MAV_ODID_TIME_ACC_0_8_SECOND = 8
    """The timestamp accuracy is smaller than or equal to 0.8 second."""

    MAV_ODID_TIME_ACC_0_9_SECOND = 9
    """The timestamp accuracy is smaller than or equal to 0.9 second."""

    MAV_ODID_TIME_ACC_1_0_SECOND = 10
    """The timestamp accuracy is smaller than or equal to 1.0 second."""

    MAV_ODID_TIME_ACC_1_1_SECOND = 11
    """The timestamp accuracy is smaller than or equal to 1.1 second."""

    MAV_ODID_TIME_ACC_1_2_SECOND = 12
    """The timestamp accuracy is smaller than or equal to 1.2 second."""

    MAV_ODID_TIME_ACC_1_3_SECOND = 13
    """The timestamp accuracy is smaller than or equal to 1.3 second."""

    MAV_ODID_TIME_ACC_1_4_SECOND = 14
    """The timestamp accuracy is smaller than or equal to 1.4 second."""

    MAV_ODID_TIME_ACC_1_5_SECOND = 15
    """The timestamp accuracy is smaller than or equal to 1.5 second."""


class AuthType(IntEnum):
    """MAVlink MAV_ODID_AUTH_TYPE values."""

    MAV_ODID_AUTH_TYPE_NONE = 0
    """No authentication type is specified."""

    MAV_ODID_AUTH_TYPE_UAS_ID_SIGNATURE = 1
    """Signature for the UAS (Unmanned Aircraft System) ID."""

    MAV_ODID_AUTH_TYPE_OPERATOR_ID_SIGNATURE = 2
    """Signature for the Operator ID."""

    MAV_ODID_AUTH_TYPE_MESSAGE_SET_SIGNATURE = 3
    """Signature for the entire message set."""

    MAV_ODID_AUTH_TYPE_NETWORK_REMOTE_ID = 4
    """Authentication is provided by Network Remote ID."""

    MAV_ODID_AUTH_TYPE_SPECIFIC_AUTHENTICATION = 5
    """The exact authentication type is indicated by the first byte of authentication_data and these type values are managed by ICAO."""


class DescType(IntEnum):
    """MAVlink MAV_ODID_DESC_TYPE values."""

    MAV_ODID_DESC_TYPE_TEXT = 0
    """Optional free-form text description of the purpose of the flight."""

    MAV_ODID_DESC_TYPE_EMERGENCY = 1
    """Optional additional clarification when status == MAV_ODID_STATUS_EMERGENCY."""

    MAV_ODID_DESC_TYPE_EXTENDED_STATUS = 2
    """Optional additional clarification when status != MAV_ODID_STATUS_EMERGENCY."""


class OperatorLocationType(IntEnum):
    """MAVlink MAV_ODID_OPERATOR_LOCATION_TYPE values."""

    MAV_ODID_OPERATOR_LOCATION_TYPE_TAKEOFF = 0
    """The location/altitude of the operator is the same as the take-off location."""

    MAV_ODID_OPERATOR_LOCATION_TYPE_LIVE_GNSS = 1
    """The location/altitude of the operator is dynamic. E.g. based on live GNSS data."""

    MAV_ODID_OPERATOR_LOCATION_TYPE_FIXED = 2
    """The location/altitude of the operator are fixed values."""


class ClassificationType(IntEnum):
    """MAVlink MAV_ODID_CLASSIFICATION_TYPE values."""

    MAV_ODID_CLASSIFICATION_TYPE_UNDECLARED = 0
    """The classification type for the UA is undeclared."""

    MAV_ODID_CLASSIFICATION_TYPE_EU = 1
    """The classification type for the UA follows EU (European Union) specifications."""


class CategoryEU(IntEnum):
    """MAVlink MAV_ODID_CATEGORY_EU values."""

    MAV_ODID_CATEGORY_EU_UNDECLARED = 0
    """The category for the UA, according to the EU specification, is undeclared."""

    MAV_ODID_CATEGORY_EU_OPEN = 1
    """The category for the UA, according to the EU specification, is the Open category."""

    MAV_ODID_CATEGORY_EU_SPECIFIC = 2
    """The category for the UA, according to the EU specification, is the Specific category."""

    MAV_ODID_CATEGORY_EU_CERTIFIED = 3
    """The category for the UA, according to the EU specification, is the Certified category."""


class ClassEU(IntEnum):
    """MAVlink MAV_ODID_CLASS_EU values."""

    MAV_ODID_CLASS_EU_UNDECLARED = 0
    """The class for the UA, according to the EU specification, is undeclared."""

    MAV_ODID_CLASS_EU_CLASS_0 = 1
    """The class for the UA, according to the EU specification, is Class 0."""

    MAV_ODID_CLASS_EU_CLASS_1 = 2
    """The class for the UA, according to the EU specification, is Class 1."""

    MAV_ODID_CLASS_EU_CLASS_2 = 3
    """The class for the UA, according to the EU specification, is Class 2."""

    MAV_ODID_CLASS_EU_CLASS_3 = 4
    """The class for the UA, according to the EU specification, is Class 3."""

    MAV_ODID_CLASS_EU_CLASS_4 = 5
    """The class for the UA, according to the EU specification, is Class 4."""

    MAV_ODID_CLASS_EU_CLASS_5 = 6
    """The class for the UA, according to the EU specification, is Class 5."""

    MAV_ODID_CLASS_EU_CLASS_6 = 7
    """The class for the UA, according to the EU specification, is Class 6."""


class OperatorIDType(IntEnum):
    """MAVlink MAV_ODID_OPERATOR_ID_TYPE values."""

    MAV_ODID_OPERATOR_ID_TYPE_CAA = 0
    """CAA (Civil Aviation Authority) registered operator ID."""


class ArmStatus(IntEnum):
    """MAVlink MAV_ODID_ARM_STATUS values."""

    MAV_ODID_ARM_STATUS_GOOD_TO_ARM = 0
    """Passing arming checks."""

    MAV_ODID_ARM_STATUS_PRE_ARM_FAIL_GENERIC = 1
    """Generic arming failure, see error string for details."""
