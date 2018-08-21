'''
    Configure the SSH port
'''

port = 22

'''
    The keys of this dictionnary are the supported device_type that can be found on
    https://github.com/ktbyers/netmiko/blob/master/netmiko/ssh_dispatcher.py
'''

vendor = [
    'a10',
    'accedian',
    'alcatel_aos',
    'alcatel_sros',
    'arista_eos',
    'aruba_os',
    'avaya_ers',
    'avaya_vsp',
    'brocade_fastiron',
    'brocade_netiron',
    'brocade_nos',
    'brocade_vdx',
    'brocade_vyos',
    'checkpoint_gaia',
    'calix_b6',
    'ciena_saos',
    'cisco_asa',
    'cisco_ios',
    'cisco_nxos',
    'cisco_s300',
    'cisco_tp',
    'cisco_wlc',
    'cisco_xe',
    'cisco_xr',
    'coriant',
    'dell_force10',
    'dell_powerconnect',
    'eltex',
    'enterasys',
    'extreme',
    'extreme_wing',
    'f5_ltm',
    'fortinet',
    'generic_termserver',
    'hp_comware',
    'hp_procurve',
    'huawei',
    'huawei_vrpv8',
    'juniper',
    'juniper_junos',
    'linux',
    'mellanox',
    'mrv_optiswitch',
    'netapp_cdot',
    'ovs_linux',
    'paloalto_panos',
    'pluribus',
    'quanta_mesh',
    'ruckus_fastiron',
    'ubiquiti_edge',
    'ubiquiti_edgeswitch',
    'vyatta_vyos',
    'vyos',
]
