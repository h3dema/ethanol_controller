#!/bin/bash
#
# generates the help (documentation) of ethanol controller module
# outputs a pdf file
#
# needs: epydoc
#
# install epydoc:
#
# opçao 1)
# apt-get install python-epydoc
#
# opcao 2)
#
# wget -q http://prdownloads.sourceforge.net/epydoc/epydoc-3.0.1.tar.gz
# gunzip epydoc-3.0.1.tar.gz
# tar -xvf epydoc-3.0.1.tar
# cd epydoc-3.0.1/
# make install
# make installdocs

epydoc --pdf  --graph all *
mv pdf/api.pdf documentation/api.pdf
rm -fr pdf
