"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com

"""

from src.modules import formatter
from bs4 import BeautifulSoup


def test_formatResults():
    """
    Checks the formatResults function
    """
    titles = [BeautifulSoup('<div class="someclass">title  </div>', "html.parser")]
    prices = [BeautifulSoup('<div class="someclass">$0.99  </div>', "html.parser")]
    links = []

    product = formatter.formatResult(
        "example", titles, prices, links, "", 0, "", None, None
    )
    ans = {"title": "title", "price": "$0.99", "website": "example"}
    print(product["website"], ans["website"])

    assert (
        product["title"] == ans["title"]
        and product["price"] == ans["price"]
        and product["website"] == ans["website"]
    )
