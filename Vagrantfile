Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_check_update = false
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.synced_folder ".", "/opt/astroConverter"

  config.vm.provider "virtualbox" do |vb|
  vb.gui = true
    vb.memory = "1024"
  end
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y xorg openbox
    sudo apt-get install -y python3
    sudo apt-get install -y python3-pip
    sudo apt-get install -y python3-numpy
    sudo apt-get install -y python3-matplotlib
    sudo apt-get install -y python3-astropy
  SHELL
end
