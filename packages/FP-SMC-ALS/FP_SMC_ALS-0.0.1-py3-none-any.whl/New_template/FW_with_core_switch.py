

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

for row in LIST_DF:
    NET_NAME_STANDARD = (row[1] + "-NET-STR-" + row[2] + "-" + row[11] + "-" + (row[13]))
    NET_OBJ_NAME_FINAL = (NET_NAME_STANDARD.upper())
    Network.create(name=NET_OBJ_NAME_FINAL, ipv4_network=(row[13]))
    #GRP_NAME_STANDARD = (row[1] + "-GRP-MALL-" + row[2])
    #GRP_NAME_FINAL = (GRP_NAME_STANDARD.upper())
    #Group.update_members(self=GRP_NAME_FINAL,members=list[(NET_OBJ_NAME_FINAL),(row[13])], append_lists=True, remove_members=False)

    if Network.create:
        print("Network element created:", (NET_OBJ_NAME_FINAL))


Dynamic = "Dynamic"
Yes = "Yes"
No = "No"
i = 0
for row in LIST_DF:
    for x in IP_Address:
        while (i < 1):
            if x == Dynamic:
                FW_NAME_STANDARD = (row[1] + "-MALL-" + row[2] + "-FW")
                FW_NAME_FINAL = (FW_NAME_STANDARD.upper())
                print(FW_NAME_FINAL)
                engine = Layer3Firewall.create_dynamic(name=FW_NAME_FINAL,
                                                       interface_id="2",
                                                       # domain_server_address=list(Siterediness(row[7])),
                                                       zone_ref=("external"))
                engine.file_reputation.enable(http_proxy=None)
                #print(engine.file_reputation.status)
                GRP_NAME_STANDARD = (row[1] + "-GRP-STR-" + row[2])
                GRP_NAME_FINAL = (GRP_NAME_STANDARD.upper())
                Group.create(name=GRP_NAME_FINAL)
                i += 1
            else:
                FW_NAME_STANDARD = (row[1] + "-STR-" + row[2] + "-FW")
                FW_NAME_FINAL = (FW_NAME_STANDARD.upper())
                print(FW_NAME_FINAL)
                engine = Layer3Firewall.create(name=FW_NAME_FINAL,
                                               mgmt_ip=(str(row[5])),
                                               mgmt_network=(str(row[6])),
                                               mgmt_interface=0,
                                               zone_ref=("external"))

                i += 1

###Internal Interface Assignment
for row in LIST_DF:
    if row[11] == 'MGMT':
        FW_NAME_STANDARD = (row[1] + "-MALL-" + row[2] + "-FW")
        # FW_NAME_FINAL = (FW_NAME_STANDARD.str.upper())
        FW_NAME_FINAL = (FW_NAME_STANDARD.upper())
        engine = Engine(FW_NAME_FINAL)
        engine.physical_interface.add_layer3_interface(interface_id=1, address=row[15],
                                                            network_value=row[13],
                                                            comment=row[11],
                                                       zone_ref="internal")
        print("Interface 1 Created Successfully")

    else:
        print("Not created Layer3")



session.logout()

