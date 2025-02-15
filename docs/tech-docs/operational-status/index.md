# Operational Status :construction:

The [Location Message](../messages/location.md#status-m) contains a field for operational status.

!!! quote "EN 4709-002 Requirements"

    UAS operational status of UA shall be set to Emergency (3) when partial or full loss of control of the flight trajectory occurs.
    This may happen in case of:

    - low battery;
    - loss of C2;
    - loss of GNSS.

PX4 publishes this message, with the following sitations declared as Emergency:

- [Low Battery](low-battery.md) when the battery percentage drops below the configured critical battery threshold.
- [Loss of C2](c2-link-loss.md) when the C2 link is lost (e.g. rebooted Herelink).
- [Loss of GNSS](gnss-loss.md) when the GNSS signal is lost while the flight mode depends on it.
