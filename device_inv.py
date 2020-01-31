import csv
from netmiko import ConnectHandler
import getpass

USERNAME = raw_input("login as: ")
PASSWORD = getpass.getpass("Login_password: ")

with open('Device-List.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    TOTAL_LIST = []
    for row in reader:
        for line in row:
            TOTAL_LIST.append(line)
print(TOTAL_LIST)

raw_input('\n''TASK LIST HAS BBEN PREPARED , Press any key to connect the listed device and get the output ')
for DICT in TOTAL_LIST:
    Header = ('Hostname,Model,IOS,serial')
    Capture = open('OUTPUT.txt', 'a')
    Capture.write(Header + '\n')
    try:
        print('Connecting to ' + str(DICT))
        net_connect = ConnectHandler(device_type='cisco_ios', ip=DICT, username=USERNAME, password=PASSWORD, port=22)
        net_connect.enable()
        print("connection successfull to " + DICT)
        hostname = net_connect.find_prompt().replace('>','')
        model = net_connect.send_command("show inventory | i SN:").strip()
        version = net_connect.send_command("show version | i Version").strip()
        description = net_connect.send_command("show int description | ex down|Vl|Po").strip()
        cdpinfo = net_connect.send_command("show ip arp").strip()
        for line in model.splitlines():
            if 'SN:' in line:
                model = line.split()[1].strip()
                serial = line.split()[-1].strip()
                break
        for line in version.splitlines():
            if 'Version' in line:
                version = line.split(',')[2].strip()
                break
        Capture.write(hostname +','+ model + ','+ version+ ','+serial+'\n'+'\n')
        Capture.write(description + '\n'+'\n')
        Capture.write(cdpinfo + '\n'+'\n')


    except:
        print('connection is not successful To device : ' + str(DICT))
        ERROR = ('connection is not successful To device : ' + str(DICT))
        Capture.write(ERROR + '\n' + '\n')

raw_input('Operation Completed!!!')
