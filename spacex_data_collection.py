import requests
import pandas as pd
import numpy as np
import datetime

# Lists to store data
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

# Functions to get data from SpaceX API
def getBoosterVersion(data):
    for x in data['rocket']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
            BoosterVersion.append(response['name'])
        else:
            BoosterVersion.append(None)

def getLaunchSite(data):
    for x in data['launchpad']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
            Longitude.append(response['longitude'])
            Latitude.append(response['latitude'])
            LaunchSite.append(response['name'])
        else:
            Longitude.append(None)
            Latitude.append(None)
            LaunchSite.append(None)

def getPayloadData(data):
    for load in data['payloads']:
        if load:
            response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
            PayloadMass.append(response['mass_kg'])
            Orbit.append(response['orbit'])
        else:
            PayloadMass.append(None)
            Orbit.append(None)

def getCoreData(data):
    for core in data['cores']:
        if core['core'] != None:
            response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
            Block.append(response['block'])
            ReusedCount.append(response['reuse_count'])
            Serial.append(response['serial'])
        else:
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)
        Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
        Flights.append(core['flight'])
        GridFins.append(core['gridfins'])
        Reused.append(core['reused'])
        Legs.append(core['legs'])
        LandingPad.append(core['landpad'])

def main():
    # URL for SpaceX API
    spacex_url = "https://api.spacexdata.com/v4/launches/past"
    
    # Get response from API
    response = requests.get(spacex_url)
    print(f"API Response Status: {response.status_code}")
    
    # Check if request was successful
    if response.status_code == 200:
        # Get the data
        data = response.json()
        
        # Convert to dataframe
        data_df = pd.json_normalize(data)
        
        # Get all the additional data
        getBoosterVersion(data_df)
        getLaunchSite(data_df)
        getPayloadData(data_df)
        getCoreData(data_df)
        
        # Create a new dataframe with the collected data
        launch_dict = {
            'BoosterVersion': BoosterVersion,
            'PayloadMass': PayloadMass,
            'Orbit': Orbit,
            'LaunchSite': LaunchSite,
            'Outcome': Outcome,
            'Flights': Flights,
            'GridFins': GridFins,
            'Reused': Reused,
            'Legs': Legs,
            'LandingPad': LandingPad,
            'Block': Block,
            'ReusedCount': ReusedCount,
            'Serial': Serial,
            'Longitude': Longitude,
            'Latitude': Latitude
        }
        
        result_df = pd.DataFrame(launch_dict)
        
        # Save to CSV
        result_df.to_csv('spacex_launch_data.csv', index=False)
        print("\nData Collection Results:")
        print(f"Total launches collected: {len(result_df)}")
        print("\nFirst few rows of the data:")
        print(result_df.head())
        
    else:
        print(f"Failed to get data. Status code: {response.status_code}")

if __name__ == "__main__":
    main() 