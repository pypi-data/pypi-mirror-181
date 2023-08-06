""" ClinicalOmicsDB: Bridging the gap between next-generation clinical omics data and machine learning
Reference: Chang In Moon, Byron Jia, Bing Zhang
Paper link: TBD
Last updated Date: October 21st 2022
Code author: Chang In Moon (moonchangin@gmail.com)
-----------------------------
"""
__version__ = '0.4.0'

import io
import pandas as pd
from database_download import download, get_dataset_link, download_sheet
from file_download import download_text as _download_text
from exceptions import BaseError, BaseWarning, InvalidParameterError, NoInternetError, OldPackageVersionWarning

def list_datasets():
    """List all available datasets."""
    dataset_list_url = "https://bcm.box.com/shared/static/v24wiuyy73rhv8jn44tyjbs0al8wa6oe.csv"
    try:
        dataset_list_text = _download_text(dataset_list_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_list_text), header=0)
