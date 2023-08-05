import datetime

import pytz
from pytz import country_timezones

US_TIME_ZONES = {
    "AL": "US/Central",
    "AK": "US/Alaska",
    "AZ": "US/Mountain",
    "AR": "US/Central",
    "CA": "US/Pacific",
    "CO": "US/Mountain",
    "CT": "US/Eastern",
    "DE": "US/Eastern",
    "DC": "US/Eastern",
    "FL": "US/Eastern",
    "GA": "US/Eastern",
    "HI": "US/Hawaii",
    "ID": "US/Mountain",
    "IL": "US/Central",
    "IN": "US/Eastern",
    "IA": "US/Central",
    "KS": "US/Central",
    "KY": "US/Central",
    "LA": "US/Central",
    "ME": "US/Eastern",
    "MD": "US/Eastern",
    "MA": "US/Eastern",
    "MI": "US/Eastern",
    "MN": "US/Central",
    "MS": "US/Central",
    "MO": "US/Central",
    "MT": "US/Mountain",
    "NE": "US/Central",
    "NV": "US/Pacific",
    "NH": "US/Eastern",
    "NJ": "US/Eastern",
    "NM": "US/Mountain",
    "NY": "US/Eastern",
    "NC": "US/Eastern",
    "ND": "US/Central",
    "OH": "US/Eastern",
    "OK": "US/Central",
    "OR": "US/Pacific",
    "PA": "US/Eastern",
    "RI": "US/Eastern",
    "SC": "US/Eastern",
    "SD": "US/Central",
    "TN": "US/Central",
    "TX": "US/Central",
    "UT": "US/Mountain",
    "VT": "US/Eastern",
    "VA": "US/Eastern",
    "WA": "US/Pacific",
    "WV": "US/Eastern",
    "WI": "US/Central",
    "WY": "US/Mountain"
}

def get_datetime(country, state=None):
    if country is None:
        return None
    
    country = country.upper()
    if country == 'US' and state:
        return get_us_datetime_by_state(state)

    return get_default_datetime_by_country(country)


def get_us_datetime_by_state(state):
    date_time = None

    if state is None:
        return date_time

    try:
        state = state.upper()
        time_zone = US_TIME_ZONES.get(state)

        date_time = datetime.datetime.now(pytz.timezone(time_zone))
    except Exception as e:
        print(e)

    return date_time


def get_default_datetime_by_country(country):
    timezones = country_timezones(country)

    if not len(timezones):
        return None
    
    timezone = timezones[0]
    return datetime.datetime.now(pytz.timezone(timezone))