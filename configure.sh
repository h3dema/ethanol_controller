MY_PATH=`pwd`

# update modules
git submodule update --remote --init

# create link
ln -sf "$MY_PATH/ethanol" "$MY_PATH/pox/pox/ethanol"
