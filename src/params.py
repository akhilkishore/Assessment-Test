#!/home/akhil/anaconda3/bin/python



'''
    Destination path to save extracted CSV
'''
DESTINATION_PATH = "../data/"


XML_URL = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100"



################################# Do Not Edit Below Configurations


'''
    Tag name which contains all required data under its child elements/nodes
    Taken from the xml after simple element analysis
'''
REQUIRED_ROOT_TAG = "TermntdRcrd"

'''
    A list of dictionary
    Key in the dictionary is a tag name from XML ( which is requred as per problem statement)
    Value is a list of tag names from XML which are the child of the Key tag name ( which are requred as per problem statement)
'''

REQUIRED_PARENT_AND_CHILD_TAGS=[
    {"FinInstrmGnlAttrbts":
        ["Id","FullNm","ClssfctnTp","NtnlCcy","CmmdtyDerivInd","Issr"]
        },
    {
        "Issr":[]
    }
]


