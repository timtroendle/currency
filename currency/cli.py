import click

import currency as cu


class Currency(click.ParamType):

    name = "currency"

    def convert(self, value, param, ctx):
        if value.lower() in [currency.alpha_3 for currency in cu.SUPPORTED_CURRENCIES]:
            return value
        else:
            self.fail(f"Currency {value} is not supported.")


@click.group()
def currency():
    pass


@currency.command()
@click.argument("amount", type=float)
@click.argument("from_currency", type=Currency())
@click.argument("to_currency", type=Currency())
@click.argument("year", type=int)
def convert(amount, from_currency, to_currency, year):
    """Convert monetary amounts to other currency based on historic exchange rates."""
    try:
        result = cu.convert(
            amount=amount,
            from_currency=from_currency,
            to_currency=to_currency,
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
        result = cu.deflate_monetary_value(
            base_value=base_amount,
            base_year=base_year,
            to_year=to_year
        )
        click.echo(result)
    except LookupError as e:
        raise click.ClickException(e)


if __name__ == "__main__":
    currency()
