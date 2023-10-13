from src.modules import full_version
from src.modules import csv_writer
import random
import string
import os
import json
import pytest

def test_set_player_name(monkeypatch):
    fv = full_version.full_version()
    if not os.path.exists(fv.user_data):
        name = "".join(random.choices(string.ascii_lowercase, k=5))
        email = "".join(random.choices(string.ascii_lowercase, k=3)) + "@mail.com"
        
        answers = iter([name, email])

        monkeypatch.setattr('builtins.input', lambda name: next(answers))

        assert fv.login() == (name, email)
    else:
        with open(fv.user_data) as json_file:
            data = json.load(json_file)
            name = data["name"]
            email = data["email"]
        assert fv.login() == (name, email)

def test_extract_list(monkeypatch, capfd):
    fv = full_version.full_version()
    wishlist_index = 0
    # Create a new wishlist
    answers = iter([2, wishlist_index, 3])
    monkeypatch.setattr('builtins.input', lambda name: next(answers))
    fv.extract_list()
    out, err = capfd.readouterr()
    assert "Wishlists" in out

    # Adds an item to wish list
    answers = iter(["socks", 1, wishlist_index, 5])
    monkeypatch.setattr('builtins.input', lambda name: next(answers))
    fv.search_fn()
    out, err = capfd.readouterr()
    assert "Item added successfully" in out

    answers = iter([1, wishlist_index, 3])
    monkeypatch.setattr('builtins.input', lambda name: next(answers))
    fv.extract_list()
    out, err = capfd.readouterr()
    assert "Wishlists" in out

    # First "3" indicates deleting the index
    # Second "3" indicates closing the menu
    # Deletes the 0th index
    answers = iter([3, wishlist_index, 3])
    monkeypatch.setattr('builtins.input', lambda name: next(answers))
    fv.extract_list()

    with pytest.raises(IndexError):
        answers = iter([1, 33, 3])
        monkeypatch.setattr('builtins.input', lambda name: next(answers))
        fv.extract_list()

def test_csv_writer():
    x = csv_writer.write_csv([{"name": "parth", "surname": "parikh", "age": 10}], "Names", ".")
    assert x[:5] == "Names"