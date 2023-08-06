import click

from autumn8.cli.commands import login, submit_model, use_environment_option
from autumn8.cli.interactive import fetch_user_data
from autumn8.common._version import __version__


@use_environment_option
def test_connection(environment):
    """
    Test connection to the autumn8.ai service, using the configured API key.
    Displays the user's email address upon successful connection.
    """
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
