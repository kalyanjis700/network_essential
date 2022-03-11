# from crypt import methods
# from shutil import register_unpack_format
import xlrd
import requests
import json
from flask import Flask, render_template,request
from pysnmp.hlapi import *
# from urllib3 import Retry
from netmiko import ConnectHandler
from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_dispatcher import ConnectHandler
import subprocess
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home')
def homeretrun():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/result', methods = ["POST", "GET"])

def result():
    iprow = 0
    ipcol = 1
    hocol = 0
    deviceipa = "NO MATCH FOUND"
    output = "NO SUCCESS ON SNMPWALK"
    vendor = "NA"
    serialno = "NA"
    hostname = "NO MATCH FOUND"
    model ="NA"
    snmpcommunity = "indranil"
    result = request.form.to_dict()
    deviceip = result['devicename']
    if deviceip == "":
        display = 15
    else:
        #try:
            #errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),CommunityData(snmpcommunity, mpModel=0),UdpTransportTarget((deviceip, 161)),ContextData(),ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))))
            #for varBind in varBinds:
                #output = (varBind[1])
        #except:
            #output = "NO SUCCESS ON SNMPWALK"

        filelocation = ("Device_Inventory.xlsx")
        workbook = xlrd.open_workbook(filelocation)
        worksheet = workbook.sheet_by_index(0)
        nrows = worksheet.nrows
        if "." in deviceip:
            for row in range (0,nrows):
                if deviceip in worksheet.cell_value(row, ipcol):
                    deviceipa = worksheet.cell_value(row, 1)
                    vendor = worksheet.cell_value(row, 2)
                    serialno = worksheet.cell_value(row, 5)
                    hostname = worksheet.cell_value(row, 0) 
                    model = worksheet.cell_value(row, 4) 

        else:
            for row in range (0,nrows):
                if deviceip in worksheet.cell_value(row, hocol):
                    deviceipa = worksheet.cell_value(row, 1)
                    vendor = worksheet.cell_value(row, 2)
                    serialno = worksheet.cell_value(row, 5)
                    hostname = worksheet.cell_value(row, 0) 
                    model = worksheet.cell_value(row, 4) 

        #display = [deviceipa, vendor, serialno, hostname, model, deviceip, output]
        display = [deviceipa, vendor, serialno, hostname, model, deviceip]
    return render_template('inventory.html', result= display)
@app.route('/invresult', methods = ["POST", "GET"])
def invresult():
        devicetypecol = 6
        devicecount = 0
        invresult = request.form.to_dict()
        devicetype = invresult['devicetype']
        filelocation = ("Device_Inventory.xlsx")
        workbook = xlrd.open_workbook(filelocation)
        worksheet = workbook.sheet_by_index(0)
        nrows = worksheet.nrows
        itemname=[]
        for row in range (0,nrows):
            if devicetype in worksheet.cell_value(row, devicetypecol):
                devicecount = devicecount+1
                itemname.append(worksheet.cell_value(row, 0))
        invresultout = [devicetype, devicecount,itemname]
        return render_template('inventory.html', invcount= invresultout )

