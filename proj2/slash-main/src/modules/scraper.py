"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com
"""

"""
The scraper module holds functions that actually scrape the e-commerce websites
"""

import requests
from src.modules.formatter import formatSearchQuery, formatResult, getCurrency, sortList
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import os
from datetime import datetime


def httpsGet(URL):
    """
    The httpsGet function makes HTTP called to the requested URL with custom headers
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }
    page = requests.get(URL, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    return BeautifulSoup(soup1.prettify(), "html.parser")


def searchAmazon(query, df_flag, currency):
    """
    The searchAmazon function scrapes amazon.com
    Parameters: query- search query for the product, df_flag- flag variable, currency- currency type entered by the user
    Returns a list of items available on Amazon.com that match the product entered by the user.
    """
    query = formatSearchQuery(query)
    URL = f"https://www.amazon.com/s?k={query}"
    page = httpsGet(URL)
    results = page.findAll("div", {"data-component-type": "s-search-result"})
    products = []
    for res in results:
        titles, prices, links = (
            res.select("h2 a span"),
            res.select("span.a-price span"),
            res.select("h2 a.a-link-normal"),
        )
        ratings = res.select("span.a-icon-alt")
        num_ratings = res.select("span.a-size-base")
        trending = res.select("span.a-badge-text")
        if len(trending) > 0:
            trending = trending[0]
        else:
            trending = None
        product = formatResult(
            "amazon",
            titles,
            prices,
            links,
            ratings,
            num_ratings,
            trending,
            df_flag,
            currency,
        )
        products.append(product)
    return products


def searchWalmart(query, df_flag, currency):
    """
    The searchWalmart function scrapes walmart.com
    Parameters: query- search query for the product, df_flag- flag variable, currency- currency type entered by the user
    Returns a list of items available on walmart.com that match the product entered by the user
    """
    query = formatSearchQuery(query)
    URL = f"https://www.walmart.com/search?q={query}"
    page = httpsGet(URL)
    results = page.findAll("div", {"data-item-id": True})
    # print(results)
    products = []
    pattern = re.compile(r"out of 5 Stars")
    for res in results:
        titles, prices, links = (
            res.select("span.lh-title"),
            res.select("div.lh-copy"),
            res.select("a"),
        )
        ratings = res.findAll("span", {"class": "w_DE"}, text=pattern)
        num_ratings = res.findAll("span", {"class": "sans-serif gray f7"})
        trending = res.select("span.w_Cs")
        if len(trending) > 0:
            trending = trending[0]
        else:
            trending = None
        product = formatResult(
            "walmart",
            titles,
            prices,
            links,
            ratings,
            num_ratings,
            trending,
            df_flag,
            currency,
        )
        products.append(product)
    return products


def searchEtsy(query, df_flag, currency):
    """
    The searchEtsy function scrapes Etsy.com
    Parameters: query- search query for the product, df_flag- flag variable, currency- currency type entered by the user
    Returns a list of items available on Etsy.com that match the product entered by the user
    """
    query = formatSearchQuery(query)
    url = f"https://www.etsy.com/search?q={query}"
    products = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    for item in soup.select(".wt-grid__item-xs-6"):
        str = item.select("a")
        if str == []:
            continue
        else:
            links = str
        titles, prices = (item.select("h3")), (item.select(".currency-value"))
        ratings = item.select("span.screen-reader-only")
        num_ratings = item.select("span.wt-text-body-01")
        trending = item.select("span.wt-badge")
        if len(trending) > 0:
            trending = trending[0]
        else:
            trending = None
        product = formatResult(
            "Etsy",
            titles,
            prices,
            links,
            ratings,
            num_ratings,
            trending,
            df_flag,
            currency,
        )
        products.append(product)
    return products


def searchGoogleShopping(query, df_flag, currency):
    """
    The searchGoogleShopping function scrapes https://shopping.google.com/
    Parameters: query- search query for the product, df_flag- flag variable, currency- currency type entered by the user
    Returns a list of items available on walmart.com that match the product entered by the user
    """
    query = formatSearchQuery(query)
    URL = f"https://www.google.com/search?tbm=shop&q={query}"
    page = httpsGet(URL)
    results = page.findAll("div", {"class": "sh-dgr__grid-result"})
    products = []
    pattern = re.compile(r"[0-9]+ product reviews")
    for res in results:
        titles, prices, links = (
            res.select("h4"),
            res.select("span.a8Pemb"),
            res.select("a"),
        )
        ratings = res.findAll("span", {"class": "Rsc7Yb"})
        try:
            num_ratings = pattern.findall(str(res.findAll("span")[1]))[0].replace(
                "product reviews", ""
            )
        except:
            num_ratings = 0
        trending = res.select("span.Ib8pOd")
        if len(trending) > 0:
            trending = trending[0]
        else:
            trending = None
        product = formatResult(
            "google",
            titles,
            prices,
            links,
            ratings,
            int(num_ratings),
            trending,
            df_flag,
            currency,
        )
        products.append(product)
    return products


def searchBJs(query, df_flag, currency):
    """
    The searchBJs function scrapes https://www.bjs.com/
    Parameters: query- search query for the product, df_flag- flag variable, currency- currency type entered by the user
    Returns a list of items available on walmart.com that match the product entered by the user
    """
    query = formatSearchQuery(query)
    URL = f"https://www.bjs.com/search/{query}"
    page = httpsGet(URL)
    results = page.findAll("div", {"class": "product"})
    # print(results)
    products = []
    for res in results:
        titles, prices, links = (
            res.select("h2"),
            res.select("span.price"),
            res.select("a"),
        )
        ratings = res.findAll("span", {"class": "on"})
        num_ratings = 0
        trending = res.select("p.instantSavings")
        if len(trending) > 0:
            trending = trending[0]
        else:
            trending = None
        product = formatResult(
            "bjs", titles, prices, links, "", num_ratings, trending, df_flag, currency
        )
        if len(ratings) != 0:
            product["rating"] = len(ratings)
        products.append(product)
    return products


def condense_helper(result_condensed, list, num):
    """This is a helper function to limit number of entries in the result"""
    for p in list:
        if num != None and len(result_condensed) >= int(num):
            break
        else:
            if p["title"] != None and p["title"] != "":
                result_condensed.append(p)


def driver(
    product, currency, num=None, df_flag=0, csv=False, cd=None, ui=False, sort=None
):
    """Returns csv is the user enters the --csv arg,
    else will display the result table in the terminal based on the args entered by the user"""

    products_1 = searchAmazon(product, df_flag, currency)
    products_2 = searchWalmart(product, df_flag, currency)
    products_3 = searchEtsy(product, df_flag, currency)
    products_4 = searchGoogleShopping(product, df_flag, currency)
    products_5 = searchBJs(product, df_flag, currency)
    result_condensed = ""
    if not ui:
        results = products_1 + products_2 + products_3 + products_4 + products_5
        result_condensed = (
            products_1[:num]
            + products_2[:num]
            + products_3[:num]
            + products_4[:num]
            + products_5[:num]
        )
        result_condensed = pd.DataFrame.from_dict(result_condensed, orient="columns")
        results = pd.DataFrame.from_dict(results, orient="columns")
        if currency == "" or currency == None:
            results = results.drop(columns="converted price")
            result_condensed = result_condensed.drop(columns="converted price")
        if csv == True:
            file_name = os.path.join(
                cd, (product + datetime.now().strftime("%y%m%d_%H%M") + ".csv")
            )
            print("CSV Saved at: ", cd)
            print("File Name:", file_name)
            results.to_csv(file_name, index=False, header=results.columns)
    else:
        result_condensed = []
        condense_helper(result_condensed, products_1, num)
        condense_helper(result_condensed, products_2, num)
        condense_helper(result_condensed, products_3, num)
        condense_helper(result_condensed, products_4, num)
        condense_helper(result_condensed, products_5, num)

        if currency != None:
            for p in result_condensed:
                p["price"] = getCurrency(currency, p["price"])

        # Fix URLs so that they contain http before www
        # TODO Fix issue with Etsy links -> For some reason they have www.Etsy.com prepended to the begining of the link
        for p in result_condensed:
            link = p["link"]
            if p["website"] == "Etsy":
                link = link[12:]
                p["link"] = link
            elif "http" not in link:
                link = "http://" + link
                p["link"] = link

        if sort != None:
            result_condensed = pd.DataFrame(result_condensed)
            if sort == "rades":
                result_condensed = sortList(result_condensed, "ra", False)
            elif sort == "raasc":
                result_condensed = sortList(result_condensed, "ra", True)
            elif sort == "pasc":
                result_condensed = sortList(result_condensed, "pr", False)
            else:
                result_condensed = sortList(result_condensed, "pr", True)
            result_condensed = result_condensed.to_dict(orient="records")

        if csv:
            file_name = product + "_" + datetime.now() + ".csv"
            result_condensed = result_condensed.to_csv(
                file_name, index=False, header=results.columns
            )
            print(result_condensed)
    return result_condensed
