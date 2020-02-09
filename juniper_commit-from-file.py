from netmiko import ConnectHandler
import getpass
from datetime import datetime
import time
start_time = datetime.now()
print('Banner')
config = raw_input(str('Enter config file name :  '))
device_list = raw_input(str('Enter Device name seperated by "," : '))
device_list = list(device_list.split(','))
username =  raw_input('Login as : ')
password =  getpass.getpass('password : ')
print(device_list)
time.sleep(1)
for devices in device_list:
    connect = ConnectHandler(device_type='juniper',ip=devices,username=username,password=password,port=22,global_delay_factor=2)
    connect.find_prompt()
    time.sleep(1)
    print('Connect Successfully')
    connect.config_mode()
    connect.send_config_from_file(config)
    print(connect.send_config_set('show | compare'))
    print(connect.send_config_set('commit check'))
    x = raw_input(str('Proceed to commit(Y or N) : '))
    if x == 'Y':
        print ('Commiting')
        connect.send_config_set('commit')
        connect.exit_config_mode()
        connect.disconnect()
    else:
        connect.disconnect()
end_time = datetime.now()
print("Total time: {}".format(end_time - start_time))
print ('Completed Successfully!!')
