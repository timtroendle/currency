# Currency Converter

[![Build Status](https://travis-ci.org/timtroendle/currency.svg)](https://travis-ci.org/timtroendle/currency)

A time aware tool to convert currencies.

With `currency` you can convert between currencies at particular points in time, and you can convert between different points in time for a particular currency.

## User Guide

### Installation

Assuming you have `pip` and `Git` installed you can install the development version directly
from GitHub.

```bash
pip install git+git://github.com/timtroendle/currency@develop
```

### Usage Example

```bash
$ currency convert 14 EUR GBP 2009 # convert 14 EUR2009 to GBP2009
$ currency deflate 12.5 GBP 2009 2016 # deflate 12.5 GBP2009 to GBP2016
$ currency convert-usd 14 EUR GBP 2009 2016 # do both at the same time, using US inflation
```

Comparing different monetary values from different points in time is difficult, as the choice
of currency for deflation is both arbitrary and influential. The `convert-usd` command
always uses US deflation data and that yields different results as using deflation data from Brazil
for example.

## Developer Guide

### Installation

Best install `currency` in editable mode:

    $ pip install -r requirements-test.txt

### Run the test suite

Run the test suite with py.test:

    $ py.test

## Data Sources

This repository contains a dataset on "Official exchange rate (LCU per US$, period average)" by the International Monetary Fund, International Financial Statistics ([PA.NUS.FCRF](https://data.worldbank.org/indicator/PA.NUS.FCRF)). It is originally CC BY-4.0 licensed and has been added to this repository without any modifications. The version of the dataset is from 2018-11-14.

This repository contains a dataset on "GDP deflator (base year varies by country)" by World Bank national accounts data, and OECD National Accounts data files. ([NY.GDP.DEFL.ZS](https://data.worldbank.org/indicator/NY.GDP.DEFL.ZS)). It is originally CC BY-4.0 licensed and has been added to this repository without any modifications. The version of the dataset is from 2019-01-30.
