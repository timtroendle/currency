import math

import pytest

from currency import currency_in_dollars, convert, convert_through_usd, deflate_monetary_value, SUPPORTED_CURRENCIES


@pytest.mark.parametrize(
    'currency, year',
    [(currency.alpha_3, 1998 if currency.alpha_3 != "eur" else 2000)
     for currency in SUPPORTED_CURRENCIES]
)
def test_positiv_amount_yields_positive_dollar_amount(currency, year):
    currency_value = 3.2
    dollar_value = currency_in_dollars(currency_value, currency, year=year)
    assert dollar_value > 0


@pytest.mark.parametrize(
    'currency, year',
    [(currency.alpha_3, 1998 if currency.alpha_3 != "eur" else 2000)
     for currency in SUPPORTED_CURRENCIES]
)
def test_negative_amount_yields_negative_dollar_amount(currency, year):
    currency_value = -5.7
    dollar_value = currency_in_dollars(currency_value, currency, year=year)
    assert dollar_value < 0


@pytest.mark.parametrize(
    'value, year',
    [(value, year)
     for value in [-100023, -345, -1.2, 0, 4.5, 45.6, 234125.2]
     for year in range(1960, 2016)]
)
def test_identity_function_for_dollars(value, year):
    assert math.isclose(value, currency_in_dollars(value, "usd", year=year), abs_tol=0.01)


@pytest.mark.parametrize('year', range(2008, 2017))
def test_euro_above_dollar(year):
    dollar_value = currency_in_dollars(1, "eur", year=year)
    assert 1 < dollar_value < 2


@pytest.mark.parametrize('year', range(2008, 2017))
def test_100_yen_roughly_1_dollars(year):
    dollar_value = currency_in_dollars(100, "jpy", year=year)
    assert 0.75 < dollar_value < 1.30


@pytest.mark.parametrize('year', range(2008, 2017))
def test_pound_up_to_2_times_dollar(year):
    dollar_value = currency_in_dollars(1, "gbp", year=year)
    assert 1 < dollar_value < 2


def test_iranian_rial_to_dollar():
    irr = 4628
    year = 2016
    assert 0.1 < currency_in_dollars(irr, "irr", year=year) < 0.2


@pytest.mark.parametrize('year', range(2009, 2015))
def test_150_nigerian_naira_roughly_1_dollar(year):
    dollar_value = currency_in_dollars(150, "ngn", year=year)
    assert 0.8 < dollar_value < 1.2


@pytest.mark.parametrize('year', range(2009, 2015))
def test_between_5_and_10_egyptian_pound_per_dollar(year):
    dollar_value = currency_in_dollars(1, "egp", year=year)
    assert 0.1 < dollar_value < 0.2


@pytest.mark.parametrize('year', range(2000, 2015))
def test_convert_identity(year):
    amount = 10
    identity = convert(amount=amount, base_currency="eur", target_currency="eur", year=year)
    assert math.isclose(identity, amount)


@pytest.mark.parametrize('year', range(2010, 2017))
def test_pound_up_to_50pct_stronger_than_eur(year):
    eur = convert(amount=1, base_currency="gbp", target_currency="eur", year=year)
    assert 1 < eur < 1.5


def test_convert_through_usd_without_time_is_convert():
    through_usd = convert_through_usd(
        amount=1,
        base_currency="gbp",
        target_currency="eur",
        base_year=2009,
        target_year=2009
    )
    normal = convert(
        amount=1,
        base_currency="gbp",
        target_currency="eur",
        year=2009
    )
    assert math.isclose(through_usd, normal)


def test_convert_through_usd():
    eur2009 = convert_through_usd(
        amount=1,
        base_currency="gbp",
        target_currency="eur",
        base_year=2009,
        target_year=2009
    )
    eur2010 = convert_through_usd(
        amount=1,
        base_currency="gbp",
        target_currency="eur",
        base_year=2009,
        target_year=2010
    )
    assert eur2010 > eur2009


@pytest.mark.parametrize(
    'year',
    [year for year in range(1960, 2016)]
)
def test_no_inflation_in_same_year(year):
    base_value = 1.1
    current_value = deflate_monetary_value(
        currency="USD",
        base_value=base_value,
        base_year=year,
        target_year=year
    )
    assert math.isclose(base_value, current_value, abs_tol=0.01)


@pytest.mark.parametrize(
    'year, currency',
    [(year, currency)
     for year in range(1970, 2015)
     for currency in ["USD", "EGP"]]
)
def test_inflation_is_steadily_rising(year, currency):
    base_value = 1.1
    current_value = deflate_monetary_value(
        currency=currency,
        base_value=base_value,
        base_year=year,
        target_year=year + 1
    )
    assert current_value > base_value
