MY_PATH="/home/ethanol/ethanol_controller/"
cd $MY_PATH

# update modules
git submodule update --remote --init

# create link
ln -s $MY_PATH/ethanol $MY_PATH/pox/pox/ethanol