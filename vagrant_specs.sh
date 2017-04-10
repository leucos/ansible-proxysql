#!/bin/bash
#
# Vagrant provisionning script
#
# Usage for provisionning VM & running (in Vagrant file):
# 
# script.sh --install <role> <URL for test suite>
#
# e.g. : 
# script.sh --install ansible-nginx https://github.com/erasme/erasme-roles-specs.git
# 
# Usage for running only (from host):
#
# vagrant ssh -c ./specs
#
if [ "x$1" == "x--install" ]; then
  mv ~ubuntu/specs /usr/local/bin/specs
  chmod 755 /usr/local/bin/specs
  sudo apt-get install -qqy git make python
  su ubuntu -c 'git clone --depth 1 https://github.com/nickjj/rolespec'
  cd ~ubuntu/rolespec && make install
  su ubuntu -c 'rolespec -i ~/testdir'
  su ubuntu -c "ln -s /vagrant/ ~/testdir/roles/$2"
  su ubuntu -c "ln -s /vagrant/tests/$2/ ~/testdir/tests/"
  # su ubuntu -c "git clone $3 ~/testdir/tests"
  exit
fi

cd ~ubuntu/testdir && rolespec -r $(ls roles) "$*"
