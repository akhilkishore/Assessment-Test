#!/home/akhil/anaconda3/bin/python
from xml_processor import XmlProcessor
import params as parameters
import functions as functions
import glob
import custom_errors as CustomErrors
import logging
import logging.config
import sys
import aws_functions


logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)

#Init following list parameters to hold data later

all_values_for_header_id = []
all_values_for_header_fullnm = []
all_values_for_header_clssfctntp = []
all_values_for_header_cmmdtyderivind = []
all_values_for_header_ntnlccy = []
all_values_for_header_issr = []

    
if __name__ == "__main__": 

    functions.add_info_log("Starting...")
    #download xml from link 
    functions.add_info_log("XML link for downloading : "+parameters.XML_URL)
    functions.add_info_log("Downloading xml file...")
    functions.get_zip_download_link(parameters.XML_URL)

    #find the xml path
    xml_path = glob.glob(parameters.DESTINATION_PATH+"*.xml")[0]
    functions.add_info_log("XML file found")
    functions.add_info_log("XML path is : "+ xml_path)

    # Create object for XmlProcessor

    processed_xml_object = XmlProcessor(xml_path, 
                            parameters.REQUIRED_ROOT_TAG, 
                            parameters.REQUIRED_PARENT_AND_CHILD_TAGS)

    # Print the length of available data after parsing and processing the XML file

    functions.add_info_log("Available number of rows : "+str(len(processed_xml_object)))


    # Iterate through the object and parse the data then append into corresponding list
    for count,data in enumerate(processed_xml_object):
        all_values_for_header_id.append(data['Id'])
        all_values_for_header_fullnm.append(data['FullNm'])
        all_values_for_header_clssfctntp.append(data['ClssfctnTp'])
        all_values_for_header_cmmdtyderivind.append(data['CmmdtyDerivInd'])
        all_values_for_header_ntnlccy.append(data['NtnlCcy'])
        all_values_for_header_issr.append(data['Issr'])



    # Pass the lists to create a DataFrame out of it 
    df = functions.create_csv_from_list_values(all_values_for_header_id, 
                all_values_for_header_fullnm, all_values_for_header_clssfctntp, 
                all_values_for_header_cmmdtyderivind, all_values_for_header_ntnlccy, 
                all_values_for_header_issr)


    #save DataFrame as CSV into local disk
    functions.add_info_log("Trying to save csv into local machine..")
    functions.save_dataframe_as_csv(df,parameters.DESTINATION_PATH+"result_as_csv.csv")

    #save DataFrame from local machine to AWS S3 
    aws_functions.upload_to_aws(parameters.DESTINATION_PATH+"result_as_csv.csv", 'result_as_csv.csv', upload_now=False)

    functions.add_info_log("END !")

