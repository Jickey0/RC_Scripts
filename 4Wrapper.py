import logging
import socket
import sys
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 4210
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(5.0)  # 5 second timeout
print("Listening for data on port", UDP_PORT)

# ---------------- Import Wrapper via local storage ---------------
sys.path.insert(0, r"UnrealRemoteControlWrapper\UnrealRemoteControlWrapper-main\src")
from upyrc import upyrc
# -----------------------------------------------------------------

# -- TODO: add disc --

print(upyrc.__file__)

#import logging
upyrc.set_log_level(logging.DEBUG)
print("Version:", upyrc.get_version())

print("\n----------- INIT CONNECTION --------------------------------------------------------------------------------------------------------------------------------\n")


# Create a connection to Unreal --> host='192.168.0.20' if connecting to rig
conn = upyrc.URConnection(host='192.168.0.20')
print("Ping: ", conn.ping())
# >>> Ping: 127.0.0.1:30010

print("\n----------- REMOTE PRESET --------------------------------------------------------------------------------------------------------------------------------\n")

# Get all presets basic infos ( Name, ID and path )
all_presets = conn.get_all_presets()
print("Presets: ", all_presets)
# >>> Presets: [{'Name': 'RCP_TestPreset', 'ID': '916A553549DCE66727D00585DED11589', 'Path': '/Game/RCP_TestPreset.RCP_TestPreset'}]

# Get an preset object, by name.
preset_name = "MyRemote"
preset = conn.get_preset(preset_name)
print("Preset: ", preset)
# >>> Preset:  UObject: /Game/RCP_TestPreset.RCP_TestPreset, of Class RemotePreset

print(preset.get_all_property_names())

# Get a preset exposed property:
preset_property = preset.get_property("Time Of Day")
print("Previous Day value: ", preset_property.eval())
# >>> Relative Location (SM_Lamp_Ceiling) value: {'X': 330, 'Y': 10, 'Z': 0}

last_val = 0
while True:
    try:
        data, addr = sock.recvfrom(1024)
        new_val = data.decode()
        print(f"Received from {addr}: {new_val}")
        print("type of data: ", type(new_val))

        if last_val != new_val:
            preset_property.single_set(int(new_val))
            print("New Time: ", preset_property.eval())
            last_val = new_val

    except socket.timeout:
        print("No data received (timeout).")
