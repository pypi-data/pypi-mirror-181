#
#  Used to fetch the stats url and determine if
#  aprsd server is 'healthy'
#
#
# python included libs
import datetime
import json
import logging
import sys

import click
import requests
from rich.console import Console

import aprsd
from aprsd import cli_helper, utils
# local imports here
from aprsd.aprsd import cli


# setup the global logger
# logging.basicConfig(level=logging.DEBUG) # level=10
LOG = logging.getLogger("APRSD")
console = Console()


@cli.command()
@cli_helper.add_options(cli_helper.common_options)
@click.option(
    "--url",
    "health_url",
    show_default=True,
    default="http://localhost:8001/stats",
    help="The aprsd url to call for checking health/stats",
)
@click.option(
    "--timeout",
    show_default=True,
    default=3,
    help="How long to wait for healtcheck url to come back",
)
@click.pass_context
@cli_helper.process_standard_options_no_config
def healthcheck(ctx, health_url, timeout):
    """Check the health of the running aprsd server."""
    console.log(f"APRSD HealthCheck version: {aprsd.__version__}")
    with console.status(f"APRSD HealthCheck version: {aprsd.__version__}") as status:
        try:
            status.update(f"Contacting APRSD on {health_url}")
            url = health_url
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
        except Exception as ex:
            console.log(f"Failed to fetch healthcheck url '{url}' : '{ex}'")
            sys.exit(-1)
        else:
            status.update("Contacted APRSD. Parsing results.")
            stats = json.loads(response.text)
            email_thread_last_update = stats["stats"]["email"]["thread_last_update"]

            if email_thread_last_update != "never":
                delta = utils.parse_delta_str(email_thread_last_update)
                d = datetime.timedelta(**delta)
                max_timeout = {"hours": 0.0, "minutes": 5, "seconds": 0}
                max_delta = datetime.timedelta(**max_timeout)
                if d > max_delta:
                    console.log(f"Email thread is very old! {d}")
                    sys.exit(-1)

            aprsis_last_update = stats["stats"]["aprs-is"]["last_update"]
            delta = utils.parse_delta_str(aprsis_last_update)
            d = datetime.timedelta(**delta)
            max_timeout = {"hours": 0.0, "minutes": 5, "seconds": 0}
            max_delta = datetime.timedelta(**max_timeout)
            if d > max_delta:
                LOG.error(f"APRS-IS last update is very old! {d}")
                sys.exit(-1)

            sys.exit(0)
