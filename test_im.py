import inventory_manager as im
import unittest
from unittest import mock
from unittest.mock import patch, MagicMock, mock_open
#python -m unittest -v test_im.py

# Test Cases For User Input Checks 
# https://stackoverflow.com/questions/47690020/python-3-unit-tests-with-user-input
# https://stackoverflow.com/questions/21046717/how-can-i-mock-user-input-from-input-in-3-x-or-raw-input-in-2-x-for-a-uni
# https://docs.python.org/3/library/unittest.mock.html
# https://docs.python.org/3/library/unittest.mock.html#magic-mock
class TestYesNoCheck(unittest.TestCase):
    # @path When function calls for e.g. input, put in 'y'
    @patch('builtins.input', side_effect=['y']) # Input
    # mock_input is the virtual input in the function
    def test_positive_response_y(self, mock_input): 
        # im.yes_no_check, call the function and put 'Test' in as prompt * 'Test' Not Important For This Function
        # store result from function in result (which result = True)
        result = im.yes_no_check('Test')
        # self.assertTrue(result) assertTrue is expected to get a True which it does.
        self.assertTrue(result) 
    
    @patch('builtins.input', side_effect=['yes'])
    def test_positive_response_yes(self, mock_input):
        result = im.yes_no_check('Test')
        self.assertTrue(result)

    @patch('builtins.input', side_effect=['n'])
    def test_negative_response(self, mock_input):
        result = im.yes_no_check('Test')
        self.assertFalse(result)

    @patch('builtins.input', side_effect=['no'])
    def test_negative_response_no(self, mock_input):
        result = im.yes_no_check('Test')
        self.assertFalse(result)

    @patch('builtins.input', side_effect=['invalid', 'y'])
    def test_invalid_then_positive_invalid_y(self, mock_input):
        result = im.yes_no_check('Test')
        self.assertTrue(result)

    @patch('builtins.input', side_effect=['foo', 'n'])
    def test_invalid_then_negative_response_foo_n(self, mock_input):
        result = im.yes_no_check('Test')
        self.assertFalse(result)

class TestUsrInputNum(unittest.TestCase):
    @patch('builtins.input', side_effect=['10.5'])
    def test_valid_float_input(self, mock_input):
        result = im.usr_input_num('Enter Num')
        self.assertEqual(result, 10.5)

    @patch('builtins.input', side_effect=['foo', '15'])
    def test_invalid_then_valid_input(self, mock_input):
        result = im.usr_input_num('Enter Num')
        self.assertEqual(result, 15)

class TestUsrInputBool(unittest.TestCase):
    @patch('builtins.input', side_effect=['True'])
    def test_valid_true_input(self, mock_input):
        result = im.usr_input_boolean('T/F')
        self.assertEqual(result, 'True')

    @patch('builtins.input', side_effect=['False'])
    def test_valid_false_input(self, mock_input):
        result = im.usr_input_boolean('T/F')
        self.assertEqual(result, 'False')

    @patch('builtins.input', side_effect=['invalid', 'True'])
    def test_invalid_then_valid_true_input(self, mock_input):
        result = im.usr_input_boolean('T/F')
        self.assertEqual(result, 'True')

class TestUsrInputRatio(unittest.TestCase):
    @patch('builtins.input', side_effect=['2', '3'])
    def test_valid_ratio_input(self, mock_input):
        result = im.usr_input_ratio('Ratio')
        self.assertEqual(result, '2.0:3.0')

    @patch('builtins.input', side_effect=['5', '5'])
    def test_equal_numbers_ratio_input(self, mock_input):
        result = im.usr_input_ratio('Ratio')
        self.assertEqual(result, '1.0')

    @patch('builtins.input', side_effect=['invalid', '4', 'invalid', '7'])
    def test_invalid_then_valid_ratio_input(self, mock_input):
        result = im.usr_input_ratio('Ratio')
        self.assertEqual(result, '4.0:7.0')

# Test Case For Least Square Calculation
class TestCalculateLeastSquare(unittest.TestCase):

    # @patch mocking print and line_graph() 
    @patch('builtins.print')
    @patch('inventory_manager.line_graph')
    # mock_print and line_graph() in the function
    def test_positive_limit(self, mock_line_graph, mock_print):
        # Make calculate_least_square_to_limit() arguments
        name = 'Test Case 1'
        y = [10, 20, 30, 40, 50]
        limit = 100
        # Put in arguments and run function
        im.calculate_least_square_to_limit(name, y, limit)
        # Checks if print was called and if the message was correct
        mock_print.assert_called_with(f'Projected {len(y)-1} Days Left!')
        # Checks if line_graph() was call once
        mock_line_graph.assert_called_once()

    @patch('builtins.print')
    @patch('inventory_manager.line_graph')
    def test_zero_limit(self, mock_line_graph, mock_print):
        name = 'Test Case 2'
        y = [10, 20, 30, 40, 50]
        limit = 0
        im.calculate_least_square_to_limit(name, y, limit)
        mock_print.assert_called_with('Error: Total Amount <= 0. Incorrect Data In Database! There Must Be Atleast 1.')

    @patch('builtins.print')
    @patch('inventory_manager.line_graph')
    def test_negative_limit(self, mock_line_graph, mock_print):
        name = 'Test Case 3'
        y = [10, 20, 30, 40, 50]
        limit = -100
        im.calculate_least_square_to_limit(name, y, limit)
        mock_print.assert_called_with('Error: Total Amount <= 0. Incorrect Data In Database! There Must Be Atleast 1.')

    @patch('builtins.print')
    @patch('inventory_manager.line_graph')
    def test_empty_data(self, mock_line_graph, mock_print):
        name = 'Test Case 4'
        y = []
        limit = 100
        im.calculate_least_square_to_limit(name, y, limit)
        mock_print.assert_called_with(f'No Useable Data Available For {name}')
        mock_line_graph.assert_not_called()

if __name__ == '__main__':# Make calculate_least_square_to_limit() arguments
    unittest.main()