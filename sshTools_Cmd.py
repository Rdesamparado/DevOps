import paramiko
import sys 
from sshTools_Class import Servicenowinfo, Robloxinfo, Cumulusinfo, Avocentinfo
import time
import ColorTerminalOutput

Terminal = ColorTerminalOutput
Rblxpdu4 = ("Configure Settings:")
Rblxpdu5 = ('Collect Logs:') 
Rblxpdu6 = ('Disabling DHCP:')
Rblxpdu7 = ('Restart Device to Factory Defaults:')
Snwpdu1 = ('Port Assignment:')
Snwpdu2 = ('Automate Configurations:')
Snwpdu3 = ('Collect Logs:')
Snwcmls8 = ('Automate Configurations:')
Snwcmls9 = ('Collect Logs:')
Snwcmls10 = ('Automate Post Snapshot Configurations:')
SnwRcon11 = ('Automate Configurations:')
SnwRcon12 = ('Collect Logs:')
SnwRcon13 = ('Factory_Defaults:')


def choice(d_node):
    print ('')
    print ("Type \"usage\" below to see usage again.")
    action = input("Type your Selection [Number] here: ")
    print ('')
    connect_(d_node,action)

def pduportassign(d_node):
    print ('PDU Port Assignment')
    Device_Fnder = d_node.app_name
    node_project = d_node.project
    node_ip_ = d_node.node_ip
    sesh = paramiko.SSHClient()
    sesh.load_system_host_keys()
    sesh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sesh.connect('10.10.64.11',22,'rdesamparado','Tyler/34')
    channel = sesh.invoke_shell()
    channel.send('sudo -i\n')
    time.sleep(1)
    channel.send('Tyler/34\n')
    time.sleep(1)
    if 'PDU-B1' in Device_Fnder:
        cmd = 'sudo python /home/chirag/fs_webtoolkit/PDUPORTASSIGN.py %s %s 1\n'%(node_project,node_ip_)
        print (cmd)
        'PDU Port Assign started for PDU-B1'
        channel.send(str(cmd))
        time.sleep(10)
        output = channel.recv(99999).decode('utf-8')
        print (output)
        choice(d_node)
    elif 'PDU-B2' in Device_Fnder:
        cmd = str('sudo python /home/chirag/fs_webtoolkit/PDUPORTASSIGN.py %s %s 2\n'%(node_project,node_ip_))
        print ('PDU Port Assign started for PDU-B2')
        print (cmd)
        channel.send(str(cmd))
        time.sleep(10)
        output = channel.recv(99999).decode('utf-8')
        print (output)
        choice(d_node)
    else:
        print ('Unable to execute port assignment.')
        choice(d_node)

