import netmiko
from netmiko import ConnectHandler, cisco, NetMikoAuthenticationException
import yaml

with open("Catalyst 2960 gold config.txt") as gold, open("sh run.txt") as sh_run:
    gold_config = gold.readlines()
    sh_run_cat = sh_run.readlines()
    with open("device.yaml") as dev:
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
                print("Unable to connect:" + str(f[i]))
                continue

            cmnd_sh_run = ssh_connect.send_command("sh ip access-lists")

            with open("sh_run_acl/acl_result_"+str(f[i]) + ".txt", "a") as res:
                for j in gold_config:
                    if j not in cmnd_sh_run:
                        res.write(j)
                        print(str(f[i]) + " done")