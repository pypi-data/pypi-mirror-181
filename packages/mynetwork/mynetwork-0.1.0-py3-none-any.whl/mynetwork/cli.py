#!/usr/bin/env python3
import click
from mynetwork.myip.myip import ip


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


cli.add_command(ip, "ip")


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
