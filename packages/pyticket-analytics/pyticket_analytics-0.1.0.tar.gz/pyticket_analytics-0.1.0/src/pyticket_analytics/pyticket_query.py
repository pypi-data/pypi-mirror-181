import pandas as pd
import numpy as np
import datetime as dt
import requests
import json

def pyticket_query(keyword,apikey,start_date=dt.datetime.today() - dt.timedelta(30),sort='date,asc'):
    """
    This function generate query based on keyword and filtered date accessed through python
    """
    # Reformat arguments
    key = apikey

    # Date adjustment, standardized as API format
    start_date = str(start_date.date()) + 'T00:00:00Z'

    keywordx = str(keyword.replace(' ', '%20'))

    # Generate customize URL
    url = f'https://app.ticketmaster.com/discovery/v2/events?apikey={key}&keyword={keywordx}&locale=*&startDateTime={start_date}&sort={sort}&size=200'

    # Requesting by query
    r = requests.get(url)
    stats = r.status_code

    # Storing JSON
    event = r.json()

    # Parsing JSON to csv
    event_df = pd.DataFrame(event['_embedded']['events'])

    # Cleaning Dataset
    ## Unpacking price type, currency, price_min, price_max, city, lon-lat, genre, and segment
    event_df['price'] = event_df.priceRanges.dropna().apply(pd.Series)[0]
    event_df[['price_type','currency','price_min','price_max']] = event_df.price.dropna().apply(pd.Series)
    event_df['genre'] = event_df.classifications.apply(pd.Series)[0].apply(pd.Series).genre.apply(pd.Series)['name']
    event_df['segment'] = event_df.classifications.apply(pd.Series)[0].apply(pd.Series).segment.apply(pd.Series)['name']

    ## Getting startdate and enddate of sales
    event_df['startdate'] = None
    event_df['enddate'] = None
    for x in range(len(event_df)):
        event_df['startdate'][x] = event_df.sales[x].get('public').get('startDateTime')
        event_df['enddate'][x] = event_df.sales[x].get('public').get('endDateTime')
    
    print('The request status is: {stats}')
    print('This is the top observation of keyword: {keyword}')
    print(url)
    return event_df