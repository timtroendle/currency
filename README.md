# Currency Converter

[![Build Status](https://travis-ci.org/timtroendle/currency.svg)](https://travis-ci.org/timtroendle/currency)

A time aware tool to convert currencies.

## User Guide

currency has the following features:

* convert between currencies at a particular point in time (to US Dollar only)
* convert between the same currency in different points in time (US Dollar only)

### Installation

Assuming you have `pip` and `Git` installed you can install the development version directly
from GitHub.

```bash
pip install git+git://github.com/timtroendle/currency@develop
```

### Usage Example

...

## Developer Guide

### Installation

Best install `currency` in editable mode:

    $ pip install -r requirements-test.txt

### Run the test suite

Run the test suite with py.test:

    $ py.test

## Data Sources

This repository contains a dataset on "Official exchange rate (LCU per US$, period average)" by the International Monetary Fund, International Financial Statistics ([PA.NUS.FCRF](https://data.worldbank.org/indicator/PA.NUS.FCRF)). It is originally CC BY-4.0 licensed and has been added to this repository without any modifications. The version of the dataset is from 2018-11-14.

This repository contains a dataset on "GDP deflator (base year varies by country)" by World Bank national accounts data, and OECD National Accounts data files. ([NY.GDP.DEFL.ZS](https://data.worldbank.org/indicator/NY.GDP.DEFL.ZS)). It is originally CC BY-4.0 licensed and has been added to this repository without any modifications. The version of the dataset is from 2018-05-02.
