# DRI Function

Requirements from chapter 5 from EN 4709-002:2023.

The DRI function is provided by the [Dronetag DRI Module](https://dronetag.com/products/dri/).

## 5.3 Broadcast Transport Protocols

- [x] 5.3.2 Bluetooth legacy advertising transport mechanism (4.x compatible)
- [x] 5.3.3 Bluetooth long range advertising mechanism (5.x compatible)
- [ ] 5.3.4 Wi-Fi NAN transport method
- [ ] 5.3.5 Wi-Fi beacon transport method

!!! success

    The Dronetag DRI Module broadcasts the DRI messages using both Bluetooth 4.0 Legacy and Bluetooth 5.0 Long Range.

## 5.5 Emission Directivity

To allow its detection in any direction within the broadcasting range, the DRI broadcasted signal should
be emitted as omni-directionally as possible considering the drone and antenna(s) design limitations.

!!! success

    The DRI module comes with an [omni-directional antenna](https://shop.dronetag.com/products/61-bluetooth-wire-antenna.html),
    mounted on the bottom side of the drone behind a plastic cover.
    It has been tested for distances up to 100m, regardless of the orientation of the drone.

## 5.6 Update and Transmission Rates

For all broadcast transport protocols, the transmission rate shall be as follows:

- dynamic messages (as indicated in the block message section) shall be sent at least every one second;
- static messages (as indicated in the block message section) shall be sent at least every three seconds;
- maximum data age: the maximum potential time elapsed since the time of applicability of the
  dynamic fields in the location/vector message shall be no older than one second;

!!! success

    Both static and dynamic messages are broadcast twice per second.

The conformity to this requirement shall be proven by testing as described in 6.3.
