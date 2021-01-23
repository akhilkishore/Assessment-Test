import unittest
import functions as fn
import custom_errors as CustomErrors
######################
import pandas as pd
######################
class TestFunctions(unittest.TestCase):

    def test_create_csv_from_list_values_dtype(self):
        """
            case 1 :
            Compare dtype of create_csv_from_list_values() result with sample_result( dtype is pandas dataframe)
            If all 6 list into method create_csv_from_list_values() has same length
            Then it should return a pandas dataframe 
        """
        result = fn.create_csv_from_list_values([1],[1],[1],[1],[1],[1])
        sample_result = pd.DataFrame()
        self.assertEqual(type(result),type(sample_result))

    def test_create_csv_from_list_values_shape(self):
        """
            case :
            Compare the shape of output dataframe from create_csv_from_list_values() with desired shape.
        """

        result = fn.create_csv_from_list_values([1],[1],[1],[1],[1],[1])
        self.assertEqual(result.shape,(1,6))


    def test_create_csv_from_list_values_length_assert(self):
        """
            case  :
            Make sure if length of all list is not same, it raises an assertion
        """

        with self.assertRaises(CustomErrors.ListLengthNotMatching):
            result = fn.create_csv_from_list_values([1],[1],[1],[1],[1],[1,2])


    def test_download_and_save_zip_file_assert(self):
        """
            Case :
            If the input url is wrong make sure its raises an assertion
        """
        with self.assertRaises(CustomErrors.UnableToDownloadDLTINSZip):
            result = fn.download_and_save_zip_file("dummy url")


    def test_save_dataframe_as_csv_assert(self):
        """
            Case:
            If the input name is null the function should raise an assertion
        """
        with self.assertRaises(CustomErrors.UnableToWriteCsvInToDisk):
            result = fn.save_dataframe_as_csv(pd.DataFrame(),123)




if __name__ == '__main__':
    unittest.main()
