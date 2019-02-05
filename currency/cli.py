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
@click.argument("currency", type=Currency())
@click.argument("base_year", type=int)
@click.argument("target_year", type=int)
def deflate(base_amount, currency, base_year, target_year):
    """Deflate monetary value from base year to target year based on GDP."""
    try:
        result = cu.deflate_monetary_value(
            base_value=base_amount,
            currency=currency,
            base_year=base_year,
            to_year=target_year
        )
        click.echo(result)
    except LookupError as e:
        raise click.ClickException(e)


@currency.command()
@click.argument("amount", type=float)
@click.argument("from_currency", type=Currency())
@click.argument("to_currency", type=Currency())
@click.argument("base_year", type=int)
@click.argument("target_year", type=int)
def convert_usd(amount, from_currency, to_currency, base_year, target_year):
    """Convert monetary amounts using US inflation."""
    try:
        result = cu.convert_through_usd(
            amount=amount,
            from_currency=from_currency,
            to_currency=to_currency,
            base_year=base_year,
            target_year=target_year
        )
        click.echo(result)
    except LookupError as e:
        raise click.ClickException(e)


if __name__ == "__main__":
    currency()
