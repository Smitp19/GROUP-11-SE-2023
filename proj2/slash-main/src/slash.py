"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com

"""

import argparse
from src.modules.scraper import driver
from src.modules.formatter import sortList
from tabulate import tabulate
import os
import csv
from src.modules.full_version import full_version
import pandas as pd
from shutil import get_terminal_size

def main():
    """Provides help for every argument"""
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", get_terminal_size()[0])
    pd.set_option("display.max_colwidth", 40)
    parser = argparse.ArgumentParser(description="Slash")
    parser.add_argument(
        "--full",
        type=str,
        help="T for full version of app; F for mini version of app",
        default="F",
    )
    parser.add_argument("--search", type=str, help="Product search query")
    parser.add_argument("--num", type=int, help="Maximum number of records", default=3)
    parser.add_argument(
        "--sort",
        type=str,
        nargs="+",
        help="Sort according to re (relevance: default), pr (price) or ra (rating)",
        default="re",
    )
    parser.add_argument("--link", action="store_true", help="Show links in the table")
    parser.add_argument(
        "--des", action="store_true", help="Sort in descending (non-increasing) order"
    )
    parser.add_argument(
        "--cd",
        type=str,
        help="Change directory to save CSV file with search results",
        default=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "csvs"
        ),
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Save results as CSV",
    )
    parser.add_argument(
        "--currency",
        type=str,
        help="Display the amount in specified currency(inr, euro, aud, yuan, yen, pound)",
    )
    args = parser.parse_args()

    if args.full == "T":

        full_version().driver()
        return

    results = driver(
        args.search,
        args.currency,
        args.num,
        csv=args.csv,
        cd=args.cd,
    )

    for sortBy in args.sort:
        results = sortList(results, sortBy, args.des)

    print()
    print()
    print(results)
    print()
    print()


if __name__ == "__main__":
    main()
