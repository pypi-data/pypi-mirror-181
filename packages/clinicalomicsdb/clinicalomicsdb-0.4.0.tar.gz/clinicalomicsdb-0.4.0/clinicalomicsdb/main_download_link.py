""" ClinicalOmicsDB: Bridging the gap between next-generation clinical omics data and machine learning
Reference: Chang In Moon, Byron Jia, Bing Zhang
Paper link: TBD
Code author: Chang In Moon (moonchangin@gmail.com)
-----------------------------
download_link.py
- interactive python script that ask several query which give a table with downloadble link and an option to download all of them

"""


import re
import io
import sys
import inquirer
from database_download import download_sheet
import pandas as pd
from datetime import datetime
from file_download import download_text as _download_text

# Disease inquiry
questions_1 = [
  inquirer.Checkbox('disease',
                    message="What type of disease type you would like to download? (Left and right arrow to select multiple)",
                    choices=['Breast', 'Colorectal', 'Lukemia', 'Lung', 'Melanoma', 'Myeloma', 'Ovarian'],
                    default='Breast'
                    ),
]
disease_type = inquirer.prompt(questions_1)
# if breast cancer is selected promt breast cancer subtype (11/14/22 continue...)
if "Breast" in  disease_type["disease"][:]:
    questions_1_1 = [
    inquirer.Checkbox('breast_subtype',
                    message="What breast cancer subtype you would like to download? (Left and right arrow to select multiple)",
                    choices=['Combined', 'HR+', 'HER2+', 'TNBC'],
                    default='Combined'
                    ),]
    breast_subtype = inquirer.prompt(questions_1_1)

# Treatment inquiry
questions_2 = [
  inquirer.Checkbox('treatment',
                    message="What treatment type you would like to download? (Left and right arrow to select multiple)",
                    choices=['Cytotoxic', 'Targeted', 'Immunotherapy'],
                    default='Cytotoxic'
                    ),
]
treatment_type = inquirer.prompt(questions_2)

# Download inquiry
questions_3 = [
  inquirer.List('download',
                    message="Would you like to download the selected data to your current directory?",
                    choices=['Yes (it may take a few minutes depending on network condition)', 'No (use the link in the excel to manually download)'],
                    default='No (use the download link in the CSV excel to manually download)'
                    ),
]
download = inquirer.prompt(questions_3)

# Based on inquiry filter out the data
main_db = download_sheet() 
# merge dictionary as one
if 'breast_subtype' in globals():
  filter = {**disease_type,**breast_subtype,**treatment_type}
else:
  filter = {**disease_type,**treatment_type}
print("Query added by user: " + str(filter))
# filter database
##Start with array of all True
ind = [True] * len(main_db)
##Loop through filters, updating index
for col, vals in filter.items():
    ind = ind & (main_db[col].isin(vals))
##Return filtered dataframe
output = main_db[ind]
if output.empty:
  sys.exit('[ERROR] No data was found from your query :( \n[ERROR] Please try again with more options checked!')
output.to_csv("clindb_download_queue_" + datetime.now().strftime("%H:%M:%S") + ".csv")

# begin the download if the user said Yes on the final question
if 'Yes (it may take a few minutes depending on network condition)' in download.values():
    print("[DOWNLOADING] This may take a few minutes depending on network condition. Thank you for you for being patient!")
    list_link = output[['File_Name','download_link']]
    list_link = list_link.reset_index()
    for file, row in list_link.iterrows():
        text = _download_text(row['download_link'])
        tmp = pd.read_csv(io.StringIO(text), header=0)
        tmp.to_csv(row['File_Name'])
        print("[LOG] " + str(row['File_Name']) + " download complete!")