# from helper import get_m_nodes, fs_webtoolkit_and_models_access #get_all_attributes
# fs_webtoolkit_and_models_access()
#import sys
# from fs_razor_core.models import ManagedNode#,Customers
#from find_ip import find_ip
#import ColorTerminalOutput

class ColorTerminalOutput:
    """Class for colored output to terminal"""

    def __init__(self):
        self.ok = '\033[92m'
        self.error = '\033[91m'
        self.ko = '\033[93m'
        self.end = '\033[0m'
        self.clear = '\033[0m'


Terminal = ColorTerminalOutput
ServiceNow_usage = """


\t==========================================================================


\t\033[36m[ServiceNow PDU Configuration]\033[0m 

\t[1] Port Assignment:

\t[2] Automate Configurations:
\t    - PDU-Serial Naming, Enabling SNMP and Register Hostname

\t[3] Collect Logs:


\t==========================================================================


"""
Roblox_usage = """


\t==========================================================================


\t\033[36m[Roblox PDU Configuration]\033[0m

\t[4] Configure Settings:
\t    - Configure IP, Subnet Mask, Gateway.
\t    - Automate SNMP Enable, Configure Banner, Location & FQDN Name.

\t[5] Collect Logs:

\t[6] Disabling DHCP:
\t    - Note: Connectivity will be lost!

\t[7] Restart Device to Factory Defaults:


\t==========================================================================


"""
Cumulus_usage = """

\t==========================================================================


\t\033[36m[Dell Cumulus Configuration]\033[0m

\t[8] Automate Configurations:
\t    - Applying License, Add Ports, Port Naming, Set Bridging and Add Users.

\t[9] Collect Logs:

\t[10] Automate Post Snapshot Configurations:
\t    - Delete all configs then re-automate configs without Bridging.


\t==========================================================================


"""
Avocent_usage = """

\t==========================================================================


\t\033[36m[Avocent Console Configuration]\033[0m

\t[11] Automate Configurations:
\t    - set user root settings(status & pw) and pw change at next login=no

\t[12] Collect Logs:

\t[13] Factory_Defaults:


\t==========================================================================


"""


def Servicenowinfo():
    print(ServiceNow_usage)


def Robloxinfo():
    print(Roblox_usage)


def Cumulusinfo():
    print(Cumulus_usage)


def Avocentinfo():
    print(Avocent_usage)


class Device:
    def __init__(self, node_id, serial, manu, model, customer, device_type, app_name, node_ip, project):
        self.node_id = node_id
        self.device_type = device_type
        self.serial = serial
        self.node_ip = node_ip
        try:
            if len(self.node_ip) == 0:
                self.node_ip = ('\033[91mNo ip found\033[0m')
        except:
            self.node_ip = 'no ip'
        self.app_name = app_name
        self.project = project
        self.manu = manu
        self.model = model
        self.customer = customer
        self.user = []
        self.pw = []
        self.sku = []
        self.result = None
        self.device_type_nodes = []
        self.nodes_ids = []
        self.set_nodes()
        self.port = 22

    def set_nodes(self):
        Snow_Dell_User = 'cumulus'
        Snow_Dell_PW = 'CumulusLinux!'
        Snow_Pdu_User = 'admin'
        Snow_Pdu_PW = 'P@ssw0rd'
        Snow_JNPR_User = 'root'
        Snow_JNPR_PW = ''
        Roblox_User = 'admn'
        Roblox_PW = '#Roblox2020'
        Square_User = 'admn'
        Square_PW = 'admn'

        try:
            Roblox_pdu = ['C2W42CE-YQME2M00/C', 'C2X42CE-YQME2M00/C', 'C1W24VT-5PPA17AC/C',
                          'C1X24VT-5PPA17AC/C', 'C1L24VS-4PFA11F2/C', 'C1S24VS-4PFA11F2/C',
                          'C1S24VS-4PFA11F2/C.RED', 'C1L24VS-4PFA11F2/C.BLUE']
            Square_pdu = ['C2W42CE-DQME2M00/0C.7ft.red',
                          'C2X42CE-DQME2M00/0C.7ft.blue']
            Snow_pdu = ['PX3-5961I2U-C8V2A6K1', 'PX3-5785U-V2A6K2', 'PX3-5961I2U-C8V2A6K2',
                        'PX3-5961I2U-V2A6K2', 'PX3-5703-A6K1', 'PX3-5723I2-C8A6K2', 'PX3-5723I2-C8A6K1',
                        'PX3-5040U-V2-A6K2', 'PX3-5040U-V2-A6K1', 'G2-84208-80B', 'G2-84208-80R']
            Snow_dell_swi = ['210-AEDQ']
            Snow_jnpr_swi = ['QFX5100-48S-AFI', 'QFX5120-48Y-AFI']
            
            Snow_rcon_swi = ['ACS8008MDAC-400', 'ACS8032MDAC-400',
                             'ACS8016MDAC-400', 'ACS8048MDAC-400']
            AllServers = ['c6420', 'r640', 'R740']
            Square_swi = ['DCS-7050TX2-128-R']

            if self.model in (Square_pdu):
                user = Square_User
                pw = Square_PW
            elif self.model in (Roblox_pdu):
                user = Roblox_User
                pw = Roblox_PW
            elif self.model in (Snow_pdu):
                user = Snow_Pdu_User
                pw = Snow_Pdu_PW
            elif self.model in (Snow_dell_swi):
                user = Snow_Dell_User
                pw = Snow_Dell_PW
            elif self.model in (Snow_jnpr_swi):
                user = Snow_JNPR_User
                pw = Snow_JNPR_PW
            elif self.model in (Snow_rcon_swi):
                user = Snow_Pdu_User
                pw = Snow_Pdu_PW
            elif self.model in (AllServers):
                user = 'root'
                pw = 'fr3sca'
            elif self.model in (Square_swi):
                user = 'admin'
                pw = ''
        except:
            self.model = 'no model'

        self.user.append(user)
        self.pw.append(pw)
