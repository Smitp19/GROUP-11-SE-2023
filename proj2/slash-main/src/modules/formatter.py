"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com
"""

"""
The formatter module focuses on processing raw text and returning it in 
the required format. 
"""

from datetime import datetime
import math
import requests
from ast import literal_eval

CURRENCY_URL = "https://api.exchangerate-api.com/v4/latest/usd"
EXCHANGES = literal_eval(requests.get(CURRENCY_URL).text)


def formatResult(
    website, titles, prices, links, ratings, num_ratings, trending, df_flag, currency
):
    """
    The formatResult function takes the scraped HTML as input, and extracts the
    necessary values from the HTML code. Ex. extracting a price '$19.99' from
    a paragraph tag.
    Parameters: titles- scraped titles of the products, prices- scraped prices of the products,
    links- scraped links of the products on the respective e-commerce sites,
    ratings-scraped ratings of the product
    Returns: A dictionary of all the parameters stated above for the product
    """

    title, price, link, rating, num_rating, converted_cur, trending_stmt = (
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    )
    if titles:
        title = titles[0].get_text().strip()
    if prices:
        price = prices[0].get_text().strip()
    if "$" not in price:
        price = "$" + price
    if links:
        link = links[0]["href"]
    if ratings:
        rating = float(ratings[0].get_text().strip().split()[0])
    if trending:
        trending_stmt = trending.get_text().strip()
    if num_ratings:
        if isinstance(num_ratings, int):
            num_rating = num_ratings
        else:
            num_ratings = (
                num_ratings[0]
                .get_text()
                .replace(")", "")
                .replace("(", "")
                .replace(",", "")
            )
            num_rating = num_ratings.strip()
    # if df_flag==0: title=formatTitle(title)
    # if df_flag==0: link=formatTitle(link)
    if currency:
        converted_cur = getCurrency(currency, price)
    product = {
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "title": title,
        "price": price,
        "link": f"www.{website}.com{link}",
        "website": website,
        "rating": rating,
        "no of ratings": num_rating,
        "trending": trending_stmt,
        "converted price": converted_cur,
    }

    return product


def sortList(arr, sortBy, reverse):
    """It sorts the products list based on the flags provided as arguements. Currently, it supports sorting by price.
    Parameters- SortBy- "pr": sorts by price, SortBy- "ra": sorts by rating
    Returns- Sorted list of the products based on the parameter requested by the user
    """
    if sortBy == "pr":
        return arr.sort_values(
            key=lambda x: x.apply(lambda y: getNumbers(y)),
            by=["price"],
            ascending=False,
        )
    # Fix Rating sort
    elif sortBy == "ra":
        arr["rating"] = arr["rating"].apply(lambda x: None if x == "" else float(x))
        return arr.sort_values(by=["rating"], ascending=False)
    return arr


def formatSearchQuery(query):
    """It formats the search string into a string that can be sent as a url paramenter."""
    return query.replace(" ", "+")


def formatTitle(title):
    """It formats titles extracted from the scraped HTML code."""
    if len(title) > 40:
        return title[:40] + "..."
    return title


def getNumbers(st):
    """It extracts float values for the price from a string.
    Ex. it extracts 10.99 from '$10.99' or 'starting at $10.99'
    """
    st = str(st)
    ans = ""
    for ch in st:
        if (ch >= "0" and ch <= "9") or ch == ".":
            ans += ch
    try:
        ans = float(ans)
    except:
        ans = 0
    return ans


def getCurrency(currency, price):
    """
    The getCurrency function converts the prices listed in USD to user specified currency.
    Currently it supports INR, EURO, AUD, YUAN, YEN, POUND
    """

    converted_cur = 0.0
    if len(price) > 1:
        if currency == "inr":
            converted_cur = EXCHANGES["rates"]["INR"] * int(
                price[(price.index("$") + 1) : price.index(".")].replace(",", "")
            )
        elif currency == "euro":
            converted_cur = EXCHANGES["rates"]["EUR"] * int(
                price[(price.index("$") + 1) : price.index(".")].replace(",", "")
            )
        elif currency == "aud":
            converted_cur = EXCHANGES["rates"]["AUD"] * int(
                price[(price.index("$") + 1) : price.index(".")].replace(",", "")
            )
        elif currency == "yuan":
            converted_cur = EXCHANGES["rates"]["CNY"] * int(
                price[(price.index("$") + 1) : price.index(".")].replace(",", "")
            )
        elif currency == "yen":
            converted_cur = EXCHANGES["rates"]["JPY"] * int(
                price[(price.index("$") + 1) : price.index(".")].replace(",", "")
            )
        elif currency == "pound":
            converted_cur = EXCHANGES["rates"]["GBP"] * int(
                price[(price.index("$") + 1) : price.index(".")].replace(",", "")
            )
        converted_cur = currency.upper() + " " + str(round(converted_cur, 2))
    return converted_cur
