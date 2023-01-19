# SPDX-FileCopyrightText: © 2022–2023 Kevin Lu
# SPDX-Licence-Identifier: AGPL-3.0-or-later
from typing import NamedTuple, Optional

from bs4 import BeautifulSoup
import httpx


class CardText(NamedTuple):
    name: str
    text: str
    pendulum: Optional[str]


def get_card(client: httpx.Client, konami_id: int) -> Optional[CardText]:
    """
    Parses card text from the website. HTTP errors are raised. Rate limits are recorded in client.rate_limit
    :param client: HTTPX Client. May support HTTP2 but shouldn't have defaults that majorly change behaviour.
    :param konami_id: Card to fetch.
    :return: HTTP exceptions propagated, otherwise a NamedTuple of the result.
    """
    url = f"https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&request_locale=ko&cid={konami_id}"
    response = client.get(url, follow_redirects=True)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    name_element = soup.select("#cardname > h1")
    text_element = soup.select(".CardText > .item_box_text")
    pendulum_element = soup.select(".CardText.pen > .frame.pen_effect > .item_box_text")

    if len(name_element):
        if len(name_element) > 1:
            print(f"{konami_id}\tWARNING: Multiple name tags detected, using first", flush=True)
        # Grab the first text node child and skip the remaining, which should be the English name that we don't need
        name = name_element[0].next.strip()
    else:
        print(f"{konami_id}\tWARNING: No name tags detected", flush=True)
        return None

    if len(text_element):
        if len(text_element) > 1:
            print(f"{konami_id}\tWARNING: Multiple text tags detected, using first", flush=True)
        # Remove <div class="text_title"> but preserve <br /> as newlines
        text_element[0].find("div").clear()
        for br in text_element[0].find_all("br"):
            br.replace_with("\n")
        text = text_element[0].text.strip()
    else:
        print(f"{konami_id}\tWARNING: No text tags detected", flush=True)
        return None

    if len(pendulum_element):
        if len(pendulum_element) > 1:
            print(f"{konami_id}\tWARNING: Multiple Pendulum text tags detected, using first", flush=True)
        for br in pendulum_element[0].find_all("br"):
            br.replace_with("\n")
        pendulum = pendulum_element[0].text.strip()
    else:
        pendulum = None

    return CardText(name, text, pendulum)


def get_rush(client: httpx.Client, konami_id: int) -> Optional[CardText]:
    """
    Parses card text from the website. HTTP errors are raised. Rate limits are recorded in client.rate_limit
    :param client: HTTPX Client. May support HTTP2 but shouldn't have defaults that majorly change behaviour.
    :param konami_id: Card to fetch.
    :return: HTTP exceptions propagated, otherwise a NamedTuple of the result.
    """
    url = f"https://www.db.yugioh-card.com/rushdb/card_search.action?ope=2&request_locale=ko&cid={konami_id}"
    response = client.get(url, follow_redirects=True)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    name_element = soup.select("#card_title > h1 > span")
    text_element = soup.select("#CardText .item_box_text")

    if len(name_element):
        if len(name_element) > 1:
            print(f"{konami_id}\tWARNING: Multiple name tags detected, using first", flush=True)
        name = name_element[0].next.strip()
    else:
        print(f"{konami_id}\tWARNING: No name tags detected", flush=True)
        return None

    if len(text_element):
        if len(text_element) > 1:
            print(f"{konami_id}\tWARNING: Multiple text tags detected, using first", flush=True)
        # Remove <div class="item_box_title"> but preserve <br /> as newlines
        text_element[0].find("div").clear()
        for br in text_element[0].find_all("br"):
            br.replace_with("\n")
        text = text_element[0].text.strip()
    else:
        print(f"{konami_id}\tWARNING: No text tags detected", flush=True)
        return None

    return CardText(name, text, None)
