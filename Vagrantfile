# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # http://www.vagrantbox.es/
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/precise/current/precise-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.box = "precise-server-cloudimg-amd64-vagrant-disk1"

  config.vm.network "forwarded_port", guest: 22, host: 2223
  config.vm.network "private_network", ip: "192.168.33.08"

end