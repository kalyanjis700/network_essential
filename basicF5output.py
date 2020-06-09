import csv
import getpass
import netmiko
import getpass
username = raw_input('login as :')
password = getpass.getpass('password :')
Capture = open('OUTPUT.txt', 'a')
with open('Device-List.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    Devicelist =[]
    for row in reader:
        for line in row:
            Devicelist.append(line)
print(Devicelist)
for device in Devicelist:
    Capture.write('Device Name : ' + device + '\n')
    connection = netmiko.ConnectHandler(ip=device, device_type='f5_ltm',username=username,password=password,global_delay_factor=3)
    connection.send_command_timing ('modify cli preference pager disabled')
    print('connection successful')
    outputvirtualserver  = connection.send_command_timing ("list ltm virtual | grep 443")
    Capture.write( outputvirtualserver + '\n')
    
