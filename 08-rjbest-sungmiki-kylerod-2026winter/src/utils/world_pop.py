import pandas as pd

def world_pop(filename: str) -> pd.DataFrame:
    '''
    input: filename
    return: pandas dataframe
    '''
    # Initiate a list of population dataframes
    # Map country codes to full names (only South African population)
    country_map = {"zaf": "South Africa"}


    # Create a list with filename parts
    parts = filename.split("_")
    parts = filename.split("\\")
    parts = parts[-1].split("_")
    print(f"Population density from {parts[2]}",parts)

    # Extract metadata from filename
    country_code = parts[0].lower()
    year = int(parts[2])
    country_name = country_map.get(country_code, "Unknown")

    # Read CSV
    df = pd.read_csv(filename)

    # Rename XYZ columns to descriptive names
    df = df.rename(columns={
        "X": "longitude",
        "Y": "latitude",
        "Z": "population_density"
    })

    # Insert metadata columns
    df.insert(0, "country", country_name)
    df.insert(1, "year", year)

    return df