@app.route('/liveresult', methods = ["POST", "GET"])
def liveresult():
    inputitems = request.form.to_dict()
    devicename = inputitems['Devicename']
    username = inputitems['Username']
    password = inputitems['password']
    action = inputitems['commands']
    foutput = []
    devicecount = len(inputitems['Devicename'].split(","))
    hostnames = inputitems['Devicename'].split(",")
    for i in range (0,devicecount):
        hostname = hostnames[i]
        try:
            remote_device = {'device_type': 'autodetect','host': hostname,'username': username,'password': password}
            guesser = SSHDetect(**remote_device)
            vendor = guesser.autodetect()
        except:
            vendor = "NULL"
        if "cisco_asa" in vendor:
            remote_device['device_type'] = vendor
            net_connect = ConnectHandler(**remote_device)
            if action == "Check Version":
                output = net_connect.send_command("show version")
                foutput.append("===========================" '\n' + "Version Details for " + hostname + ": " '\n'+ "==========================="'\n'+ output)
            elif action == "Check Inventory":
                output = net_connect.send_command("show inventory")
                foutput.append("===========================" '\n' + "inventory For " + hostname + ": " '\n'+ "==========================="'\n'+ output)
            elif action == "Interface Status":
                output = net_connect.send_command("show ip")
                foutput.append("===========================" '\n' + "Interface status For "+ hostname + ": " '\n'+ "==========================="'\n'+ output)
            elif action == "CDP Status":
                output = net_connect.send_command("sh cdp neighbors")
                foutput.append("===========================" '\n' + "Neighbor status For "+ hostname + ": " '\n'+ "==========================="'\n'+ 'CDP/LLDP not supported by ASA')
        elif "cisco" in vendor:
            remote_device['device_type'] = vendor
            net_connect = ConnectHandler(**remote_device)
            if action == "Check Version":
                output = net_connect.send_command("show version")
                foutput.append("===========================" '\n' + "Version Details for " + hostname + ": " '\n'+ "==========================="'\n'+ output)
            elif action == "Check Inventory":
                output = net_connect.send_command("show inventory")
                foutput.append("===========================" '\n' + "inventory For " + hostname + ": " '\n'+ "==========================="'\n'+ output)
            elif action == "Interface Status":
                output = net_connect.send_command("show interface status")
                foutput.append("===========================" '\n' + "Interface status For "+ hostname + ": " '\n'+ "==========================="'\n'+ output)
            elif action == "CDP Status":
                output = net_connect.send_command("sh cdp neighbors")
                foutput.append("===========================" '\n' + "Neighbor status For "+ hostname + ": " '\n'+ "==========================="'\n'+ output)
        elif "junos" in vendor:
            remote_device['device_type'] = vendor
            net_connect = ConnectHandler(**remote_device)
            if action == "Check Version":
                output = net_connect.send_command("show version")
                foutput.append("===========================" '\n' + "Version Details for " + hostname + ": " '\n'+ "==========================="'\n'+ output)
            elif action == "Check Inventory":
                output = net_connect.send_command("show chassis hardware detail")
                foutput.append("===========================" '\n' + "inventory For " + hostname + ": " '\n'+ "==========================="'\n'+ output)
            elif action == "Interface Status":
                output = net_connect.send_command("show interfaces terse")
                foutput.append("===========================" '\n' + "Interface status For "+ hostname + ": " '\n'+ "==========================="'\n'+ output)
            elif action == "CDP Status":
                output = net_connect.send_command("sh lldp neighbors")
                foutput.append("===========================" '\n' + "Neighbor status For "+ hostname + ": " '\n'+ "==========================="'\n'+ output)
        elif "linux" in vendor:
            remote_device['device_type'] = vendor
            net_connect = ConnectHandler(**remote_device)
            if action == "Check Version":
                output = net_connect.send_command("tmsh show sys version")
                foutput.append("===========================" '\n' + "Version Details for " + hostname + ": " '\n'+ "==========================="'\n'+ output)
            elif action == "Check Inventory":
                output = net_connect.send_command("tmsh show sys hardware")
                foutput.append("===========================" '\n' + "inventory For " + hostname + ": " '\n'+ "==========================="'\n'+ output)
            elif action == "Interface Status":
                output = net_connect.send_command("tmsh show sys ip-address")
                foutput.append("===========================" '\n' + "Interface IP status For "+ hostname + ": " '\n'+ "==========================="'\n'+ output)
            elif action == "CDP Status":
                #output = net_connect.send_command("sh lldp neighbors")
                foutput.append("===========================" '\n' + "Neighbor status For "+ hostname + ": " '\n'+ "==========================="'\n'+ 'CDP/LLDP not supported by F5')
        else:
            foutput.append('\n'+"Details for " + hostname + ": " + "Login not possible to the device")
@app.route('/livef5result', methods = ["POST", "GET"])
def livef5result():
    inputitems = request.form.to_dict()
    devicename = inputitems['Devicename']
    action = inputitems['commandsf5']
    if action == "List node configuration":
        url = 'https://'+ devicename + '/mgmt/tm/ltm/node'
        payload = ""
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Basic eHNBRENyb0FQSTo5YmpzWDFOYklEVzZZVWphakR0cjdPaWkx',
          'Cookie': 'BIGIPAuthCookie=KVedellW3Cgjdqvw2tnY6LJ4uxnYgnA5ilZKr078; BIGIPAuthUsernameCookie=xsADCroAPI'
        }
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    
    return render_template('inventory.html', livef5result= response.json())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port= '8080', debug=True , threaded=True)
