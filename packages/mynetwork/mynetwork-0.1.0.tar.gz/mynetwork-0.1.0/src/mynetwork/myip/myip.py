import requests
import click


def public_ip() -> requests.Response:
    return requests.get('https://wgetip.com')


@click.command()
def ip():
    response = public_ip()
    print(response.text)
