import serial
import struct
SERIAL_PORT = 'COM5'
BAUD_RATE = 115200

import logging
import sys

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
conn = upyrc.URConnection()
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
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Listening on {SERIAL_PORT} at {BAUD_RATE} baud...")
    while True:
        # Wait for 2 bytes (size of int)
        data = ser.read(2)
        if len(data) == 2:
            # Unpack as little-endian signed int (same as Arduino default)
            new_val = struct.unpack('<h', data)[0]
            print("Received:", new_val)

            if last_val != new_val:
                preset_property.single_set(int(new_val))
                print("New Time: ", preset_property.eval())
                last_val = new_val

except serial.SerialException as e:
    print(":x: Serial error:", e)
except KeyboardInterrupt:
    print("\n:wave: Exiting.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()