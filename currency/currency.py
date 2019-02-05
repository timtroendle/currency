"""Normalising currency values."""
from typing import NamedTuple
from pathlib import Path

import numpy as np
import pandas as pd

PATH_TO_DATA = Path(__file__).parent / ".." / "data"
PATH_TO_EXCHANGE_RATES = PATH_TO_DATA / "exchange-rates" / "API_PA.NUS.FCRF_DS2_en_csv_v2_10322214.csv"
PATH_TO_DEFLATOR = PATH_TO_DATA / "gdp-deflator" / "API_NY.GDP.DEFL.ZS_DS2_en_csv_v2.csv"
EXCHANGE_RATE_TIME_SERIES = (
    pd.read_csv(PATH_TO_EXCHANGE_RATES, skiprows=4)
      .iloc[:, :-1]
      .set_index("Country Name")
      .transpose()
      .drop(index=["Indicator Name", "Indicator Code", "Country Code"])
      .rename(index=lambda x: int(x))
      .astype(np.float32)
)
DEFLATOR = (
    pd.read_csv(PATH_TO_DEFLATOR, skiprows=4)
      .iloc[:, :-1]
      .set_index("Country Name")
      .transpose()
      .drop(index=["Indicator Name", "Indicator Code", "Country Code"])
      .rename(index=lambda x: int(x))
      .astype(np.float32)
)


class Currency(NamedTuple):
    alpha_3: str
    iso_4217: int
    country: str


SUPPORTED_CURRENCIES = [
    Currency('bgn', 975, "Bulgaria"),
    Currency('eur', 978, "Euro area"),
    Currency('nad', 516, "Namibia"),
    Currency('usd', 840, "United States"),
    Currency('dzd', 12, "Algeria"),
    Currency('ars', 32, "Argentina"),
    Currency('amd', 51, "Armenia"),
    Currency('aud', 36, "Australia"),
    Currency('azn', 944, "Azerbaijan"),
    Currency('bam', 977, "Bosnia and Herzegovina"),
    Currency('brl', 986, "Brazil"),
    Currency('cad', 124, "Canada"),
    Currency('cny', 156, "China"),
    Currency('hrk', 191, "Croatia"),
    Currency('czk', 203, "Czech Republic"),
    Currency('dkk', 208, "Denmark"),
    Currency('egp', 818, "Egypt, Arab Rep."),
    Currency('eek', 233, "Estonia"),
    Currency('ghs', 936, "Ghana"),
    Currency('huf', 348, "Hungary"),
    Currency('inr', 356, "India"),
    Currency('idr', 360, "Indonesia"),
    Currency('irr', 364, "Iran, Islamic Rep."),
    Currency('ils', 376, "Israel"),
    Currency('jpy', 392, "Japan"),
    Currency('jod', 400, "Jordan"),
    Currency('kzt', 398, "Kazakhstan"),
    Currency('krw', 410, "Korea, Rep."),
    Currency('chf', 756, "Switzerland"),
    Currency('ltl', 440, "Lithuania"),
    Currency('myr', 458, "Malaysia"),
    Currency('mur', 480, "Mauritius"),
    Currency('mdl', 498, "Moldova"),
    Currency('mad', 504, "Morocco"),
    Currency('mzn', 943, "Mozambique"),
    Currency('ngn', 566, "Nigeria"),
    Currency('nok', 578, "Norway"),
    Currency('pkr', 586, "Pakistan"),
    Currency('php', 608, "Philippines"),
    Currency('pln', 985, "Poland"),
    Currency('skk', 703, "Slovak Republic"),
    Currency('sit', 705, "Slovenia"),
    Currency('zar', 710, "South Africa"),
    Currency('esp', 724, "Spain"),
    Currency('lkr', 144, "Sri Lanka"),
    Currency('sek', 752, "Sweden"),
    Currency('tzs', 834, "Tanzania"),
    Currency('thb', 764, "Thailand"),
    Currency('tnd', 788, "Tunisia"),
    Currency('gbp', 826, "United Kingdom"),
    Currency('vuv', 548, "Vanuatu"),
    Currency('vnd', 704, "Vietnam"),
    Currency('thb', 764, "Thailand"),
    Currency('dem', 276, "Germany"),
    Currency('frf', 250, "France"),
    Currency('sar', 682, "Saudi Arabia")
]

CURRENCY_TO_COUNTRY_MAP = {
    currency.alpha_3: currency.country for currency in SUPPORTED_CURRENCIES
}


def convert(amount, from_currency, to_currency, year, exchange_rates=EXCHANGE_RATE_TIME_SERIES):
    """Convert monetary amounts to other currencies based on historic exchange rates to US Dollars.

    By default, the data stems from IMF:
    https://data.worldbank.org/indicator/PA.NUS.FCRF
    but you can also inject your own timeseries, see below.

    Parameters:
        * amount: (float) amount to convert
        * from_currency: alpha_3 code of source currency
        * to_currency: alpha_3 code of target currency
        * year: the year of the source amount
        * exchange_rates: by default IMF data, but other can be injected

    Returns:
        the monetary amount in target currency

    """
    amount_in_dollar = currency_in_dollars(
        currency_value=amount,
        currency=from_currency,
        year=year
    )
    dollar_per_target_currency = currency_in_dollars(
        currency_value=1,
        currency=to_currency,
        year=year
    )
    return amount_in_dollar / dollar_per_target_currency


def currency_in_dollars(currency_value, currency, year, exchange_rates=EXCHANGE_RATE_TIME_SERIES):
    """Convert monetary amounts to US Dollars based on historic exchange rates.

    By default, the data stems from IMF:
    https://data.worldbank.org/indicator/PA.NUS.FCRF
    but you can also inject your own timeseries, see below.

    Parameters:
        * currency_value: (float) amount to convert
        * currency: alpha_3 code of source currency
        * year: the year of the source amount
        * exchange_rates: by default IMF data, but other can be injected

    Returns:
        the monetary amount in US dollars

    """
    assert isinstance(currency, str), "Currency must be given as a string."
    currency = currency.lower()
    if currency not in [currency.alpha_3 for currency in SUPPORTED_CURRENCIES]:
        raise ValueError(f"Currency {currency.upper()} is not supported.")
    country = CURRENCY_TO_COUNTRY_MAP[currency]
    try:
        exchange_rate = exchange_rates.loc[year, country]
        if np.isnan(exchange_rate):
            raise LookupError()
    except LookupError:
        raise LookupError(f"Data of year {year} for country {country} not available. "
                          f"Cannot convert {currency_value} {currency.upper()}.")
    return currency_value / exchange_rate


def deflate_monetary_value(base_value, base_year, to_year, deflator=DEFLATOR):
    """Deflate US Dollar value from base year to other year based on GDP.

    By default uses a deflator published by the Worldbank:
    https://data.worldbank.org/indicator/NY.GDP.DEFL.ZS
    but you can also inject your own timeseries, see below.

    Parameters:
        * base_value: the monetary amount in US Dollars in the base year
        * base_year: the year for which the monetary value is given
        * to_year: the year to which the base value should be transformed
        * deflator: by default Worldbank data, but other can be injected

    Returns:
        the monetary value from the base year deflated to the other year

    """
    country = CURRENCY_TO_COUNTRY_MAP["usd"]
    try:
        base = deflator.loc[base_year, country]
        to = deflator.loc[to_year, country]
    except LookupError:
        raise LookupError(f"Data for year {base_year} or {to_year} not available. "
                          f"Cannot deflate {base_value} USD{base_year} to year {to_year}.")
    return base_value * to / base
