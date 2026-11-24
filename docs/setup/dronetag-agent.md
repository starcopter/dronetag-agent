# Dronetag Agent

With both the DRI module and the Skynode configured, all that's left is to install the Dronetag Agent application.

For this you'll need:

- the [prepared](skynode.md) Skynode with a way to power it
- a way to connect to the Skynode (WiFi or USB-C)
- access to the [:simple-github: starcopter/dronetag-agent][dronetag-agent-repo] repository
- a laptop

## Download

The Dronetag Agent application is released with a GitHub Action workflow.
The latest release (`.auterionos` file) can be downloaded from the [Releases Page][dronetag-agent-releases].

## Install

Open the AuterionOS web interface in your browser ([10.41.0.1](http://10.41.0.1/) for WiFi, [10.41.1.1](http://10.41.1.1/) for USB-C).
In the **Install Software** section, select the `.auterionos` file you downloaded and click **Upload**.

!!! note

    If AuterionOS is asking for a password, try `starcopter` or `mountain`.

![Install Software Section](img/auterion-os-install-software.png)

Wait for the installation to complete, then click on the **Apps** tab in the left sidebar.
You should see the Dronetag Agent in the list of installed user applications.

![Installed Dronetag Agent](img/auterion-os-installed-dronetag-agent.png)

## Vehicle serial

The app reads the UAS serial from `/persistent/suite/vehicle_sn` when it starts.
The UI shows "Not set" until that file exists. Restart the app after the file is written.

Older releases mounted `vehicle_sn` itself. When the file was not on the Skynode yet, Docker created a directory at that path, and the serial file could not replace it.
Over SSH:

```shell
ls -ld /persistent/suite/vehicle_sn
```

Stop the app when that path is a directory. If the directory is empty, remove it, then write the serial file (one line, the ANSI/CTA-2063-A serial) before starting the app again:

```shell
rmdir /persistent/suite/vehicle_sn
```

Install the updated app and open the UI. The UAS ID line shows the serial.

## Verify

Click the blue **Dronetag Agent >** button to open the application user interface.
If you see the following, the Dronetag Agent is working correctly:

![Dronetag Agent](img/dronetag-agent-web-ui-fresh-install.png)

[dronetag-agent-releases]: https://github.com/starcopter/dronetag-agent/releases/latest
[dronetag-agent-repo]: https://github.com/starcopter/dronetag-agent
