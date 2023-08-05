import re

import typer
from cli.common.command_help import INVALID_DOMAIN_MESSAGE


def validate_domain(domain) -> str:
    regex = "^((?!-)[A-Za-z0-9-_]{1,63}(?<!_-)\\.)+[A-Za-z]{2,6}"
    domain_regex_match = re.compile(regex).match(domain)
    if not domain_regex_match or len(domain) > 255:
        raise typer.BadParameter(
            message=INVALID_DOMAIN_MESSAGE,
        )
    return domain
