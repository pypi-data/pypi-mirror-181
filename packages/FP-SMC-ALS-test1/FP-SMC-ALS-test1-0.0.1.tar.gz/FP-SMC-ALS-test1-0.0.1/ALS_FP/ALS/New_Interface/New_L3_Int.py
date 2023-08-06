from ALS_FP.Library.libr import *

def NEW_l3_Int(Site_Readiness_file_path,Sheet_Name,Interface_ID,ISP_Name):
    df = pd.read_excel(Site_Readiness_file_path,sheet_name=Sheet_Name)
    LIST_DF = df.values.tolist()
    # List_DHCP = df['DHCP Enabled'].values.tolist()
    DHCP = df['DHCP Address Range']
    IP_Address = df['IP ADDRESS']
    Country = df['COUNTRY']
    Net_IP = df['NETWORK']
    VLAN_Name = df['VLAN NAME']
    VLAN_ID = df['VLAN ID']
    VLAN_NET = df['VLAN NETWORK']
    # DHCP_STATUS = df['DHCP Enabled']
    DHCP_Range = df['DHCP Address Range']
    Net_ADD = df['GATEWAY']
    Dynamic = "Dynamic"
    Yes = "Yes"
    No = "No"
    i = 0
    j = 0
    # print(path)
    # print(Interface_ID)
    # print(ISP_Name)
    for row in LIST_DF:
        if row[4] == 'YES':
            # NET_NAME_STANDARD = (row[1] + "-NET-" + row[0] + "-" + row[2] + "-" + ISP_Name + "-" + (row[6]))  ##rnetwork = (row[6])
            # print(NET_NAME_STANDARD)
            # ISP Interface along with Static IP interface creation.
            # if row[4] == 'LAN':
            # Netlink Network creation
            RNET_NAME_STANDARD = (row[1] + "-NET-" + row[0] + "-" + row[2] + "-" + ISP_Name + "-" + (row[6]))  ##rnetwork = (row[6])
            RNET_OBJ_NAME_FINAL = (RNET_NAME_STANDARD.upper())
            Network.create(name=RNET_OBJ_NAME_FINAL, ipv4_network=(row[6]))
            if Network.create:
                print("Network element created:", (RNET_OBJ_NAME_FINAL))
            # FW Interface creation
            FW_NAME_STANDARD = (row[1] + "-" + row[0] + "-" + row[2] + "-FW")
            # FW_NAME_STANDARD = ("FW_Name")
            FW_NAME_FINAL = (FW_NAME_STANDARD.upper())
            engine = Engine(FW_NAME_FINAL)
            engine.physical_interface.add_layer3_interface(interface_id=Interface_ID, address=row[5], network_value=row[6],
                                                           comment=ISP_Name, zone_ref="External")
            print("Interface ", Interface_ID, " Successfully")

            # ISP Router Creation
            RTR_Gateway1 = (row[7])
            ISPRname = (row[1] + "-" + row[0] + "-" + row[2] + "-" + ISP_Name + "-" + "ROUTER")
            Router.create(ISPRname, RTR_Gateway1)
            if Router.create:
                print("Router is created:", (ISPRname))

            # Netlink creation
            nlname = (row[1] + "-" + row[0] + "-" + row[2] + "-" + ISP_Name + "-" + "-NETLINK")
            StaticNetlink.create(name=nlname, gateway=Router(ISPRname), network=[Network(RNET_OBJ_NAME_FINAL)], probe_address=['8.8.8.8'])
            if StaticNetlink.create:
                print("Static Netlink Created:", (nlname))
            rtnode = engine.routing.get(Interface_ID)
            rtnode.add_traffic_handler(netlink=StaticNetlink(nlname))  ## netlink_gw=[Router(ISPRname)]
            print("Traffic handler is assigned to the newly created Internet. Please set default route manually for same.")