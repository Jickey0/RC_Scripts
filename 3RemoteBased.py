import requests
import time

# --TODO: add disc --

UE_PROPS_BASE_URL = 'http://localhost:30010/remote/preset/MyRemote/property/Time of Day'

request_all_weather_data = {"objectPath" : "/Game/Main.Main:PersistentLevel.Ultra_Dynamic_Sky_C_1", "access" : "READ_ACCESS"}

def WeatherGetRequest(name, value):
    return { "propertyValue": value,
            "generateTransaction": True
            }   


def speed_test_change_time(start, increment, frequency_hz, max_value):
    current_value = start
    interval = 1.0 / frequency_hz  # seconds per request
    
    print(f"Starting speed test: increment {increment} every {interval*1000:.1f} ms")
    
    session = requests.Session()
    while current_value <= max_value:
        payload = WeatherGetRequest("Time of Day", current_value)
        response = session.put(UE_PROPS_BASE_URL, json=payload)
        current_value += increment

        print(f"Set Time of Day to {current_value} - Status: {response.status_code}")
        print(f"Status: {response.status_code} in {response.elapsed.total_seconds()*1000:.1f} ms")

        time.sleep(interval)


speed_test_change_time(0, 100, 5, 2400)