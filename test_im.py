from inventory_manager import usr_input_num
import unittest
from unittest import mock
from unittest.mock import patch
#python -m unittest -v test_im.py

    
class TestUserTryFunc(unittest.TestCase):
    
    def test_main(self, mocked_input):
        with unittest.mock.patch('builtins.input', return_value=1):
            mocked_input.side_effect = '1'


    #Test usr_input_num with input as 1
    @mock.patch('inventory_manager.input', create=True)
    def test_usr_input_num(self, mocked_input):
        mocked_input.side_effect = '1'
        num = usr_input_num('test')
        expected_num = 1
        assert num == expected_num




    # @mock.patch('inventory_manager.input', create=True) 
    # def test_usr_input_boolean(self, mocked_input):
    #     mocked_input.side_effect = 'True'
    #     boolean = usr_input_num('test')
    #     expected_bool = 'True'
    #     assert boolean == expected_bool


    # @mock.patch('input', return_value='1')
    # def test_valid_input(self, mock_input):
     

    # @patch('builtins.input', side_effect=['42'])
    # def test_valid_input(self, mock_input):
    #     result = im.usr_input_num("Enter a number: ")
    #     self.assertEqual(result, 42.0)

    # @patch('builtins.input', side_effect=['abc', '10'])
    # def test_invalid_then_valid_input(self, mock_input):
    #     result = im.usr_input_num("Enter a number: ")
    #     self.assertEqual(result, 10.0)

    # @patch('builtins.input', side_effect=['abc', 'xyz', '123'])
    # def test_invalid_then_valid_then_valid_input(self, mock_input):
    #     result = im.usr_input_num("Enter a number: ")
    #     self.assertEqual(result, 123.0)


# Add more test cases as needed
if __name__ == '__main__':
    unittest.main()