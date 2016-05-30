Vagrant.configure('2') do |config|
 config.vm.box = 'azure'
 config.vm.network "public_network"
 config.vm.network "private_network",ip: "192.168.56.10", virtualbox__intnet: "vboxnet0"
 config.vm.network "forwarded_port", guest: 80, host: 80
 config.vm.define "localhost" do |l|
    l.vm.hostname = "localhost"
  end



 config.vm.provider :azure do |azure, override|
 azure.mgmt_certificate = File.expand_path('~/.ssh/azurejuanfran.pem')
 azure.mgmt_endpoint = 'https://management.core.windows.net'
 azure.subscription_id = 'b187be6d-afae-40aa-9513-a3b91e07f3a3'
 azure.vm_image = 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150506-en-us-30GB'
 azure.vm_name = 'noinventory'
 azure.cloud_service_name = 'noinventory'
 azure.vm_password = 'Clave#Hugo#1'
 azure.vm_location = 'Central US'
 azure.ssh_port = '22'
 azure.tcp_endpoints = '80:80'
 end

 config.vm.provision "ansible" do |ansible|
    ansible.sudo = true
    ansible.playbook = "playbook.yml"
    ansible.verbose = "v"
    ansible.host_key_checking = false
  end

end
