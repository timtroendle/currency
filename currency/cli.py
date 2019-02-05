import click

from currency import currency_in_dollars, deflate_monetary_value


@click.group()
def currency():
    pass


@currency.command()
@click.argument("amount", type=float)
@click.argument("currency")
@click.argument("year", type=int)
def convert(amount, currency, year):
    """Convert monetary amounts to US Dollars based on historic exchange rates."""
    try:
        result = currency_in_dollars(
            currency_value=amount,
            currency=currency,
            year=year
        )
        click.echo(result)
    except (LookupError, ValueError) as e:
        raise click.ClickException(e)


@currency.command()
@click.argument("base_amount", type=float)
@click.argument("base_year", type=int)
@click.argument("to_year", type=int)
def deflate(base_amount, base_year, to_year):
    """Deflate US Dollar value from base year to other year based on GDP."""
    try:
        result = deflate_monetary_value(
            base_value=base_amount,
            base_year=base_year,
            to_year=to_year
        )
        click.echo(result)
    except LookupError as e:
        raise click.ClickException(e)


if __name__ == "__main__":
    currency()
