from netmiko import ConnectHandler
import getpass
import time

print('Banner')
config = input('Enter config file name : ')
device_list = input('Enter Device name seperated by "," : ')
device_list = list(device_list.split(','))
username =  input('Login as : ')
password =  getpass.getpass('password : ')
print(device_list)
time.sleep(1)
for devices in device_list:
     
    connect = ConnectHandler(device_type='juniper',ip=devices,username=username,password=password,port=22)
    connect.find_prompt()
    time.sleep(1)
    print('Connect Successfully')
    connect.config_mode()
    with open (config, 'r') as f:
        command=f.read().splitlines()
    for line in command:
        print(line)
        connect.send_config_set(line)
        connect.exit_config_mode()
    print(connect.send_command('show | compare'))
    x = input('Proceed to commit(Y or N) : ')
    if x == 'Y':
        print ('Commiting')
        connect.commit()
        connect.exit_config_mode()
        time.sleep(1)
        connect.disconnect()
    else:
        connect.disconnect()
print ('Completed Successfully!!')
