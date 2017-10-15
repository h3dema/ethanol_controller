# Ethanol controller
This repository contains the Ethanol controller. It is in Python 2. 7, and runs as a POX (dart) module.

We have developed a docker container that allows the compilation and development of ethanol agents. This is the method we recommend for you to compile (and change) Ethanol. The container already makes the clone of this repository (ethanol_controller). To see more go to [ethanol_devel](https://github.com/h3dema/ethanol_devel).

# Installation #

Clone the repository and update submodules
```bash
cd /home/ethanol
git clone https://github.com/h3dema/ethanol_devel.git
cd ethanol_devel
bash configure.sh
```

# Requisites #

Read [ethanol/README.MD](https://github.com/h3dema/ethanol_controller/blob/master/ethanol/README.MD)

# Template #

Inside **template** directory, you find a sample file, showing how to create a simple module in python that uses Ethanol's resources.

# More info #

See more information in [ethanol/ssl_message/README.MD.](https://github.com/h3dema/ethanol_controller/blob/master/ethanol/ssl_message/README.MD)


# Connection #

The figure below shows a terminal emulator with two open cones: (right) a connection to the computer running ethanol_hostapd and (left) a connection to the Ethanol controller.
It is important to note that in the controller (left), we can activate different logging level using the ** log.level --LEVEL ** (in the figure we show DEBUG).
Ethanol controller initialization process begins with the registration of the Ethanol module in the POX, followed by the initialization of a local server to receive the messages from the clients. In our example, the Ethanol server starts on port 22222 (default).
We see next that the protocol OpenFlow also begins to execute, creating a port of connection in 6633 (default port).

In the right part of the figure we see hostapd loading. Ethanol checks to see if the /etc/ethanol.ini configuration file exists, and if it exists it is read. In our example, the file exists and enables Ethanol to work. Hostapd also creates an Ethanol server on port 22222 (default port) to receive controller commands.
A Hello message is periodically sent to the controller. The first connection serves to pass additional information from the AP to the controller and in the others it acts as a signal informing that hostapd is active.

![alt text](https://github.com/h3dema/ethanol_controller/blob/master/connection.png "Connection Example")

We can see that on the first connection of the AP to the controller, the controller requests additional information represented by the MSG_GET_RADIO_WLANS and MSG_GET_AP_SSID messages shown on the lines below Connection ...
This information is important for popular class architecture objects. This creates an *ap*. This *ap* has *radio*s and *vap*s. *radio*s represent the physical radio devices on the device, while *vap*s are the configured SSIDs.
