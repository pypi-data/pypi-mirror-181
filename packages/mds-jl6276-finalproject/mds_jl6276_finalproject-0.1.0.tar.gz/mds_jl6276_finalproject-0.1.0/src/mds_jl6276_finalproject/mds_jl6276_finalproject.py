import requests
import pandas as pd
import configparser
from . import config
import folium
from folium.plugins import MarkerCluster
def get_map(term):
    """
    Display user specified location on map in New York.

    Parameters
    ----------
    term: A category, can be 'Spanish', 'bars', 'restaurant'

    Returns
    -------
    Location of the user's search in New York City shown on map.

    Examples
    --------
    >>> from mds_jl6276_finalproject import mds_jl6276_finalproject
    >>> m = get_map('spanish')
    >>> m
    """
    api_key = config.api_key
    headers = {
      "Authorization": "Bearer " + api_key
    }
    # Set the base URL for the Yelp API
    base_url = 'https://api.yelp.com/v3/businesses/search'

    # Set the parameters for the API request
    params = {
        'term': 'restaurant' , # search for restaurants
        'location': 'New York' ,# in New York
        'limit': 50
    }
    response = requests.get(base_url, params=params, headers=headers)

    # Get the list of businesses from the response
    businesses = response.json()['businesses']

    # Append the results for the current restaurant to the results list
    df = pd.DataFrame(businesses)

    # Iterate over a list of restaurant names
    for terms in ['restaurant', 'cocktailbar', 'bar']:
        # Set the 'term' parameter to the current restaurant name
        params['term'] = terms
        for place in ['New York','long island city', 'jersey city']:
            params['location'] = place

            # Make the API request
            response = requests.get(base_url, params=params, headers=headers)

            # Get the list of businesses from the response
            businesses = response.json()['businesses']

            # Append the results for the current restaurant to the results list
            df = pd.concat([pd.DataFrame(businesses),df])
    categories = []
    for i in range(df.shape[0]):
        if type(df.iloc[i]['categories']) != type('i'):
            categories.append(df.iloc[i]['categories'][0]['alias'])
        else:
            categories.append(df.iloc[i]['categories'])

    df = df.assign(categories2 = categories)
    looking_for = df.loc[df['categories2'] == term]
    
        # Create a map centered on New York City
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=11)

    # Create a marker cluster object
    marker_cluster = MarkerCluster().add_to(m)

    # Add a marker for each business
    for b in range(looking_for.shape[0]):
        folium.Marker(
            location=[looking_for.iloc[b]['coordinates']['latitude'], looking_for.iloc[b]['coordinates']['longitude']],popup=looking_for.iloc[b]['name']).add_to(marker_cluster)

    # Display the map
    if looking_for.shape[0] == 0:
        return None
    return m

