# General Design

Requirements from chapter 4 from EN 4709-002:2023.

## 4.2 Mandatory information

The direct remote ID system shall broadcast locally the mandatory information listed below:

- [x] Identification information:
    - [x] the UAS operator registration number :material-arrow-right-thin: [Operator ID](../messages/operator-id.md#operator-id-m)
    - [x] the unique serial number of the UA :material-arrow-right-thin: [Basic ID](../messages/basic-id.md#uas-id-m)
- [x] Geolocation information:
    - [x] the time stamp, the geographical position of the UA and its height above ~~the ground or~~ its takeoff point
          :material-arrow-right-thin: [Location](../messages/location.md#latitude-and-longitude-m)
    - [x] the route course measured clockwise from true north and ground speed of the UA
          :material-arrow-right-thin: [Direction](../messages/location.md#direction-m)
    - [x] ~~the geographical position of the remote pilot, or if not available,~~ the geographical position of the take-off point
          :material-arrow-right-thin: [Operator Location](../messages/system.md#operator-location-type-m)
- [x] UA status information:
    - [x] the UAS emergency status for Class C3
          :material-arrow-right-thin: [Operational Status](../messages/location.md#status-m)

!!! success

    All of the above are implemented in the Dronetag Agent.
    See the [Messages](../messages/index.md) section for more information.

## 4.3 Security of the DRI system

### General security requirement

The direct remote identification system shall reduce the ability of tampering with the functionality of the direct remote identification system.

!!! info

    In this sense, the _direct remote identification system_ is the DRI module, not the Dronetag Agent.

!!! success

    As the DRI module is enclosed in the HIGHDRA, the user would need to physically disassemble the HIGHDRA to tamper with the DRI module.
    The software (Dronetag Agent) is protected against tampering by a password.

### Specific security requirements

#### Serial Number

!!! quote "Requirement"

    The UA comes with a unique serial number; this number is loaded at factory level and shall not be modified anymore afterwards.
    The protection of the unique serial number of the UA shall be done by design. The serial number shall be stored in a secure memory area.

The serial number is programmed to the HIGHDRA at starcopter during the manucfacturing process.
It is then stored persistently in onboard eMMC memory, which is part of the onboard mission computer.
The Dronetag Agent reads that serial from `/persistent/suite/vehicle_sn`.
This memory is only accessible from _inside_ the mission computer, which requires SSH access to the embedded Linux system.

!!! success

    As the user does not have SSH access to the onboard system, the serial number can be considered secure.

#### Geolocation Information

!!! quote "Requirement"

    The design of the DRI shall not allow the user to modify the Geolocation information part of the DRI message, as defined in 4.2 above.

All geolocation information is provided directly by the flight management unit (FMU) itself:

- timestamp, UA position, UA height above takeoff location and ground course inside the [Location](../messages/location.md) message
- the takeoff location via the [HOME_POSITION] MAVLink message (see [System](../messages/system.md#implementation) message)

!!! success

    It is not possible for the user to modify the geolocation information, as it is provided directly by the FMU itself.
    Short of physically removing the FMU from the HIGHDRA, there is no way to modify the geolocation information.

[HOME_POSITION]: https://mavlink.io/en/messages/common.html#HOME_POSITION

## 4.5 Performance requirements

This document defines several performance requirements:

- radio transmission performance: as radio-transmitting equipment, a DRI system shall comply with
  relevant standards on radio-transmitting equipment: ETSI EN 301 893 for Wi-Fi 5GHz and
  ETSI EN 300 328 V2.1.1 for Bluetooth and Wi-Fi 2,4 GHz (see Clause 2). These standards define
  only maximum transmit power values. To guarantee minimum performance of a DRI system, the
  DRI equipment shall comply with the minimum output power values defined in 5.4 and emission
  directivity requirements defined in 5.5;

- data transmission and update rates: to allow proper identification and tracking of UA by observers,
  the remote identification information shall be broadcasted periodically as defined in 5.6;

- direct remote identification information shall be received by existing mobile receiver devices (such
  as a smartphone, tablet, laptop, or any kind of mobile device).

## 4.6 Working time

The information broadcasted by the DRI system shall be transmitted during the whole duration of the flight (i.e. when the drone is airborne).
The broadcasted information can optionally also be transmitted when the drone is on the ground (i.e. from switch-on to switch-off).

!!! success

    The DRI module broadcasts the information as long as the drone is powered, including when it is on the ground.
