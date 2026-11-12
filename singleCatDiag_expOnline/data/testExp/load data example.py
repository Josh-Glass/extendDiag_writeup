import os, json
import pandas as pd


for file in os.listdir('./'): # <-- iterate through jsons
    if file.endswith('.json') == True:
        with open(file, 'r') as file:
            data = json.load(file) # <-- load as a python dictionary

            df = pd.DataFrame(data['trainPhase'][1:], columns = data['trainPhase'][0]) # <-- convert to pandas df (or you can use numpy or even the csv modules; doesnt matter)
            print(df)
            ## now you can do whatever you want with it

        exit()