"""

This can be triggered in Windows Task Scheduler on network connect/disconnect events.
Create a task that is triggered by multiple events.

Event 1:
    Log: Microsoft-Windows-NetworkProfile/Operational 
    Source: Network Profile 
    EvenID: 10000           <-- This is a network connection event

Event 2:
    Log: Microsoft-Windows-NetworkProfile/Operational 
    Source: Network Profile 
    EvenID: 10001           <-- This is a network disconnection event

Event 3:
    Trigger is "On connection to user session" Select "Any User", "Connections from local computer" and "Delay task for" = 3 seconds

"""

import subprocess, os, time

import yaml                 # pip install pyyaml
from pathlib import Path    # pip install pathlib


# Change to true for verbose debug outputs
debug_output = False

######################################################################################################################################################################################################
######################################################################################################################################################################################################
######################################################################################################################################################################################################
######################################################################################################################################################################################################
# Function that does the actual mounting


def mount_drive():

    # Register if the host is available
    command = r'ping -n 2 ' + host
    server = subprocess.Popen( command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    server.wait()
    unreachable = server.poll()

    if(debug_output):
        print("host: " + host + "\t\tUnreachable:" + str(unreachable) )



    # If file server is offline, then unmount network resources, and remove registry values for mount labels
    if ( unreachable ):
        # Unmount if not available
        command = 'net use ' + drive + ': /d /y'
        subprocess.call( command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if(debug_output):
            print(command)


        # Remove RegKey for the share - helps later with labeling drives
        command = 'reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MountPoints2\\##' + host + '#' + share + ' /f'
        subprocess.call( command,shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if(debug_output):
            print(command)



    # If file server is online, mount share(s) and label drive(s)
    else:
        # Add RegKey for desired labeling
        command = 'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MountPoints2\\##' + host + '#' + share + ' /v _LabelFromReg /t REG_SZ /f /d ' + share_name
        subprocess.call(command,shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if(debug_output):
            print(command)


        # Mount the share
        command = 'net use ' + drive + ': \\\\' + host + '\\' + share + ' /user:' + user + ' ' + key
        subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if(debug_output):
            print(command)


######################################################################################################################################################################################################
######################################################################################################################################################################################################
######################################################################################################################################################################################################
######################################################################################################################################################################################################
# Check for config path and file, make them if not found


config_path = str( Path.home() ) + "\\.smb"
if not os.path.exists(config_path):
    os.makedirs(config_path)

    if(debug_output):
        print('Path not found, creating folder')


config_file = str( Path.home() ) + "\\.smb\\config.yaml"
if not os.path.isfile(config_file):
    with open(config_file, 'w') as file:
        file.write('# EXAMPLE LAYOUT\n')
        file.write('#share_label:\n')
        file.write('    #host: 192.168.1.*\n')
        file.write('    #share: storage\n')
        file.write('    #user: guest\n')
        file.write('    #key: password123\n')
        file.write('    #drive: z')
    file.close()

    if(debug_output):
        print('config not found, creating config file')


    time.sleep(1)


######################################################################################################################################################################################################
######################################################################################################################################################################################################
######################################################################################################################################################################################################
######################################################################################################################################################################################################
# Read the config.yaml file and extract SMB details


with open(config_file, 'r') as file:
    data = yaml.safe_load(file)

file.close()


for share_name, content in data.items():
    
    if isinstance(content, dict):  # Ensure the content is a dictionary
        for sub_key, sub_value in content.items():
            if sub_key == 'host':
                host = sub_value
            elif sub_key == 'user':
                user = sub_value
            elif sub_key == 'key':
                key = sub_value
            elif sub_key == 'drive':
                drive = sub_value
            elif sub_key == 'share':
                share = sub_value
    mount_drive()


######################################################################################################################################################################################################
######################################################################################################################################################################################################
######################################################################################################################################################################################################
######################################################################################################################################################################################################
