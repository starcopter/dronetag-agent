# Skynode

Along with the Skynode you are configuring, you will need:

- a power supply for the Skynode
- a laptop with [Auterion Mission Control][auterion-mission-control] installed
- a way to connect the Skynode to the laptop (WiFi or USB-C)
- an SSH client on the laptop (should be included even on Windows)

[auterion-mission-control]: https://auterion.com/product/mission-control/

## Preparation

Power the Skynode and connect it to the laptop.

!!! note

    The default WiFi network name is `skynode-<serial-number>` (AOS 3.5.13 and lower) or just `skynode` (AOS 3.7.9 and higher),
    with the password `1234567890`.

You should now be able to access the Skynode's web interface. The IP address depends on the connection method:

| Connection | WiFi          | USB-C         |
| ---------- | ------------- | ------------- |
| IP Address | [10.41.0.1][] | [10.41.1.1][] |

[10.41.0.1]: http://10.41.0.1/
[10.41.1.1]: http://10.41.1.1/

## PX4 Configuration

Open Auterion Mission Control. When the Skynode is connected properly to your laptop, AMC will automatically detect it.
Enter [Advanced Mode][amc-advanced-mode] and navigate to the **Advanced** --> **Parameters** tab.

!!! note

    If AMC is asking for a password to enter advanced mode, try `starcopter` or `mountain`.

[amc-advanced-mode]: https://docs.auterion.com/hardware-integration/flight-controller-customization/amcs-advanced-mode#enable-advanced-mode-in-amc

Ensure the following parameters are configured correctly:

| Parameter          | Value         |
| ------------------ | ------------- |
| `MAV_0_CONFIG`     | TELEM1        |
| `MAV_0_FLOW_CTRL`  | Auto-detected |
| `MAV_0_FORWARD`    | Enabled       |
| `MAV_0_MODE`       | Normal        |
| `MAV_0_RADIO_CTRL` | Disabled      |
| `MAV_0_RATE`       | 1200 B/s      |
| `MAV_S_FORWARD`    | Enabled       |
| `SER_TEL1_BAUD`    | 115200 8N1    |

## AuterionOS Configuration

!!! warning "Attention"
    This step needs to be repeated every time AuterionOS is up- or downgraded!

With the Skynode still connected to your laptop, open a terminal window and SSH into the Skynode.
As described [above](#preparation), the IP address depends on the connection method.

The password should be either `auterion` (default), or `catfish`.

```shell
$ ssh root@10.41.0.1
root@10.41.0.1's password:
Last login: Fri Dec 20 15:55:10 2024 from 10.41.0.2

    /\        | |          (_)
   /  \  _   _| |_ ___ _ __ _  ___  _ __
  / /\ \| | | | __/ _ \ '__| |/ _ \| '_ \
 / ____ \ |_| | ||  __/ |  | | (_) | | | |
/_/    \_\__,_|\__\___|_|  |_|\___/|_| |_|


Hello, Big Blue Sky!
      IP: 172.19.0.1 172.18.0.1 192.168.144.25 10.0.0.1 10.41.10.1 10.41.0.1
    UUID: 117339353
 FC UUID: uid2:000200000000393037363138510d0025001c
root@skynode-117339353:~#
```

Once logged in, deactivate Auterion's own Remote ID agent to prevent it from interfering with the DRI module:

```shell
$ mountrw  # to mount the root filesystem in read-write mode
$ systemctl disable remoteid-agent --now
Removed /etc/systemd/system/multi-user.target.wants/remoteid-agent.service.
$ mountro  # mount root filesystem in read-only mode
```

As this modification is made on the root filesystem, it is not persistent across AuterionOS upgrades.
It therefore has to be repeated after each software update!
The [AuterionOS Documentation][auterion-os-docs] has more information on the subject.

[auterion-os-docs]: https://docs.auterion.com/hardware-integration/auterionos-system-guide/filesystem-and-partitions#auterionos-partitions

### Change Password

If the password is still `auterion`, please change it, as that is [publicly documented][aos-password].

!!! note

    Use the password `catfish` for now.
    Yes, I know that's not very secure.

```shell
root@skynode-117339353:~# mountrw
root@skynode-117339353:~# passwd
New password:
Retype new password:
passwd: password updated successfully
root@skynode-117339353:~# mountro
```

[aos-password]: https://docs.auterion.com/hardware-integration/auterionos-system-guide/filesystem-and-partitions#change-root-auterion-user-password

## Next Steps

The Skynode is now configured.
Reboot it to make sure all the changes take effect, and continue to installing the [Dronetag Agent](dronetag-agent.md).
