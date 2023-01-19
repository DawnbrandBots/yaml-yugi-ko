# SPDX-FileCopyrightText: © 2022–2023 Kevin Lu
# SPDX-Licence-Identifier: AGPL-3.0-or-later
import json
import os
import sys
import time
from typing import Any, Dict, Optional

from httpx import Client, HTTPStatusError, RequestError
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

from scraper import get_card


def get_card_retry(client: Client, konami_id: int, database: str) -> Optional[Dict[str, Any]]:
    for retry in range(5):
        try:
            card = get_card(client, konami_id, database)
            if card:
                return card._asdict()
            else:
                print(f"{konami_id}\tNOT FOUND", flush=True)
                return
        except HTTPStatusError as e:
            print(f"{konami_id}\tTRY {retry}\tFAIL {e.response.status_code}", flush=True)
            if e.response.is_server_error:
                time.sleep(1)
            else:
                return
        except RequestError as e:
            print(f"{konami_id}\tTRY {retry}\t{e}", flush=True)
            time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} <yugiohdb|rushdb> <cards.json> [output directory]")

    target = sys.argv[1]
    file = sys.argv[2]
    with open(file) as handle:
        cards = json.load(handle)
    print(f"Found {len(cards)} cards.", flush=True)
    ids = [card["konami_id"] for card in cards if card.get("konami_id")]
    print(f"Using {len(cards)} ids.", flush=True)

    if len(sys.argv) > 3:
        os.chdir(sys.argv[3])

    with Client(http2=True) as client:
        yaml = YAML()
        for kid in ids:
            if os.path.exists(f"{kid}.yaml"):
                print(f"{kid}\tSKIP", flush=True)
                continue

            card = get_card_retry(client, kid, target)
            if card is None:
                continue

            card["text"] = LiteralScalarString(card["text"])
            if card["pendulum"]:
                card["pendulum"] = LiteralScalarString(card["pendulum"])
            else:
                card.pop("pendulum")

            with open(f"{kid}.yaml", mode="w", encoding="utf-8") as out:
                yaml.dump(card, out)
            print(f"{kid}.yaml", flush=True)
            time.sleep(1)
