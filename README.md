# netcode-netmiko
analyze ip addresses and bgp prefixes from cisco devices.
flow.py connects to device and gets result from qradar flow and writes to .txt file.
Also gets result from command "sh ip bgp" and writes to .txt file.
Compares if ip address from qradar flow belongs to any bgp prefix and writes to .txt file in both cases.
