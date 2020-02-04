import csv
from netmiko import ConnectHandler
import getpass
#import smtplib
#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart
#from email.mime.base import MIMEBase
#from email import encoders
USERNAME = raw_input("login as: ")
PASSWORD = getpass.getpass("Login_password: ")

#Sender_Email = '$senderemail@abc.com'
#Receiver_Email = '$receiveremail@abc.com'
#subject = 'Xlate Counters Report'

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
    try:
        print('Connecting to ' + str(DICT))
        net_connect = ConnectHandler(device_type='cisco_asa', ip=DICT, username=USERNAME, password=PASSWORD, port=22)
        net_connect.enable()
        print("connection successfull to " + DICT)
        #check = net_connect.send_command('show xlate | i used').strip()
        #print(check)
        #mail = 'current connection : '+str(check.split(' ')[0].strip())+' Clearing...'
        #print (mail)
        #if int(check.split(' ')[0].strip()) > 0:
        cmd = ("clear xlate")
        output = net_connect.send_command_timing(cmd, strip_command=False, strip_prompt=False)
        if "confirm" in output:
            output += net_connect.send_command_timing("\n", strip_command=False, strip_prompt=False)
        else:
            output += net_connect.send_command_timing("YES", strip_command=False, strip_prompt=False)
            #try:
                #msg = MIMEMultipart()
                #msg['From'] = Sender_Email
                #msg['To'] = Receiver_Email
                #msg['Subject'] = subject
                #body = (mail)
                #msg.attach(MIMEText(body,'plain'))
                #text = msg.as_string()
                #Serder_server = smtplib.SMTP('$mailserver', $port)
                #Serder_server.starttls()
                #Serder_server.login(Sender_Email,'$password')
                #print('through')
                #Serder_server.sendmail(Sender_Email,Receiver_Email,msg.as_string())
                #Serder_server.quit()
                #print('completed')
            #except:
                    #print('SMTP ERROR')

    except:
        print('connection is not successful To device : ' + str(DICT))
raw_input('Operation Completed!!!')
