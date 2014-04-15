#!/bin/sh

# Script which installs mfold from source

install_mfold () {
    cd /tmp
    curl -O http://mfold.rna.albany.edu/download/mfold-3.6.tar.gz
    tar zxvf mfold-3.6.tar.gz
    cd mfold-3.6
    ./configure --prefix=/usr/local
    make all
    sudo make install
    sudo ln -s /usr/local/bin/* /usr/bin
}

if ! [ -f /usr/local/bin/mfold ]; then
    install_mfold
fi
