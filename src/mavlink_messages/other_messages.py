from .base import MavlinkMessage

__all__ = ["SystemTime", "GpsRawInt", "GlobalPositionInt", "Altitude", "HomePosition"]


class SystemTime(MavlinkMessage):
    """
    MAVlink SYSTEM_TIME (2) message.

    The system time is the time of the master clock, typically the computer clock of the main onboard computer.
    """

    time_unix_usec: int
    """Timestamp (UNIX epoch time)."""

    time_boot_ms: int
    """Timestamp (time since system boot)."""


class GpsRawInt(MavlinkMessage):
    """
    MAVlink GPS_RAW_INT (24) message.

    The global position, as returned by the Global Positioning System (GPS).
    This is NOT the global position estimate of the system, but rather a RAW sensor value.
    See message GLOBAL_POSITION for the global position estimate.
    """

    time_usec: int
    """
    Timestamp (UNIX Epoch time or time since system boot). The receiving end can infer timestamp format
    (since 1.1.1970 or since system boot) by checking for the magnitude of the number.
    """

    fix_type: int
    """GPS fix type."""

    lat: int
    """Latitude (WGS84, EGM96 ellipsoid), in degrees * 1E7."""

    lon: int
    """Longitude (WGS84, EGM96 ellipsoid), in degrees * 1E7."""

    alt: int
    """
    Altitude (MSL). Positive for up.
    Note that virtually all GPS modules provide the MSL altitude in addition to the WGS84 altitude.
    """

    eph: int
    """GPS HDOP horizontal dilution of position (unitless * 100). If unknown, set to: UINT16_MAX."""

    epv: int
    """GPS VDOP vertical dilution of position (unitless * 100). If unknown, set to: UINT16_MAX."""

    vel: int
    """GPS ground speed (m/s * 100). If unknown, set to: UINT16_MAX."""

    cog: int
    """
    Course over ground (NOT heading, but direction of movement) in degrees * 100, 0.0..359.99 degrees.
    If unknown, set to: UINT16_MAX.
    """

    satellites_visible: int
    """Number of satellites visible. If unknown, set to 255."""


class GlobalPositionInt(MavlinkMessage):
    """
    MAVlink GLOBAL_POSITION_INT (33) message.

    The filtered global position (e.g. fused GPS and accelerometers). The position is in GPS-frame (right-handed, Z-up).
    All fields are populated in meters or degrees * 1E7 for compressed transmission.
    """

    time_boot_ms: int
    """Timestamp (time since system boot)."""

    lat: int
    """Latitude, expressed in degrees * 1E7."""

    lon: int
    """Longitude, expressed in degrees * 1E7."""

    alt: int
    """Altitude (MSL). Note that virtually all GPS modules provide both WGS84 and MSL."""

    relative_alt: int
    """Altitude above ground."""

    vx: int
    """Ground X Speed (Latitude, positive north), expressed as m/s * 100."""

    vy: int
    """Ground Y Speed (Longitude, positive east), expressed as m/s * 100."""

    vz: int
    """Ground Z Speed (Altitude, positive down), expressed as m/s * 100."""

    hdg: int
    """Vehicle heading (yaw angle), 0.0..359.99 degrees. If unknown, set to: UINT16_MAX."""


class Altitude(MavlinkMessage):
    """
    MAVlink ALTITUDE (141) message.

    The current system altitude.
    """

    time_usec: int
    """Timestamp (UNIX Epoch time or time since system boot)."""

    altitude_monotonic: float
    """
    This altitude measure is initialized on system boot and monotonic
    (it is never reset, but represents the local altitude change).
    """

    altitude_amsl: float
    """
    This altitude measure is strictly above mean sea level and might be non-monotonic
    (it might reset on events like GPS lock or when a new QNH value is set).
    """

    altitude_local: float
    """This is the local altitude in the local coordinate frame."""

    altitude_relative: float
    """This is the altitude above the home position."""

    altitude_terrain: float
    """This is the altitude above terrain."""

    bottom_clearance: float
    """This is not the altitude, but the clear space below the system according to the fused clearance estimate."""


class HomePosition(MavlinkMessage):
    """
    MAVlink HOME_POSITION (242) message.

    Contains the home position. The home position is the default position that the system will return to and land on.
    The position must be set automatically by the system during the takeoff, and may also be explicitly set using
    MAV_CMD_DO_SET_HOME.
    """

    latitude: int
    """Latitude (WGS84), in degrees * 1E7."""

    longitude: int
    """Longitude (WGS84), in degrees * 1E7."""

    altitude: int
    """Altitude (MSL), in mm. Positive for up."""

    x: float
    """Local X position of this position in the local coordinate frame (NED)."""

    y: float
    """Local Y position of this position in the local coordinate frame (NED)."""

    z: float
    """Local Z position of this position in the local coordinate frame (NED: positive "down")."""

    q: list[float]
    """
    Quaternion indicating world-to-surface-normal and heading transformation of the takeoff position.
    Used to indicate the heading and slope of the ground.
    """
