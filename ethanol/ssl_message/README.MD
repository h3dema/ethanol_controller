# Important information #

When msg_server.py starts running, it looks for a SSL certificate in the path defined by SSL_CERTIFICATE. This certificate is in https://github.com/h3dema/ethanol_hostapd repository. You should copy or link this file, otherwise this module will give you an error.

# Requires

All ssl_modules use python construct (https://pypi.python.org/pypi/construct).
To install this module:

```
wget -c https://pypi.python.org/packages/source/c/construct/construct-2.5.2.tar.gz
tar zxvf construct-2.5.2.tar.gz
cd construct-2.5.2
sudo ./setup.py install
```

# Update Python to 2.7.9+

If you are using Ubuntu 14.04 LTS, maybe it cannot update to 2.7.9 by its own.
you will need to insert a PPA repository.
type the following commands:

```
sudo add-apt-repository -y ppa:jonathonf/python-2.7
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install python2.7
```
