import click

from lib.autumn8.cli_environment import CliEnvironment
from lib.cli.commands import login, submit_model
from lib.cli.interactive import fetch_user_data
from lib.common._version import __version__


@click.option(
    "-e",
    "--environment",
    "--env",
    type=click.Choice(CliEnvironment.__members__, case_sensitive=False),
    default="production",
    callback=lambda c, p, v: getattr(CliEnvironment, v),
    help="Environment to use",
)
def test_connection(environment):
    user_data = fetch_user_data(environment)
    print(f"Hello! You're authenticated as {user_data['email']}")


@click.group()
@click.version_option(version=__version__)
def main():
    pass


main.command()(submit_model)
main.command()(test_connection)
main.command()(login)

if __name__ == "__main__":
    main()
