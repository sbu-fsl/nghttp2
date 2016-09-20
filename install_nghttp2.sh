#!/bin/bash -
#=============================================================================

set -o nounset                          # treat unset variables as an error
set -o errexit                          # stop script if command fail

export PATH=$PATH:/usr/local/lib:/usr/lib:/usr/lib64
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
export PYTHONPATH=/usr/local/lib64/python2.7/site-packages/

yum install -y pkgconfig
yum install -y CUnit-devel
yum install -y openssl-devel
yum install -y libev-devel
yum install -y zlib-devel
yum install -y libxml2-devel
yum install -y jemalloc-devel
yum install -y boost-devel
yum install -y boost-filesystem
yum install -y boost-thread
yum install -y python-devel
yum install -y ruby
yum install -y libwbclient-devel
yum install -y libcap-devel
yum install -y libblkid-devel

if [ ! -e deps ]; then
	mkdir deps
fi
cd deps

#install spdylay
if [ ! -e spdylay ]; then
	echo "fetching spdylay from git\n"
	git clone https://github.com/tatsuhiro-t/spdylay.git
	cd spdylay
	autoreconf -i
	automake
	autoconf
	./configure
	make
	make install
	cd ..
fi

#install jansson
if [ ! -e jansson-2.8 ]; then
	echo "downloading jansson-2.8\n"
	wget http://www.digip.org/jansson/releases/jansson-2.8.tar.bz2
	bunzip2 -c jansson-2.8.tar.bz2 | tar xf -
	cd jansson-2.8
	./configure
	make
	make install
	cd ..
fi

#install libevent
if [ ! -e libevent-2.0.22-stable ]; then
        echo "downloading libevent-2.0.22-stable\n"
	wget http://downloads.sourceforge.net/levent/libevent-2.0.22-stable.tar.gz
	tar -xvzf libevent-2.0.22-stable.tar.gz
	cd libevent-2.0.22-stable
	./configure --prefix=/usr --disable-static
	make
	make verify
	make install
	cd ..
fi

cd ..

#updating submodules for --with-mruby option
cd third-party
if [ ! -e mruby ]; then
	rm -rf mruby
fi
if [ ! -e neverbleed ]; then
        rm -rf neverbleed
fi
cd ..

git submodule update --init

#now install nghttp2
autoreconf -i
automake
autoconf
./configure --with-spdylay --enable-app --with-mruby --with-neverbleed
make
make install
echo "Successfully installed nghttp2\n"
