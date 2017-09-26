# Dependencies #

Our preferred development environment in Ubuntu 14.04 LTS.
We didn't test it in another linux. We recommend using our docker container (see [Ethanol Development container](https://github.com/h3dema/ethanol_devel)).
If you use the container all downloading and configure is made by the docker build process.

Some python modules are needed to run ethanol.
To install them.

```bash
apt-get -y update
apt-get -y upgrade
apt-get -y install python-setuptools python-pip python-dev
apt-get -y install python-numpy python-scipy python-matplotlib python-networkx ipython
pip install --upgrade pip 

cd /tmp
wget -c https://pypi.python.org/packages/source/c/construct/construct-2.5.2.tar.gz
tar zxvf construct-2.5.2.tar.gz
cd construct-2.5.2
sudo ./setup.py install

apt-get install -y python-epydoc
```

# Running #

To run you should install e update the modules -- see [README Installation](https://github.com/h3dema/ethanol_controller/blob/master/README.md).
The following command starts POX with two modules:
* an L2 learning switch
* an Ethanol controller

```bash
cd pox
./pox.py forwarding.l2_learning ethanol.server
```

To run the Ethanol module you need the SSL certificate. You can create your own or use ours. Our certificate is in the ethanol hostapd repository. Go to [its certificate directory](https://github.com/h3dema/ethanol_hostapd/tree/master/certificate) to see the file.

Ethanol controller by its own does nothing, only receives Hello messages from clients (APs).

# More info #

See more information in [ethanol/ssl_message/README.MD.](https://github.com/h3dema/ethanol_controller/blob/master/ethanol/ssl_message/README.MD)
