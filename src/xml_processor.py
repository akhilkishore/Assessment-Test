#!/home/akhil/anaconda3/bin/python
"""
    Parse and process XML (file_type : DLTINS) into a iterative object.
"""

import json
import pandas as pd
import xml.etree.ElementTree as ET
import params as parameters
import custom_errors as CustomErrors
import logging
import functions

class XmlProcessor:
    """
        Class Reference 
        ---------------

        Object of this module is iterable  such as in a for-loop
        Each Iteration will provide a python dictionary.
        Where key in the dictionary is the element tag name ( eg : Id, Issr etc)
        And value is the data related to it.
    """
    def __init__(self, xml_path, root_tag, parent_and_child_tags):
        """
            Initialize instances of the class from user parameters

            Parameters
            ----------
                xml_path :             
                    Absolute path of the xml file.

                root_tag :              
                    root_tag is defined as the tag name of the element
                    which has all data we consider as its child nodes.

                parent_and_child_tags : 
                    A list of dictionary where each key of the
                    dictionary represent a xml tag name and value is a list 
                    its child xml tag names.

        """
    
        self.xml_path = xml_path
        self.root_tag = root_tag
        self.parent_and_child_tags = parent_and_child_tags
        self.original_xml_tag_names_dict = {}
        self.parsed_data_with_required_contents = self.collect_required_xml_tags_only()

    def read_xml_file(self):
        """
            Read the xml path and parse using ElementTree API

            Parameters 
            ----------
            No parameters taken !

            Returns
            -------
            ElementTree Object: 
                It represents the whole XML document as a tree

            Raises
            ------
                UnableToReadXmlFile : if its unable to read xml from given path

        """
        try:
            return ET.parse(self.xml_path)
        except:
            raise CustomErrors.UnableToReadXmlFile

        


    def get_orginal_xml_tag_for_given_tag(self, parsed_xml_data, tag):
        """
            For a given user defined tag name retuns its original tag name 
            associated with xml file if available else returns None

            Parameters
            ----------
            parsed_xml_data (ElementTree Object) : 
                Parsed Xml file 
            tag (String) : 
                A user defined xml tag name ( eg : Id or Issr )

            Returns 
            -------
            Strting :
                Original tag name from xml file for give user defined tag name
        """

        for elem in parsed_xml_data.iter(): 
            if elem.tag.split('}')[1] == tag :
                return elem.tag
        return None

    def original_tag_name_collector(self, parsed_xml_object ):
        """
            Iterate through given ElementTree Object and map user 
            defined tag names with its original tag names from the
            xml file. 

            Parameters
            ----------
            parsed_xml_object (ElementTree Object) :
                Parsed Xml file 

            Returns
            -------
            Dictionary :
                Where key is user definde tag name
                And value is original tag name associated with xml            
        """

        temp_dict = {}

        for tag in self.parent_and_child_tags:
            for key in tag:
                temp_dict[key] = self.get_orginal_xml_tag_for_given_tag(parsed_xml_object, key)
                for sub_tag in tag[key]:
                    temp_dict[sub_tag] = self.get_orginal_xml_tag_for_given_tag(parsed_xml_object, sub_tag)
        return temp_dict

            
            


    def collect_required_xml_tags_only(self):
        """
            Read and parse the xml file using ElementTree Module

            Iterate throught the ElementTree Object using self.toot_tag,
            And if nodes under the root_tag contains reqired parent_tag and child_tags
            then keep it for further process Else drop the inspected subset.

            Parameters
            ----------
            No parameters taken !

            Returns
            -------    
            A list of ElementTree Objects :
                A list of validated subset of ElementTree Object 
                which contains required data within it. 

        """

        parsed_xml_object = self.read_xml_file()

        self.original_xml_tag_names_dict = self.original_tag_name_collector(parsed_xml_object)

        collected_tags = []

        original_root_tag_name = self.get_orginal_xml_tag_for_given_tag(parsed_xml_object, self.root_tag) 

        for item in parsed_xml_object.iter(original_root_tag_name):
            available_tags = [child.tag for child in item]
            flag =True 
            for parent_tag in self.parent_and_child_tags:
                for key in parent_tag:
                    if self.original_xml_tag_names_dict[key] not in available_tags: 
                        # one of the required tag is not present in the selected ElementTree subset.
                        flag =False
                        break
            if flag == True:
                collected_tags.append(item)
            else :
                flag = True

        del parsed_xml_object # delete the variable because it can be huge in size.
        functions.add_info_log(str(len(collected_tags))+" subsets found for data extraction..")
        return collected_tags

    def __getitem__(self, idx):
        """
            Used to support the indexing such that object_of_the_class[i] can be used to get ith sample
            
            For collected list of valid XML elements each child node's ( required ) data is collected.

            Parameters
            ----------
            idx (int):
                A interger number with in the range of target list size

            Returns
            -------
            Dictionary:
                Where key is the user defined tag
                And value is the data associated to that tag which is taken from XML
        """

        temp_dict = {}

        for child in self.parsed_data_with_required_contents[idx]:

            if child.tag.split('}')[-1] in self.original_xml_tag_names_dict.keys():
                if len(child) == 0:
                    temp_dict[child.tag.split('}')[-1]] = child.text
                for sub_child in child:
                    if sub_child.tag.split('}')[-1] in self.original_xml_tag_names_dict.keys():
                        temp_dict[sub_child.tag.split('}')[-1]] = sub_child.text

        return temp_dict


    def __len__(self):
        """
            Parameters
            ----------
            No parameters taken !

            Returns
            -------
                Integer:
                    The length of available data( Number of rows ) that extracted from the XML file. 
        """
        return len(self.parsed_data_with_required_contents)






    
        




