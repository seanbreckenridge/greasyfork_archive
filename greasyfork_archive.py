import sys
import json
import time
from typing import List, Callable, Mapping

import click
import requests
import bs4
import backoff

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0"
)
BASE_GREASYFORK_URL = "https://greasyfork.org"
BASE_GREASYFORK_ENGLISH_URL = f"{BASE_GREASYFORK_URL}/en"
BASE_USER_URL = f"{BASE_GREASYFORK_ENGLISH_URL}/users"
get_user_url: Callable = lambda user_id: f"{BASE_USER_URL}/{user_id}"


def backoff_hdlr(details):
    click.echo(
        "Backing off {wait:0.1f} seconds afters {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details),
        err=True,
    )


@backoff.on_exception(
    backoff.constant,
    requests.exceptions.RequestException,
    interval=5,
    max_tries=3,
    jitter=None,
    on_backoff=backoff_hdlr,
)
def request_url(url: str) -> requests.Response:
    time.sleep(2)
    resp: requests.Response = requests.get(url, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    return resp


class UserScript:
    """
    takes an HTML li userscipt element as input and converts
    extracts data from it
    """

    attrs = [
        "script_name",
        "script_authors",
        "daily_installs",
        "total_installs",
        "rating_score",
        "created_date",
        "updated_date",
        "script_type",
        "script_version",
        "sensitive",
        "language",
        "css_available_as_js",
        "description",
        "url",
        "code",
    ]

    def __init__(self, userscript_list_element: bs4.element.PageElement):
        self.el = userscript_list_element

        links = self.el.find_all("a", href=True)
        assert len(links) >= 1
        self.url = f"{BASE_GREASYFORK_URL}/{links[0]['href']}"
        description = self.el.find_all("span", {"class": "description"})
        assert len(description) == 1
        self.description = description[0].text.strip()

        try:
            self.script_id: int = int(self.el["data-script-id"])
            self.script_name: str = self.el["data-script-name"]
            self.script_authors: Mapping[int, str] = json.loads(
                self.el["data-script-authors"]
            )
            self.daily_installs: int = int(self.el["data-script-daily-installs"])
            self.total_installs: int = int(self.el["data-script-total-installs"])
            self.rating_score: float = float(self.el["data-script-rating-score"])
            self.created_date: str = self.el["data-script-created-date"]
            self.updated_date: str = self.el["data-script-updated-date"]
            self.script_type: str = self.el["data-script-type"]
            self.script_version: str = self.el["data-script-version"]
            self.sensitive: bool = self.el["data-sensitive"] == "true"
            self.language: str = self.el["data-script-language"]
            self.css_available_as_js: bool = self.el[
                "data-css-available-as-js"
            ] == "true"
        except KeyError as k:
            click.echo(
                "Could not find data-attribute '{}' in list element".format(str(k)),
                err=True,
            )
            sys.exit(1)
        self.code = request_url(self.get_raw_script_code_link()).text

    def __repr__(self) -> str:
        assert self.__class__.attrs is not None  # type: ignore

        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                [
                    "{}={}".format(a, repr(getattr(self, a, None)))
                    for a in self.__class__.attrs  # type: ignore
                ]
            ),
        )

    def __str__(self) -> str:
        return self.__repr__()

    def to_dict(self) -> str:
        return {k: getattr(self, k) for k in self.__class__.attrs}

    @property
    def code_url(self) -> str:
        return f"{self.url}/code"

    def get_raw_script_code_link(self) -> str:
        resp: requests.Response = request_url(self.code_url)
        code_soup = bs4.BeautifulSoup(resp.text, "html.parser")
        install_links: List[bs4.element.PageElement] = code_soup.find_all(
            "a", attrs={"class": "install-link"}, href=True
        )
        assert len(install_links) >= 1
        return f"{BASE_GREASYFORK_URL}/{install_links[0]['href']}"


def get_user_scripts(user_url: str) -> List[bs4.element.PageElement]:
    """Request and select the li items representing each script"""
    user_page: requests.Response = request_url(user_url)
    user_soup: bs4.BeautifulSoup = bs4.BeautifulSoup(user_page.text, "html.parser")
    script_items: List[bs4.element.PageElement] = user_soup.select(
        "ol#user-script-list > li"
    )
    return script_items


def main_wrapper(greasyfork_user_id: int, output_file: str):
    script_html_elements: List[bs4.element.PageElement] = get_user_scripts(
        get_user_url(greasyfork_user_id)
    )
    script_items: List[UserScript] = list(
        map(lambda el: UserScript(el), script_html_elements)
    )
    json_dict: Mapping = {
        "greasyfork_scripts": list(map(lambda s: s.to_dict(), script_items))
    }
    if output_file:
        with open(output_file, "w") as jf:
            json.dump(json_dict, jf)
    else:
        print(json.dumps(json_dict))
    return 0


@click.command()
@click.argument("GREASYFORK_USER_ID", required=True, type=int)
@click.option(
    "--output-file",
    required=True,
    type=click.Path(),
    help="JSON filepath to output scraped data to",
)
def main(greasyfork_user_id: int, output_file: str):
    sys.exit(main_wrapper(greasyfork_user_id, output_file))
