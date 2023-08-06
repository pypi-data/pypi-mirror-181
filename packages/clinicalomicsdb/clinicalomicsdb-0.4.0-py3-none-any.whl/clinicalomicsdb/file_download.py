""" ClinicalOmicsDB: Bridging the gap between next-generation clinical omics data and machine learning
Reference: Chang In Moon, Byron Jia, Bing Zhang
Paper link: TBD
Code author: Chang In Moon (moonchangin@gmail.com)
-----------------------------

file_download.py
- API/SDK that will download data from box
"""
import threading
from queue import Queue

from werkzeug import Request
from werkzeug import Response
from werkzeug.serving import make_server

import webbrowser
import time
import logging
import os
import requests
from requests.adapters import HTTPAdapter, Retry
import getpass
import bs4

from file_tools import *
from exceptions import InvalidParameterError, NoInternetError, DownloadFailedError

# Some websites don't like requests from sources without a user agent. Let's preempt that issue.
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0)'
HEADERS = {'User-Agent': USER_AGENT}

def download_text(url):
    """Download text from a direct download url for a text file.

    Parameters:
    url (str): The direct download url for the text.

    Returns:
    str: The downloaded text.
    """
    
    try:
        s = requests.Session()
        retries = Retry(total=10,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        response = s.get(url) #s.get(url, headers=HEADERS, allow_redirects=True)
        response.raise_for_status() # Raises a requests HTTPError if the response code was unsuccessful
    except requests.RequestException: # Parent class for all exceptions in the requests module
        raise NoInternetError("Insufficient internet. Check your internet connection.") from None 

    text = response.text.strip()
    return text