""" ClinicalOmicsDB: Bridging the gap between next-generation clinical omics data and machine learning
Reference: Chang In Moon, Byron Jia, Bing Zhang
Paper link: TBD
Code author: Chang In Moon (moonchangin@gmail.com)
-----------------------------
database_download.py
- Basic functions that will use box api to obtain dataset

(0) download_sheet: provide a table with list of dataset link
(1) get_dataset_link: provide available data in a data frame
(2) get_ssl_dataset_link: provide available data with multiple treatment arms
(3) HR_dataset_link: provide available data with BRCA-HR subtype
(4) HER2_dataset_link: provide available data with BRCA-HER2 subtype
(5) TNBC_dataset_link: provide available data with BRCA-TNBC subtype
(6) ssl_HR_dataset_link: provide available data with multiple treatment arms [BRCA-HR subtype]
(7) ssl_HER2_dataset_link: provide available data with multiple treatment arms [BRCA-HER2 subtype]
(8) ssl_TNBC_dataset_link: provide available data with multiple treatment arms [BRCA-TNBC subtype]
(9) download: returns dataset for analysis
(10) get_patient_dataset_link: provide available clinical in a data frame [under development]
(11) download_patient_data: returns dataset for subsetting data frame [under development]

"""
import io
import pandas as pd
from file_download import download_text as _download_text
from exceptions import BaseError, BaseWarning, InvalidParameterError, NoInternetError, OldPackageVersionWarning

def download_sheet():
    dataset_link_url = "https://bcm.box.com/shared/static/0t7n2lcx8pewasxjuicez78k9tyj0kc5.csv"
    try:
        dataset_link_text = _download_text(dataset_link_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_link_text), header=0)


def get_dataset_link():
    dataset_link_url = "https://bcm.box.com/shared/static/1rs6wid9em7tewjpqchnar4wlr75l3ml.csv"
    try:
        dataset_link_text = _download_text(dataset_link_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_link_text), header=0)

def get_ssl_dataset_link():
    dataset_link_url = "https://bcm.box.com/shared/static/6h0jdwq1lsfm13qmrfbv8yac8hje8zzb.csv"
    try:
        dataset_link_text = _download_text(dataset_link_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_link_text), header=0)

def HR_dataset_link():
    dataset_link_url = "https://bcm.box.com/shared/static/57eq2myuuxpxjimm8tus5sjlhxijdgi1.csv"
    try:
        dataset_link_text = _download_text(dataset_link_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_link_text), header=0)

def HER2_dataset_link():
    dataset_link_url = "https://bcm.box.com/shared/static/ifaxp6bxka909lggeb8fmyv4ze70ek6k.csv"
    try:
        dataset_link_text = _download_text(dataset_link_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_link_text), header=0)

def TNBC_dataset_link():
    dataset_link_url = "https://bcm.box.com/shared/static/9hd1vmvcztsbxdzcw2ino2t4tmltw2hv.csv"
    try:
        dataset_link_text = _download_text(dataset_link_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_link_text), header=0)

def ssl_HR_dataset_link():
    dataset_link_url = "https://bcm.box.com/shared/static/di0xm2y2w2n7f8hp7he4xgdugnadnf32.csv"
    try:
        dataset_link_text = _download_text(dataset_link_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_link_text), header=0)

def ssl_HER2_dataset_link():
    dataset_link_url = "https://bcm.box.com/shared/static/hb2hgxogx2h0wq6ud0mbigjvrli5j4lx.csv"
    try:
        dataset_link_text = _download_text(dataset_link_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_link_text), header=0)

def ssl_TNBC_dataset_link():
    dataset_link_url = "https://bcm.box.com/shared/static/8lfgpx9mkrc13fa0e9gfpsfjsoe29n2a.csv"
    try:
        dataset_link_text = _download_text(dataset_link_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_link_text), header=0)

def download(url):
    try:
        dataset_text = _download_text(url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_text), header=0)

def get_patient_dataset_link():
    dataset_link_url = "https://bcm.box.com/shared/static/yt0ldc2nptxn96ovnna3hjxtlntzfvig.csv"
    try:
        dataset_link_text = _download_text(dataset_link_url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_link_text), header=0)


def download_patient_data(input):
    input = input.upper()
    data_link = get_patient_dataset_link()
    target = data_link.loc[data_link['Series'] == input]
    url = target.iloc[0,1]
    try:
        dataset_text = _download_text(url)
    except NoInternetError:
        raise NoInternetError("Insufficient internet to download available dataset info. Check your internet connection.") from None
    return pd.read_csv(io.StringIO(dataset_text), header=0)