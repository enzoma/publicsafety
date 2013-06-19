#!/bin/bash

rm -rf ~/cpd
cd ~
virtualenv -p python27 --no-site-packages cpd
cd -
source ~/cpd/bin/activate
pip install numpy
pip install scipy
pip install matplotlib
pip install gdal
pip install ipython
pip install scikit-learn
pip install pandas

