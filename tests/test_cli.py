import math

import pytest
from click.testing import CliRunner

from currency import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_help(runner):
    help_result = runner.invoke(cli.currency, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_currency_conversion(runner):
    result = runner.invoke(cli.convert, ['14', 'USD', 'USD', '2009'])
    assert result.exit_code == 0
    assert math.isclose(float(result.output), 14)


def test_unsupported_currency(runner):
    result = runner.invoke(cli.convert, ['76', 'PDB', 'USD', '2006'])
    assert result.exit_code != 0
    assert "Currency PDB is not supported." in result.output


@pytest.mark.parametrize('unavailable_year', ['1980', '2080'])
def test_no_exchange_rate_available(runner, unavailable_year):
    result = runner.invoke(cli.convert, ['16', 'EUR', 'USD', unavailable_year])
    assert result.exit_code != 0
    assert "Cannot convert" in result.output


def test_currency_deflation(runner):
    result = runner.invoke(cli.deflate, ['15', 'USD', '2009', '2009'])
    assert result.exit_code == 0
    assert math.isclose(float(result.output), 15)


def test_no_deflator_available(runner):
    result = runner.invoke(cli.deflate, ['15', 'USD', '2009', '2090'])
    assert result.exit_code != 0


def test_convert_and_deflate_through_usd(runner):
    result = runner.invoke(cli.convert_usd, ['99', 'EUR', 'EUR', '2009', '2009'])
    assert result.exit_code == 0
    assert math.isclose(float(result.output), 99)
