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

![alt text](https://github.com/h3dema/ethanol_controller/blob/master/connection.png "Connection Example")
