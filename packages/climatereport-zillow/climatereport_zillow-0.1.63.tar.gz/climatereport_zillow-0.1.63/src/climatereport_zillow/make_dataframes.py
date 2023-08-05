import pandas as pd
from climatereport_zillow.make_vars_zip import make_vars_zip
from climatereport_zillow import heat_zip_file, heat_state_file, fire_zip_file, fire_state_file, flood_zip_file, flood_state_file


def create_file_zip(risk,file):
    risk_zip = file
    make_vars_zip(risk_zip, risk)
    risk_zip = risk_zip.set_index("fips")
    return risk_zip

def create_file_state(risk,file):
    risk_state = file
    risk_state.columns = risk_state.columns.str.replace(risk, "risk")
    risk_state["state"] = risk_state["name"]
    state_dict = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "American Samoa": "AS",
                  "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
                  "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
                  "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY",
                  "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
                  "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
                  "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
                  "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
                  "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Puerto Rico": "PR",
                  "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
                  "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
                  "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}

    risk_state = risk_state.replace({'state':state_dict})
    risk_state = risk_state.set_index("state")
    return risk_state
