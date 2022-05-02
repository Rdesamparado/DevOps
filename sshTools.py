# sshools.py version for Ansible Tower

import sys
import paramiko
import time
from sshTools_Class import Device, Servicenowinfo, Robloxinfo, Cumulusinfo, Avocentinfo
from sshTools_Cmd import choice


def Info_(d_node):
    Vendor_List = ['Raritan Computer', 'Servertech', 'Arista', 'Avocent']
    #Inventory = ["DCS-7050TX2-128-R","210-AEDQ"]
    if 'Arista' in Vendor_List:
        print('-' * 110)
        print("This is a %s %s Device for %s" %
              (d_node.manu, d_node.device_type, d_node.project))
        print("SN: %s | App_Name: %s | Model: %s | Customer: %s" %
              (d_node.serial, d_node.app_name, d_node.model, d_node.customer))
        print("ip: %s | Login: %s | PW: %s" %
              (d_node.node_ip, str(d_node.user), str(d_node.pw)))
        print("\n\033[36m   Usage:\033[0m")
        if "Servertech" in d_node.manu:
            print(Robloxinfo())
        elif "Raritan Computer" in d_node.manu or "Raritan" in d_node.manu:
            print(Servicenowinfo())
        elif "Gelu" in d_node.manu:
            print(Servicenowinfo())
        elif "210-AEDQ" in d_node.model:
            print(Cumulusinfo())
        elif "DCS-7050TX2-128-R" in d_node.model:
            print(Robloxinfo())
        elif "Avocent" in d_node.manu:
            print(Avocentinfo())
        else:
            print('')
    else:
        print("Model Device not available in system.")
        sys.exit(0)
    choice(d_node)


if __name__ == '__main__':
    len_argv = len(sys.argv)
    if len_argv <= 1:
        print('\n')
        print("<Node ID> must be entered as an argument.")
        print('\n')
    elif len_argv == 2:
        m_nodes = sys.argv[1]
        sesh = paramiko.SSHClient()
        sesh.load_system_host_keys()
        sesh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sesh.connect('10.10.64.11', 22, 'rdesamparado', 'Tyler/34')
        channel = sesh.invoke_shell()
        time.sleep(1)
        channel.send('sudo -i\n')
        time.sleep(1)
        channel.send('Tyler/34\n')
        time.sleep(1)
        cmd1 = ('py sshTools_art.py {} | tee sshToolsobj.txt\n'.format(m_nodes))
        channel.send(cmd1)
        time.sleep(2)
        channel.close()
        cmd2 = 'cat /root/fs/sshToolsobj.txt'
        stdin, stdout, stderr = sesh.exec_command(cmd2)
        output = stdout.read().decode('utf-8')
        time.sleep(5)
        #print (output)
        node_id = output.split()[0]
        serial = output.split()[1]
        model = output.split()[2]
        customer = output.split()[3]
        device_type = output.split()[4]
        app_name = output.split()[5]
        node_ip = output.split()[6]
        project = output.split()[7]
        manu = output.split()[8]
    else:
        print('\n')
        print("<Node ID> must be entered as an argument.")
        print('\n')

    d_node = Device(node_id, serial, manu, model, customer,
                    device_type, app_name, node_ip, project)
    #d_node = (x.decode('utf-8')for x in str(d_node_.user,d_node_.pw,d_node_.node_ip))
    Info_(d_node)
