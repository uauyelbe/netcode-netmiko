import netmiko
from netmiko import ConnectHandler, cisco, NetMikoAuthenticationException
import yaml

with open("device_2960_shar.yaml") as dev:
    f = yaml.load(dev, Loader=yaml.FullLoader)
    for i in range(len(f)):
        try:
            ssh_connect = ConnectHandler(
                device_type="cisco_ios",
                ip=f[i],
                username="username",
                password="password",
                port=22
            )
        except:
            print("Unable to connect " + str(f[i]))
            continue

        result = ssh_connect.send_config_from_file("2960_acl_config.txt")
        print("config is loaded to " + str(f[i]))
        with open("sh_run_acl/" + str(f[i]) + ".txt", "a") as config:
            acl = ssh_connect.send_command("sh ip access-lists")
            config.write(acl)