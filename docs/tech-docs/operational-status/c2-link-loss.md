# Loss of C2 Link :construction:

When the C2 link is lost (here: rebooted Herelink), the `status` field in **OPEN_DRONE_ID_LOCATION (12901)** correctly
indicates the **Emergency** status.

The trace displayed below ([dashboard][grafana-mavlink-loss-of-c2]) shows a deliberate C2 link loss: the Herelink controller was rebooted.
At 19:15:04, the Herelink controller shut down, and the copter went into a failsafe mode and attempted to return to launch.
The ODID_LOCATION message correctly indicated the **Emergency** status.
After the RC connection was reestablished around 19:15:28, the copter _remained_ in emergency mode, since it was still executing
the failsafe action. At around 19:16:07, the flight mode was switched (back) to Altitude mode, which caused the failsafe action to be
aborted, and the status to return to **Airborne**.

![PX4 Emergency Status under Loss of C2](img/mavlink-loss-of-c2.png)

[grafana-mavlink-loss-of-c2]: https://grafana.starcopter.de/d/ae9v33evpjjswa/mavlink-snippets?orgId=1&from=1736878440000&to=1736878650000&var-datasource=Mig5CVbnk&var-bucket=mavlink&var-logger=All&var-session=All&var-system_id=1&var-component_id=1
