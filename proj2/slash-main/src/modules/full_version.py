from genericpath import exists
import json
import os
import pandas as pd
from src.modules.scraper import driver
import webbrowser
import numpy as np
from pathlib import Path
from shutil import get_terminal_size


class full_version:
    def __init__(self):
        self.data = {}
        self.name = ""
        self.email = ""
        self.user_data_dir = Path(__file__).parent.parent / "json"
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.user_data = self.user_data_dir / "user_data.json"
        self.user_list_dir = Path(__file__).parent.parent / "csvs"
        self.user_list_dir.mkdir(parents=True, exist_ok=True)
        self.user_list = self.user_list_dir / "default.csv"
        self.df = pd.DataFrame()
        self.currency = ""
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", get_terminal_size()[0])
        pd.set_option("display.max_colwidth", 40)

    def login(self):
        """Used for User Login
        Returns the username and email"""
        if not os.path.exists(self.user_data):
            print("Welcome to Slash!")
            print("Please enter the following information: ")
            name = input("Name: ")
            email = input("Email: ")
            self.data["name"] = name
            self.data["email"] = email
            with open(self.user_data, "w") as outfile:
                json.dump(self.data, outfile)
            self.name = name
            self.email = email
            open(self.user_list, "a").close()

        else:
            with open(self.user_data) as json_file:
                data = json.load(json_file)
                self.name = data["name"]
                self.email = data["email"]
        return self.name, self.email

    def search_fn(self):
        """Function searches for a given product and returns full list of products scraped.
        It then gives the user and option to save an item or open an item in browser"""
        prod = input("Enter name of product to Search: ")
        self.scrape(prod)
        ch = input(
            "\nEnter 1 to save product to wishlist \nEnter 2 to open link in browser\nElse enter any other key to continue\n"
        )
        try:
            ch = int(ch)
        except Exception:
            pass
        """By selecting 1, the User can store a searched product into a wishlist. Multiple wishlist are available and it has to be pre-selected 
        to store an item into it."""
        if ch == 1:
            wish_lists = self.wishlist_maker()
            wishlist_index = int(input("\nEnter your wishlist index: "))
            selected_wishlist = wish_lists[wishlist_index]
            wishlist_path = self.user_list_dir / selected_wishlist
            """Select the row number of the product to save into the selected wishlist."""
            indx = int(input("\nEnter row number of product to save: "))
            if indx < len(self.df):
                new_data = self.df.iloc[[indx]]
                if os.path.exists(wishlist_path) and (
                    os.path.getsize(wishlist_path) > 0
                ):
                    old_data = pd.read_csv(wishlist_path)
                else:
                    old_data = pd.DataFrame()
                if self.df.title[indx] not in old_data:
                    final_data = pd.concat([old_data, new_data])
                    print("Item added successfully")
                final_data.to_csv(wishlist_path, index=False, header=self.df.columns)
        """Selecting 2 allows the user to open the searched item in a broswer"""
        if ch == 2:
            indx = int(input("\nEnter row number of product to open: "))
            webbrowser.open_new(self.df.link[indx])

        return

    def extract_list(self):
        """This function helps user extract saved products, create new lists, modify list or open product in browser"""
        wish_lists = self.wishlist_maker()
        wishlist_options = int(
            input(
                "\nSelect from the following: \n1. Open Wishlist \n2. Create new Wishlist \n3. Delete Wishlist \n4. Return to Main\n"
            )
        )

        if wishlist_options == 1:
            wishlist_index = int(input("\nEnter the wishlist index: "))
            selected_wishlist = wish_lists[wishlist_index]
            wishlist_path = self.user_list_dir / selected_wishlist
            if os.path.exists(wishlist_path):
                try:
                    old_data = pd.read_csv(wishlist_path)
                    print(old_data)
                except Exception:
                    old_data = pd.DataFrame()
                    print("Empty Wishlist")
                choice = int(
                    input(
                        "\nSelect from the following:\n1. Delete item from list\n2. Open link in Chrome\n3. Return to Main\n"
                    )
                )
                if choice == 1:
                    indx = int(input("\nEnter row number to be removed: "))
                    old_data = old_data.drop(index=indx)
                    old_data.to_csv(wishlist_path, index=False, header=old_data.columns)
                if choice == 2:
                    indx = int(input("\nEnter row number to open in chrome: "))
                    url = old_data.link[indx]
                    webbrowser.open_new(url)

        elif wishlist_options == 2:
            wishlist_name = str(input("\nName your wishlist: "))
            new_wishlist = self.user_list_dir / (wishlist_name + ".csv")
            open(new_wishlist, "a").close()

        elif wishlist_options == 3:
            wishlist_index = int(input("Enter the wishlist index to delete: "))
            selected_wishlist = wish_lists[wishlist_index]
            wishlist_path = self.user_list_dir / selected_wishlist
            wishlist_path.unlink()
        else:
            print("No saved data found.")

    def wishlist_maker(self):
        wish_lists = []
        print("----------Wishlists---------")
        for index, wishlist in enumerate(os.listdir(self.user_list_dir)):
            wish_lists.append(wishlist)
            wishlist = wishlist.replace(".csv", "")
            print(index, "\t", wishlist)
        return wish_lists

    def scrape(self, prod):
        """calls the scraper function from scraper.py"""
        results = driver(prod, df_flag=1, currency=self.currency)
        # esults = formatter.sortList(results, "ra" , True)
        self.df = pd.DataFrame.from_dict(results, orient="columns")
        print(self.df.replace("", np.nan).dropna())

    def driver(self):
        self.login()
        flag_loop = 1
        print("Welcome ", self.name)
        while flag_loop == 1:
            print("Select from following:")
            print(
                "1. Search new product\n2. Manage Wishlists\n3. See Currency Conversion\n4. Exit"
            )
            choice = int(input())
            if choice == 1:
                self.search_fn()
            elif choice == 2:
                self.extract_list()
            elif choice == 3:
                self.currency = str.lower(input("Enter INR/EUR\n"))
            elif choice == 4:
                print("Thank You for Using Slash")
                flag_loop = 0
            else:
                print("Incorrect Option")
