# SPDX-FileCopyrightText: © 2022 Kevin Lu
# SPDX-Licence-Identifier: AGPL-3.0-or-later
import sys

from httpx import Client

from scraper import get_card


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with Client(http2=True) as client:
            for kid in sys.argv[1:]:
                print(get_card(client, kid))
