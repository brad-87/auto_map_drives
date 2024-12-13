## auto_map_drives


# drives.pyw
This will add and remove network drives depending on the share availability. I justified this program because if you click on a mapped network drive in explorer when it isn't available, the system just get stuck waiting until the network connection times out. I find that very annoying.


This will look for a config in C:\Users\[username]\.smb\config.yaml
If the file doesn't exist, it will create it and show an example config.
