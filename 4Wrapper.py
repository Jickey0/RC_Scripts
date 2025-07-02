from upyrc import upyrc
import logging

# -- TODO: add disc --

print(upyrc.__file__)

#import logging
upyrc.set_log_level(logging.DEBUG)
print("Version:", upyrc.get_version())

print("\n----------- INIT CONNECTION --------------------------------------------------------------------------------------------------------------------------------\n")

# Create a connection to Unreal
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
preset_property = preset.get_property("Fog")
print("Previous Fog value: ", preset_property.eval())
# >>> Relative Location (SM_Lamp_Ceiling) value: {'X': 330, 'Y': 10, 'Z': 0}


print("\n----------- CHANGE FOG --------------------------------------------------------------------------------------------------------------------------------\n")

# Set a property value:
# currently the JSON is empty (WHYYYYYYY)
preset_property.set(Fog=7)
print("New Fog Value: ", preset_property.eval())
# The object "PointLight" has now its Z position set to 200.0

# Changing the PointLight color to red.
#preset_property_light_color = preset.get_property("Time Of Day")
#preset_property_light_color.set(Time_of_Day=1000)

