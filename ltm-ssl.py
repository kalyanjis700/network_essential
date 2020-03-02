import csv
import getpass
import netmiko
import getpass
username = raw_input('login as :')
password = getpass.getpass('password :')

Devicelist = ['158.28.75.77','158.28.75.74']
with open('output.csv','w') as csvfile:
        writer=csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Device', 'Option'])

        for device in Devicelist:
                connection = netmiko.ConnectHandler(ip=device, device_type='f5_ltm',username=username,password=password,global_delay_factor=3)
                connection.send_command_timing ('modify cli preference pager disabled')
                print('connection successful')
                cmd =["list ltm virtual | grep 443"]

                print('working on : ' + str(cmd))
                outputvirtualserver  = connection.send_command_timing ("list ltm virtual | grep 443")
                output =outputvirtualserver.strip().splitlines()
                if "cougar.exxonmobil" in output[index]:
                    ltmv = output[index].replace('{','')
                else:
                          print('issue with ' + str(cmd))
                ltmcmd = 'list '+ str(ltmv)
                print('working on : ' + str(ltmcmd)
                couger = connection.send_command_timing (ltmcmd)
                output =couger.strip().splitlines()
                if "profiles" in output[index]:
                        profiles = output[index+1]
                        profile = profiles.replace('{','')
                else:
                      print('issue with ' + str(cmd))
                cmd = 'list ltm profile ' + str(profile) +' | grep options'
                print('working on : ' + str(cmd)
                options = connection.send_command_timing (cmd)
                output =options.strip().splitlines()
                if "options" in output[index]:
                        options = output[index+1]
                        option = options.replace('option {','')
                        option = option.replace('}','')

                        writer.writerow([device,option])

 print ('completed Successfully')
                        
