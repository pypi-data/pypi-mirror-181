from ALS_FP.Library.libr import *


def New_CCNMP_Template(Site_Readiness_file_path, Sheet_Name, LAN_Interface,
                       IC_Interface_ID, Static_Public_IP_Int, ISP_NAME):
    df = pd.read_excel(Site_Readiness_file_path, sheet_name=Sheet_Name)
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
    # Network & Group Creation
    for row in LIST_DF:
        NET_NAME_STANDARD = (row[1] + "-NET-" + row[0] + "-" + row[2] + "-" + row[11] + "-" + (row[13]))
        NET_OBJ_NAME_FINAL = (NET_NAME_STANDARD.upper())
        GRP_NAME_STANDARD = (row[1] + "-GRP-" + row[0] + "-" + row[2])
        GRP_NAME_FINAL = (GRP_NAME_STANDARD.upper())
        while (j < 1):
            try:
                Group.create(GRP_NAME_FINAL)
            except Exception as e:
                print(e)
                pass
            nwk_element = Group(GRP_NAME_FINAL)
            RO_STORE_NAME_STANDARD = row[3]
            # add if group.create section here
            if row[3] is not None:
                try:
                    grp = Group.update_or_create(name=RO_STORE_NAME_STANDARD, members=[nwk_element])
                except Exception as e:
                    # print(nwk_element)
                    print(e)
                    pass
            j += 1
        try:
            Network.create(name=NET_OBJ_NAME_FINAL, ipv4_network=(row[13]))
            if Network.create:
                print("Network element created:", (NET_OBJ_NAME_FINAL))
                nwk = Network(NET_OBJ_NAME_FINAL)
                grp = Group.update_or_create(name=GRP_NAME_FINAL, members=[nwk])
        except Exception as e:
            print(e)
            pass
    # Creating Firewall with DHCP interface
    for row in LIST_DF:
        while (i < 1):
            FW_NAME_STANDARD = (row[1] + "-" + row[0] + "-" + row[2] + "-FW")
            FW_NAME_FINAL = (FW_NAME_STANDARD.upper())
            print(FW_NAME_FINAL)
            GRP_NAME_STANDARD = (row[1] + "-GRP-" + row[0] + "-" + row[2])
            GRP_NAME_FINAL = (GRP_NAME_STANDARD.upper())
            SITE_GROUP = Group(GRP_NAME_FINAL)
            engine = Layer3Firewall.create_dynamic(name=FW_NAME_FINAL, interface_id=IC_Interface_ID,
                                                   zone_ref=("External"), domain_server_address=['8.8.8.8', '4.2.2.2'],
                                                   default_nat=False, enable_gti=True)
            SITE_NAME_STANDARD = (row[1] + "-" + row[0] + "-" + row[2] + "-SITE")
            SITE_NAME_FINAL = (SITE_NAME_STANDARD.upper())
            try:
                engine.vpn.add_site(name=SITE_NAME_FINAL, site_elements=[SITE_GROUP])
                print("VPN Site Created and assigned store Group")
            except Exception as e:
                print("****")
                print(e)
                print("    ****")
                pass
            print("Firewall Created Successfully. Created Interface ",IC_Interface_ID," with DHCP")
            i += 1
    # If Static IP provided//Creating Interface 0 with Static IP and creating LAN Gateway/Creating NetlinkMake sure MGMT Interface is in first
    for row in LIST_DF:
        if row[4] == 'YES' and row[11] == 'MGMT':
            RNET_NAME_STANDARD = (row[1] + "-NET-" + row[0] + "-" + row[2] + "-" + ISP_NAME + "-" + (row[6]))
            RNET_OBJ_NAME_FINAL = (RNET_NAME_STANDARD.upper())
            Network.create(name=RNET_OBJ_NAME_FINAL, ipv4_network=(row[6]))
            if Network.create:
                print("Network element created:", (RNET_OBJ_NAME_FINAL))
            FW_NAME_STANDARD = (row[1] + "-" + row[0] + "-" + row[2] + "-FW")
            FW_NAME_FINAL = (FW_NAME_STANDARD.upper())
            engine = Engine(FW_NAME_FINAL)
            engine.physical_interface.add_layer3_interface(interface_id=Static_Public_IP_Int, address=row[5], network_value=row[6],
                                                           comment=ISP_NAME, zone_ref="External")
            print("Interface ",Static_Public_IP_Int," Created Successfully")
            # ISP Router Creation
            RTR_Gateway1 = (row[7])
            ISPRname = (row[1] + "-" + row[0] + "-" + row[2] + "-" + ISP_NAME + "-ROUTER")
            Router.create(ISPRname, RTR_Gateway1)
            if Router.create:
                print("Router is created:", (ISPRname))
            # Netlink creation
            nlname = (row[1] + "-" + row[0] + "-" + row[2] + "-" + ISP_NAME + "-NETLINK")
            StaticNetlink.create(name=nlname, gateway=Router(ISPRname), network=[Network(RNET_OBJ_NAME_FINAL)],
                                 probe_address=['8.8.8.8'])
            if StaticNetlink.create:
                print("Static Netlink Created:", (nlname))
            rtnode = engine.routing.get(Static_Public_IP_Int)
            rtnode.add_traffic_handler(netlink=StaticNetlink(nlname))  ## netlink_gw=[Router(ISPRname)]
            print(
                "Traffic handler is assigned to the newly crea]ted Internet. Please set default route manually for same.")

            # LAN Gateway creation
            LAN_Gateway = (row[10])
            Rname = (row[1] + "-" + row[0] + "-" + row[2] + "-LAN GATEWAY")
            Router.create(Rname, LAN_Gateway, comment='LAN GATEWAY')
            if row[16] == 'YES':
                engine.physical_interface.add_layer3_interface(interface_id=LAN_Interface, address=row[15], network_value=row[13],
                                                               comment="LAN", zone_ref="Internal",
                                                               dhcp_server_on_interface={'default_gateway': row[15],
                                                                                         'default_lease_time': '86400',
                                                                                         'dhcp_address_range': row[20],
                                                                                         'dhcp_range_per_node': [],
                                                                                         'primary_dns_server': row[21],
                                                                                         'secondary_dns_server': row[
                                                                                             22]})
            else:
                engine.physical_interface.add_layer3_interface(interface_id=LAN_Interface, address=row[15], network_value=row[13],
                                                               comment="LAN", zone_ref="Internal")

            print("Interface ",LAN_Interface," Successfully")
            LAN_Gateway = (row[10])
            Rname = (row[1] + "-" + row[0] + "-" + row[2] + "-LAN GATEWAY")
            Router.create(Rname, LAN_Gateway)  # , comment='LAN GATEWAY'
            if Router.create:
                print("LAN Gateway Router Created Successfully")

    # No Static IP provided/Creating only LAN Gateway
    for row in LIST_DF:
        if row[4] == 'NO' and row[11] == 'MGMT':
            # if row[4] == 'LAN':
            FW_NAME_STANDARD = (row[1] + "-" + row[0] + "-" + row[2] + "-FW")
            # FW_NAME_FINAL = (FW_NAME_STANDARD.str.upper())
            FW_NAME_FINAL = (FW_NAME_STANDARD.upper())
            engine = Engine(FW_NAME_FINAL)
            engine.physical_interface.add_layer3_interface(interface_id=LAN_Interface, address=row[15], network_value=row[13],
                                                           comment="LAN", zone_ref="Internal")
            print("Interface ",LAN_Interface," Successfully")
            LAN_Gateway = (row[10])
            Rname = (row[1] + "-" + row[0] + "-" + row[2] + "-LAN GATEWAY")
            Router.create(Rname, LAN_Gateway)  # , comment='LAN GATEWAY'
            if Router.create:
                print("LAN Gateway Router Created Successfully")
    # adding lan gateway and networks
    for row in LIST_DF:
        FW_NAME_STANDARD = (row[1] + "-" + row[0] + "-" + row[2] + "-FW")
        FW_NAME_FINAL = (FW_NAME_STANDARD.upper())
        engine = Engine(FW_NAME_FINAL)
        NET_NAME_STANDARD = (row[1] + "-NET-" + row[0] + "-" + row[2] + "-" + row[11] + "-" + (row[13]))
        NET_OBJ_NAME_FINAL = (NET_NAME_STANDARD.upper())
        Rname = (row[1] + "-" + row[0] + "-" + row[2] + "-LAN GATEWAY")
        route1 = engine.routing.get(LAN_Interface)
        try:
            route1.add_static_route(gateway=Router(Rname), destination=[Network(NET_OBJ_NAME_FINAL)])
            # print("LAN Gateway and networks are assigned to LAN Interface")
        except Exception as e:
            print(e)

    #Enabling SNMP
    k = 0
    for row in LIST_DF:
        FW_NAME_STANDARD = (row[1] + "-" + row[0] + "-" + row[2] + "-FW")
        FW_NAME_FINAL = (FW_NAME_STANDARD.upper())
        engine = Engine(FW_NAME_FINAL)
        while (k < 1):
            try:
                engine.snmp.enable(SNMPAgent("Solarwinds_SNMP_Agent"), snmp_location=FW_NAME_FINAL,
                                   snmp_interface=[LAN_Interface])
                engine.antivirus.enable()
                engine.update()
                print("SNMP is enabled")
            except Exception as e:
                print(e)
                pass
            k += 1
