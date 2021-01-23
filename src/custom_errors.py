class ListLengthNotMatching(Exception):
    """Exception raised when input lists for dataframe has different length .
    """
    def __init__(self):
        self.message = "All list do not have same length"
        super().__init__(self.message)


class UnableToWriteCsvInToDisk(Exception):
    """Exception raised when it is unable to write the csv into disk.
    """
    def __init__(self):
        self.message = "Unable to write file into local disk"
        super().__init__(self.message)

class UnableToWriteCsvInToAWSS3(Exception):
    """Exception raised when it is unable to write the csv into AWS S3.
    """
    def __init__(self):
        self.message = "Unable to write file into AWS S3"
        super().__init__(self.message)

class UnableToReadXmlFile(Exception):
    """Exception raised when XML is unable to read.
    """
    def __init__(self):
        self.message = "Unable to read XML file, check path"
        super().__init__(self.message)

class UnableToGetDLTINSDownloadLink(Exception):
    """Exception raised when unable to parse xml and get DLTINS file download link
    """
    def __init__(self):
        self.message = "Unable to get DLTINS download link,check internet connection"
        super().__init__(self.message)

class UnableToDownloadDLTINSZip(Exception):
    """Exception raised when unable download and unzip the file
    """
    def __init__(self):
        self.message = "Unable to download and unzip the zip file"
        super().__init__(self.message)


class UnableToConnectToS3(Exception):
    """Exception raised when unable to connect to AWS S3
    """
    def __init__(self):
        self.message = "Unable to connect to AWS S3"
        super().__init__(self.message)
