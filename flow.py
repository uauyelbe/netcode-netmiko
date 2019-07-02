import netmiko
from netmiko import ConnectHandler, cisco, NetMikoAuthenticationException
import ipaddress
from netaddr import IPAddress, IPNetwork

#get qradar routes from asbr
def get_qradar_routes(ssh_connect):
    qradar_routes = ssh_connect.send_command("sh flow monitor qradar cache format table | in Po1.915")
    with open("qradar_routes.txt", "a") as f_qradar:
        f_qradar.write(qradar_routes)
    qradar = open("qradar_routes.txt", "r")
    return qradar

#get sh ip bgp from AS 21299
def get_ip_bgp_routes(ssh_connect):
    ip_bgp_routes = ssh_connect.send_command("sh ip bgp | in 21299")
    with open("ip_bgp_routes.txt", "a") as f_ip_bgp:
        f_ip_bgp.write(ip_bgp_routes)
    ip_bgp = open("ip_bgp_routes.txt", "r")
    return ip_bgp

#check if ip address from qradar monitor is in subnet from sh ip bgp
def ip_compare(qradar, ip_bgp):
    flag = 0
    a = ""
    for i in qradar:
        ip_qradar = i.rstrip().split(" ")
        for j in ip_bgp:
            ip_bgp_addr = j.rstrip().split(" ")
            if (IPAddress(ip_qradar[0]) in IPNetwork(ip_bgp_addr[4])) and (IPAddress(ip_qradar[0]) not in IPNetwork("194.187.245.0/24")):
                flag = 1
                a = ip_bgp_addr[4]
                with open("ip_bgp_in_qradar.txt", "a") as res:
                    res.write(str(ip_qradar[0]) + " in " + str(a) + "\n")
            else:
                continue
        if not flag:
            with open("ip_bgp_not_in_qradar.txt", "a") as res:
                if IPAddress(ip_qradar[0]) not in IPNetwork("194.187.245.0/24"):
                    res.write(str(ip_qradar[0]) + " not in ip bgp prefixes" + "\n")
                else:
                    continue
        flag = 0

def main():
    ssh_connect = ConnectHandler(
        device_type="cisco_ios",
        ip="10.10.10.1",
        username="username",
        password="password",
        port=22
    )

    qradar_open = get_qradar_routes(ssh_connect)
    ip_bgp_open = get_ip_bgp_routes(ssh_connect)
    
    #checks if ip address in listed bgp prefix
    with qradar_open, ip_bgp_open:
        qradar = qradar_open.readlines()
        ip_bgp = ip_bgp_open.readlines()
        ip_compare(qradar, ip_bgp)

if __name__ == "__main__":
    main()