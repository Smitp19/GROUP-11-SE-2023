"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com

"""

from src.modules.formatter import formatSearchQuery, formatTitle

def test_formatSearchQuery():
    """
    Checks the formatSearchQuery function
    """
    assert formatSearchQuery("1 2") == "1+2"
    assert formatSearchQuery("A B") == "A+B"
    assert formatSearchQuery("ABC") == "ABC"

def test_formatTitle():
    """
    Checks the formatTitle function
    """
    assert formatTitle("0"*50) == "0"*40+"..."
    assert formatTitle("0"*5) == "0"*5