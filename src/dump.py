# SPDX-FileCopyrightText: © 2023 Kevin Lu
# SPDX-Licence-Identifier: AGPL-3.0-or-later
from csv import writer
import logging
import sys
from typing import Tuple, TYPE_CHECKING

from bs4 import BeautifulSoup
from httpx import Client


if TYPE_CHECKING:
    from bs4 import Tag


def download_all(locale: str) -> str:
    prime_url = f"https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&keyword=&stype=1&ctype=&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&link_m=2&atkfr=&atkto=&deffr=&defto=&othercon=2&request_locale={locale}"
    dump_url = f"https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=2&sort=1&rp=99999&page=1&stype=1&othercon=2&page=1&request_locale={locale}"
    with Client(http2=True, follow_redirects=True, headers={"Referer": "https://www.db.yugioh-card.com/"}) as client:
        client.get(prime_url).raise_for_status()
        response = client.get(dump_url)
        response.raise_for_status()
        return response.text


def replace_text_breaks(element: "Tag") -> str:
    for br in element.find_all("br"):
        br.replace_with("\n")
    return element.text.strip()


def parse_card_text(div: "Tag") -> Tuple[str, str, str, str | None]:
    cid_input = div.select_one("input.cid")
    # Alternate: span.card_name
    name_input = div.select_one("input.cnm")
    text_dd = div.select_one("dd.box_card_text")
    pendulum_span = div.select_one("span.box_card_pen_effect")

    konami_id = cid_input["value"]
    name = name_input["value"]
    text = replace_text_breaks(text_dd)
    pendulum = replace_text_breaks(pendulum_span) if pendulum_span else None

    return konami_id, name, text, pendulum


def transform_all(html: str, output_csv: str) -> None:
    logging.log("Start HTML parse")
    soup = BeautifulSoup(html, "lxml")
    logging.log("End HTML parse")
    with open(output_csv, "w") as f:
        csv = writer(f)
        csv.writerow(["konami_id", "name", "text", "pendulum"])
        for div in soup.select("div.t_row.c_normal"):
            csv.writerow(parse_card_text(div))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} <locale> <output.csv>")

    logging.basicConfig(level=logging.INFO)
    html = download_all(sys.argv[1])
    # TODO: compute SHA256 checksum and skip if matching
    transform_all(html, sys.argv[2])
