"""
    This module contails utility funcitions to supprot XML processing
"""
import pandas as pd 
import custom_errors as CustomErrors
from bs4 import BeautifulSoup
import requests
import zipfile
import params as parameters
import dload
import urllib
import logging



def add_info_log(message):
    """
    Used to add log (info) into the log file
    
    Parameters
    ----------
        message (string):
            Content to add in the log

    Returns
    -------
        Returns nothing

    """
    logging.info(message)






def create_csv_from_list_values(all_values_for_header_id, all_values_for_header_fullnm,
                            all_values_for_header_clssfctntp, all_values_for_header_cmmdtyderivind,
                            all_values_for_header_ntnlccy, all_values_for_header_issr):
    
    """

        Take lists and insert them into a DataFrame
        using proper header/column names

        Parameters
        ----------
            all_values_for_header_id (List) :
                which contains Id as elements
            all_values_for_header_fullnm (List) : 
                which contains FullNm as elements
            all_values_for_header_clssfctntp (List) :
                which contains ClssfctnTp as elements
            all_values_for_header_cmmdtyderivind (List) :
                which contains CmmdtyDerivInd as elements
            all_values_for_header_ntnlccy (List) :
                which contains NtnlCcy as elements
            all_values_for_header_issr (List) :
                which contains Issr as elements
        
        Returns
        -------
            Pandas DataFrame:
                Which has 6 columns (required as per the problem statements)
        
        Raises
        ------
            ListLengthNotMatching : input lists for dataframe has different length
    """

    if (len(all_values_for_header_id) == len(all_values_for_header_fullnm)
                            == len(all_values_for_header_clssfctntp) == len(all_values_for_header_cmmdtyderivind)
                            == len(all_values_for_header_ntnlccy) == len(all_values_for_header_issr)):
                            add_info_log("All list data for dataframe creation is validated")
    else:
        raise CustomErrors.ListLengthNotMatching

    df = pd.DataFrame()
    df['FinInstrmGnlAttrbts.Id'] = all_values_for_header_id
    df['FinInstrmGnlAttrbts.FullNm'] = all_values_for_header_fullnm
    df['FinInstrmGnlAttrbts.ClssfctnTp'] = all_values_for_header_clssfctntp
    df['FinInstrmGnlAttrbts.CmmdtyDerivInd'] = all_values_for_header_cmmdtyderivind
    df['FinInstrmGnlAttrbts.NtnlCcy'] = all_values_for_header_ntnlccy
    df['Issr'] = all_values_for_header_issr

    return df

    

def save_dataframe_as_csv(df, csv_name):
    """
        Take the dataframe and save using give csv_name
    
        Parameters
        ----------
            df (padas dataframe) :
                Where XML data is processed and stored
            
            csv_name (string) :
                Name used to save the csv

        Returns
        -------
            Return nothing.   

        Raises
        ------
            UnableToWriteCsvInToDisk : if unable to save csv into local disk

    """    
    try:
 
        df.to_csv(csv_name,index=False)
        add_info_log("CSV saved in path : "+csv_name)
    except:
        add_info_log("Unable to write csv into local machine")
        raise CustomErrors.UnableToWriteCsvInToDisk



def get_zip_download_link(url):
    """
        Download the XML using input url 
        parse the xml using BeautifulSoup and get first DLTINS zip download link
        call download_and_save_zip_file() to download the zip using extracted url 

        Parameters
        ----------
            url (string):
                The url to download XML file
        Returns
        -------
            Return nothing.

        Raises
        ------
            UnableToGetDLTINSDownloadLink : If unable to download or parse the XML for first link

    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.findAll("str", {"name" : "download_link"})
    add_info_log("Trying to find the first link for downloading...")

    try:
        url_to_download = results[0].text
        add_info_log("First link found for downloading...")
        add_info_log("First link is : "+url)

    except:
        add_info_log("unable to find the first link...")
        raise CustomErrors.UnableToGetDLTINSDownloadLink

    download_and_save_zip_file(url_to_download)

def download_and_save_zip_file(url):
    """
        Download the zip file and extract it's contents into local disk

        Parameters 
        ----------
            url (string):
                The link for ZIP file to download

        Returns
        -------
            Return nothing.

        Raises 
        ------
            UnableToDownloadDLTINSZip : If its unable to download ,extract or save the zip.

    """
    add_info_log("zip url is :"+url)

    add_info_log("Zip file downloading ....")
    try:
        zip_path, _ = urllib.request.urlretrieve(url)
        add_info_log("Zip file download completed.")
        with zipfile.ZipFile(zip_path, "r") as f:
            f.extractall(parameters.DESTINATION_PATH)
        add_info_log("Zip file extraction completed")

    except:
        add_info_log("Failed to download and extract the zip file")
        raise CustomErrors.UnableToDownloadDLTINSZip



