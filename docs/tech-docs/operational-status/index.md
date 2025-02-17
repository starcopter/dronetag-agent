# Operational Status

The [Location Message](../messages/location.md#status-m) contains a field for operational status.

## Grounded

When the status field is set to Grounded (1), the UA is on the ground. This means:

- either it is not armed, and its propellers are not spinning
- or it is armed, but still/again on the ground (directly before takeoff or after landing)

In both cases, the UA does not pose a threat to other aircraft.

## Airborne

When the status field is set to Airborne (2), the UA is airborne.
This can be directly during takeoff, in the middle of an hour-long mission, or just before landing.

## Emergency

When a partial or full loss of control of the flight trajectory occurs, the status is declared as Emergency (3).

??? quote "EN 4709-002 Requirements"

    UAS operational status of UA shall be set to Emergency (3) when partial or full
    loss of control of the flight trajectory occurs. This may happen in case of:

    - low battery;
    - loss of C2;
    - loss of GNSS.

PX4 declares the following conditions as an Emergency (partial loss of control):

- [Low Battery](low-battery.md) when the battery percentage drops below a critical battery threshold.
- [Loss of C2](c2-link-loss.md) when the C2 link is lost (e.g. rebooted Herelink).
- [Loss of GNSS](gnss-loss.md) when the GNSS signal is lost while the flight mode depends on it.