def connect_(d_node,action):
    sesh = paramiko.SSHClient()
    sesh.load_system_host_keys()
    sesh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    node_ip_ = d_node.node_ip
    node_user = d_node.user
    node_pw = d_node.pw
    Dvice = d_node.manu
    Modelx = d_node.model
    print (d_node.node_id, ('SN:'),d_node.serial, Dvice, d_node.project)
    print (node_ip_,node_user,node_pw)
    print ('')

    if action == 'usage':
        if 'Servertech' in Dvice:
            print (Robloxinfo())
            choice(d_node)
        elif 'Raritan Computer' in Dvice or 'Raritan' in Dvice:    
            print (Servicenowinfo())
            choice(d_node)
        elif '210-AEDQ' in Modelx:
            print (Cumulusinfo())
            choice(d_node)
        elif 'Avocent' in Dvice:
            print (Avocentinfo())
            choice(d_node)
        else: 
            print ("Model not available in System")
            choice(d_node)

    elif action == '1' and 'Raritan Computer' in Dvice or action == '1' and 'Raritan' in Dvice:
        pduportassign(d_node)

    elif action == '1' and 'Raritan Computer' not in Dvice or action == '1' and 'Raritan' not in Dvice:
        print('\n')
        print ("\033[91m     Unable to execute pduportassign on this device.\033[0m")
        print('\n')
        choice(d_node)

    elif len(action) == 1 and action == '2' or action == '3':
        for x in node_user:
            node_user_1 = str(x).strip(str(['']))
        for x in node_pw:
            node_pw_1 = str(x).strip(str(['']))
        try:
            print ('You have selected &s' %(action))
            if action == '1':
                print (Snwpdu1)
            elif action == '2':
                print (Snwpdu2)
            elif action == '3':
                print (Snwpdu3)
        except:
            print ('')
        seshconnect = sesh.connect(d_node.node_ip, 22, node_user_1, node_pw_1)
        print (seshconnect)
        channel = sesh.invoke_shell()
        print ('')
        print ("\033[92m[Connection Made]\033[0m")
        print ('')
        time.sleep(3)
        Dvice = d_node.manu
        serial = d_node.serial
        print ('Device', str(Dvice), serial,('\n'))
        Snowmodel = ('Raritan')
        if Snowmodel not in str(Dvice): 
            print('\n')
            print ("\033[91m     Action selected is not available for this Device.\033[0m")
            print('\n')
            choice(d_node)
        
        if action == '2' and Snowmodel in str(Dvice):
            print ('')
            print ('Servicenow PDU Configuration')
            channel.send('config\n')
            time.sleep(2)
            channel.send('pdu name PDU-%s\n' %(serial))
            print ('PDU-Serial Naming')
            time.sleep(2)
            channel.send('network services snmp v1/v2c enable\n')
            time.sleep(1)
            channel.send('y\n')
            channel.send('\b\n')
            print ('Enabling SNMP')
            time.sleep(2)
            channel.send('network ipv4 interface ETH1 preferredHostName PDU-%s\n' %(serial))
            print ('Registering Hostname')
            time.sleep(1)
            channel.send('apply\n')
            time.sleep(2)
            channel.send('show pdu details\n')
            print ('Generating Validation Output')
            channel.send('\n')
            channel.send('show network services snmp\n')
            time.sleep(3)
            output = channel.recv(9999).decode('utf-8')
            print (output)
            time.sleep(3)
            print ('')
            choice(d_node)
        
        elif action == '3' and Snowmodel in str(Dvice):
            print ('')
            print ('Collecting Servicenow PDU Logs')
            print ('-'*110)
            time.sleep(3)
            channel.send('show pdu details\n')
            time.sleep(2)
            channel.send('show network services snmp\n')
            time.sleep(2)
            channel.send('show network\n')
            time.sleep(2)
            channel.send('show outlets\n')
            time.sleep(8)
            output = channel.recv(99999).decode('utf-8')
            print (output)
            print ('')
            choice(d_node)

    elif action == '4' or action == '5' or action == '6' or action == '7':
        for x in d_node.user:    
            node_user_1 = str(x).strip(str(['']))
        for x in d_node.pw:
            node_pw_1 = str(x).strip(str(['']))
        print ('You have selected %s' %(action))
        try:
            if action == '4':
                print (Rblxpdu4)
            if action == '5':
                print (Rblxpdu5)
            if action == '6':
                print (Rblxpdu6)
            if action == '7':
                print (Rblxpdu7)
        except:
            print ('')

        seshconnect = sesh.connect(d_node.node_ip, 22, node_user_1, node_pw_1)
        print (seshconnect)
        channel = sesh.invoke_shell()
        print ('')
        print ("\033[92mConnection Made\033[0m ")
        print ('')
        Dvice = d_node.manu
        time.sleep(3)
    
        if 'Servertech' not in Dvice:
            print('\n')
            print ("\033[91m     Action selected is unavailable for this Device.\033[0m ")
            print('\n')
            choice(d_node)
        
        elif action == '4' and 'Servertech' in Dvice:
            print ('\033[4mConfigure Settings:\033[0m')
            print ('')
            ip = input("Input IP Address: ")
            subnet = input("Input Subnet Mask: ")
            gateway = input("Input Gateway: ")
            banner = input("Input Banner & Location Name: ")
            channel.send('set ipv4 address\n')
            settings = [ip,subnet,gateway,banner]
            for line in settings:
                print (line.strip('\n'))
            Resp = input("Type 'yes' to continue? ").lower()

            try:
                if str(Resp) == 'yes' or str(Resp) == 'y':
                    print (settings)
                    print ("Setting ip, subnet & gateway")
                    time.sleep(1)
                    channel.send(ip + '\n')
                    time.sleep(1)
                    channel.send('set ipv4 subnet\n')
                    time.sleep(1)
                    channel.send(subnet + '\n')
                    time.sleep(1)
                    channel.send('set ipv4 gateway\n')
                    time.sleep(1) 
                    channel.send(gateway + '\n')
                    time.sleep(1)
                    print ('Setting FQDN and Location Name')
                    channel.send('set location\n')
                    time.sleep(1)
                    channel.send(banner + '\n')
                    time.sleep(1)
                    channel.send('set dhcp fqdn name\n')
                    time.sleep(1)
                    channel.send(banner + '\n')
                    time.sleep(1) 
                    channel.send('set snmp v2 enabled\n')
                    time.sleep(1)
                    channel.send('y\n')
                    time.sleep(1)
                    channel.send('set banner\n')
                    time.sleep(1)
                    channel.send(banner + '\n')
                    time.sleep(1)
                    channel.send('\x1a\n')
                    time.sleep(1)
                    channel.send('show system\n')
                    time.sleep(2)
                    channel.send('show units\n')
                    time.sleep(2)
                    channel.send('show network\n')
                    time.sleep(2)
                    channel.send('show outlets\n')
                    time.sleep(8)
                    output = channel.recv(99999).decode('utf-8')
                    print (output)
                    time.sleep(2)
                    restart = input("Type \"Yes\" to restart device to apply changes: ")
                    if restart == "Yes" or restart == 'yes' or restart == 'y':
                        channel.send('restart\n')
                        time.sleep(1)
                        print ('restart')
                        channel.send('y\n')
                        print ('yes')
                        time.sleep(4)
                        output = channel.recv(9999).decode('utf-8')
                        print (output)
                        print ('Device Restarted.')
                        choice(d_node)
                    elif restart == None:
                        print ('')
                        print ('No action was made.')
                        choice(d_node)
                    else:
                        print ('')
                        print ('No action was made.')
                        choice(d_node)
                else:
                    print ('')
                    print ('No action was made.')
                    choice(d_node)
            except:
                choice(d_node)

        elif action == '5':
            print ('Collecting Roblox PDU Logs')
            print ('-' * 100)
            channel.send('show system\n')
            time.sleep(2)
            channel.send('show units\n')
            time.sleep(2)
            channel.send('show network\n')
            time.sleep(2)
            channel.send('show outlets\n')
            time.sleep(8)
            output = channel.recv(99999).decode('utf-8')
            print (output)
            choice(d_node)

        elif action == '6' and 'Servertech' in Dvice:
            print ('Disabling DHCP')
            print ("Connection will be lost")
            channel.send('set dhcp disabled\n')
            time.sleep(1)
            print ('Restarting Device')
            channel.send('restart\n')
            time.sleep(1)
            conf = input('Type "yes" to continue:').lower()
            if conf == 'yes' or conf == 'y':
                channel.send('y\n')
                time.sleep(2)
                output = channel.recv(9999).decode('utf-8')
                print (output)
                choice(d_node)
            else:
                channel.send('n\n')
                print ('No action was made')
                choice(d_node)

        elif action == '7' and 'Servertech' in Dvice:
            print ('Restarting Device to Factory Defaults')
            channel.send('restart factory \n')
            conf = input("Type 'yes' to continue: ").lower()
            if conf == 'yes' or conf == 'y':
                channel.send('y\n')
                time.sleep(2)
                output = channel.recv(99999).decode('utf-8')
                print (output)
                choice(d_node)
            else:
                channel.send('n\n')
                print ('No action was made')
                choice(d_node)
        else:
            choice(d_node)

    elif action == '8' or action == '9' or action == '10':
        for x in node_user:
            node_user_1 = str(x).strip(str(['']))
        for x in node_pw:
            node_pw_1 = str(x).strip(str(['']))
        try:
            print ('You have selected &s' %(action))
            if action == '8':
                print (Snwcmls8)
            elif action == '9':
                print (Snwcmls9)
            elif action == '10':
                print (Snwcmls10)
        except:
            print ('')
        sesh.connect(d_node.node_ip, 22, node_user_1,node_pw_1)
        channel = sesh.invoke_shell()
        print ('')
        print ("\033[92mConnection Made\033[0m ")
        print ('')
        Dmodel = d_node.model
        time.sleep(3)

        if '210-AEDQ' not in Dmodel:
            print('\n')
            print ("\033[91m     Action selected is unavailable for this Device!\033[0m ")
            print('\n')
            choice(d_node)

        elif action == '8' and '210-AEDQ' in Dmodel:
            print ('\033[4m     Automate Configurations:\033[0m')
            channel.send('sudo cl-license-i\n')
            time.sleep(1)
            channel.send(node_pw_1 + '\n')
            time.sleep(3)
            channel.send('fabien.broquet@servicenow.com|4CtjMCACDi5ctakKPHDBMa+EfmOVAg4IIO33JXhBpDZSERL11Q\n')
            time.sleep(1)
            channel.send('net add interface swp1-52\n')
            time.sleep(1)
            channel.send('net add bridge bridge ports swp1-52\n')
            time.sleep(1)
            channel.send('net commit\n')
            time.sleep(1)
            channel.send('sudo ifreload -a\n')
            time.sleep(1)
            channel.send(node_pw_1 + '\n')
            time.sleep(3)
            channel.send('net add interface swp1-52 alias [DCS TEST]\n')
            time.sleep(1)
            channel.send('net commit\n')
            time.sleep(1)
            channel.send('sudo systemctl restart switchd\n')
            time.sleep(1)
            channel.send(node_pw_1 + '\n')
            time.sleep(3)
            channel.send('sudo adduser root sudo\n')
            time.sleep(1)
            channel.send(node_pw_1 + '\n')
            time.sleep(2)
            channel.send('sudo passwd root\n')
            time.sleep(2)
            channel.send(node_pw_1 + '\n')
            time.sleep(2)
            output = channel.recv(99999).decode('utf-8')
            
            print (output)
            choice(d_node)

        elif action == '9' and '210-AEDQ' in Dmodel:
            print ('Collecting Logs')
            channel.send('cat /etc/os-release\n')
            time.sleep(1)
            channel.send('decode-syseeprom\n')
            time.sleep(1)
            channel.send('cat /etc/network/interfaces\n')
            time.sleep(5)
            channel.send('sudo ethtool -m swp49 | grep -E "Vendor PN|Vendor SN"\n')
            time.sleep(1)
            channel.send(node_pw_1 + ('\n'))
            time.sleep(1)
            channel.send('sudo ethtool -m swp50 | grep -E "Vendor PN|Vendor SN"\n')
            time.sleep(1)

            channel.send('sudo ethtool -m swp51 | grep -E "Vendor PN|Vendor SN"\n')
            time.sleep(1)
            channel.send('sudo ethtool -m swp52 | grep -E "Vendor PN|Vendor SN"\n')
            time.sleep(1)
            output = channel.recv(99999).decode('utf-8')
            
            print (output)
            choice(d_node)
	
        elif action == '10' and '210-AEDQ' in Dmodel:
            print ('Automate Post Snapshot Configurations:')
            channel.send('net del all\n')
            time.sleep(1)
            channel.send('net commit\n')
            time.sleep(1)
            channel.send('sudo systemctl restart switchd\n')
            time.sleep(1)
            channel.send(node_pw_1 + '\n')
            time.sleep(3)
            channel.send('cat /etc/network/interfaces\n')
            time.sleep(5)
            channel.send('net add interface swp1-52 alias [DCS TEST]\n')
            time.sleep(1)
            channel.send('net commit\n')
            time.sleep(1)
            channel.send('sudo systemctl restart switchd\n')
            time.sleep(1)
            channel.send(node_pw_1 + '\n')
            time.sleep(3)
            channel.send('sudo adduser root sudo\n')
            time.sleep(1)
            channel.send(node_pw_1 + '\n')
            time.sleep(2)
            channel.send('sudo passwd root\n')
            time.sleep(2)
            channel.send(node_pw_1 + '\n')
            time.sleep(2)
            output = channel.recv(99999).decode('utf-8')
            
            print (output)
            choice(d_node)

    elif action == '11' or action == '12' or action == '13':
        for x in node_user:
            node_user_1 = str(x).strip(str(['']))
        for x in node_pw:
            node_pw_1 = str(x).strip(str(['']))
        try:
            print ('You have selected &s' %(action))
            if action == '11':
                print (SnwRcon11)
            elif action == '12':
                print (SnwRcon12)
            elif action == '13':
                print (SnwRcon13)
        except:
            print ('')
        sesh.connect(d_node.node_ip, 22, node_user_1,node_pw_1)
        channel = sesh.invoke_shell()
        print ('')
        print ("\033[92mConnection Made\033[0m ")
        print ('')
        Dmodel = d_node.model
        print (Dmodel)
        time.sleep(3)

        if 'Avocent' not in d_node.manu:
            print('\n')
            print ("\033[91m     Action selected is unavailable for this Device\033[0m ")
            print('\n')
            choice(d_node)
            
        if action == '11' and 'Avocent' in d_node.manu:
            print ('\033[4mAutomate Configurations:\033[0m')
            channel.send('set users/local_accounts/user_names/root/settings/ status=enabled\n')
            time.sleep(1)
            channel.send('set users/local_accounts/user_names/root/settings/ password=P@ssw0rd confirm_password=P@ssw0rd\n')
            time.sleep(1)
            channel.send('set users/local_accounts/user_names/root/settings/ password_change_at_next_login=no\n')
            time.sleep(1)
            channel.send('commit\n')
            time.sleep(3)
            output = channel.recv(99999).decode('utf-8')
            print (output)
            choice(d_node)

        elif action == '12' and 'Avocent' in d_node.manu:
            print ('\033[4mCollect Logs:\033\n[0m')
            channel.send('\n')
            channel.send('show system/information/\n')
            time.sleep(1)
            channel.send('show network/devices/eth0\n')
            time.sleep(1)
            channel.send('show network/devices/eth1\n')
            time.sleep(1)
            channel.send('show ports/serial_ports/\n')
            time.sleep(3)
            channel.send('\n')
            channel.send('show users/local_accounts/user_names/\n')
            time.sleep(1)
            output = channel.recv(99999).decode('utf-8')
            print (output)
            choice(d_node)

        elif action == '13' and "Avocent" in d_node.manu:
            print ('')
            print ('\033[4mFactory_Defaults:\033[0m')
            print ('')
            confirm = input("Type 'yes' to continue restarting device to Factory Default: ").lower()
            if confirm == 'yes' or confirm == 'y':
                channel.send('factory_defaults\n')
                time.sleep(1)
                channel.send('yes\n')
                time.sleep(3)
                output = channel.recv(99999).decode('utf-8')
                print (output)
                choice(d_node)
            else:
                print('\033[91m     No Action was made.\033[0m')
                choice(d_node)
    else:
        print('\n')
        print ("     \033[91mAction not valid, Try again.\033[0m")
        print('\n')
        choice(d_node)
        


if __name__ == '__main__':
    len_argv = len(sys.argv)
    m_nodes = None
    if len_argv < 2:
        print ('Initiate sshTools Program with sshTools.py <node_id>')
        sys.exit(0)
