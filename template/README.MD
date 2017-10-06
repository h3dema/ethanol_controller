# Template module #


This module (sampleApp) is a template that is being provided as a guideline for creating Ethanol based controllers.
This Python code is a POX module and should be loaded on the command line along with the Ethanol server as shown in the line below.

To run this module:
1) link this diretory inside pox directory
```bash
ln -s ~/ethanol/ethanol_controller/template ~/ethanol/ethanol_controller/pox/pox/template
```

2) start the module with ethanol
```bash
cd ~/ethanol/ethanol_controller/pox
python pox.py ethanol.server template.sampleApp --ap_ip="<your AP's ip address here>"
```

Notice that you can pass parameters to your code in the command line, as shown in the line above.

SampleApp checks if ethanol is running,
if ethanol is running, this module can also run.
It checks and waits until a specified AP connects.
When it connects, the module prints a list of AP's already connected to the controller.

The most important part of the module is the function **launch()**. This is the entry point that must exists in all POX modules. When pox.py starts running, it calls **launch()** function in all its modules. So this functions loads all dependencies and starts all process.

# More Info #

If you want more information:

* about POX components, go to the [POX Wiki](https://openflow.stanford.edu/display/ONL/POX+Wiki).

* Ethanol: Software defined networking for 802.11 Wireless Networks [IM 2015](http://im2015.ieee-im.org/content/technical-sessions-0) [Paper](http://ieeexplore.ieee.org/document/7140315/)

* [Ethanol: uma plataforma SDN para redes wi-fi](http://www.bibliotecadigital.ufmg.br/dspace/handle/1843/ESBF-9ZPNXT)
 (In portuguese)