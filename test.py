import unittest
from unittest.mock import patch, mock_open
import os
from Index import read_integer, reading_race_results, read_integer_between_numbers,race_venues
 # Adjust import if necessary

class TestIndexFunctions(unittest.TestCase):

    # Tests for read_integer
    
    @patch('builtins.input', return_value='5')
    def test_read_integer_valid(self, mock_input):
        result = read_integer("Enter a number: ")
        self.assertEqual(result, 5)

    @patch('builtins.input', side_effect=['-1', '5'])
    def test_read_integer_negative(self, mock_input):
        with patch('builtins.print') as mock_print:
            result = read_integer("Enter a number: ")
            mock_print.assert_called_with("Sorry - number only, please.")
        self.assertEqual(result, 5)

    @patch('builtins.input', side_effect=['abc', '5'])
    def test_read_integer_non_integer(self, mock_input):
        with patch('builtins.print') as mock_print:
            result = read_integer("Enter a number: ")
            mock_print.assert_called_with("Invalid input. Please enter a valid integer.")
        self.assertEqual(result, 5)

    # Tests for reading_race_results

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='1,300\n2,600\n3,400')
    def test_reading_race_results_valid(self, mock_isfile, mock_file):
        ids, times = reading_race_results('valid_data')
        self.assertEqual(ids, ('1', '3', '2'))
        self.assertEqual(times, (300, 400, 600))

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='1,300\ninvalid,line\n3,400')
    @patch('builtins.print')
    def test_reading_race_results_invalid_line(self, mock_print, mock_isfile, mock_file):
        ids, times = reading_race_results('invalid_line')
        self.assertEqual(ids, ('1', '3'))  # Assuming this is the correct expected outcome
        self.assertEqual(times, (300, 400))
       


    @patch('os.path.isfile', return_value=False)
    @patch('builtins.print')
    def test_reading_race_results_nonexistent_file(self, mock_print, mock_isfile):
        ids, times = reading_race_results('nonexistent')
        self.assertEqual(ids, [])
        self.assertEqual(times, [])
        mock_print.assert_called_with("Invalid file path: nonexistent.txt")

     # Test read_integer_between_numbers with valid input within range
    @patch('builtins.input', return_value='5')
    def test_read_integer_between_valid(self, mock_input):
        result = read_integer_between_numbers("Enter a number: ", 1, 10)
        self.assertEqual(result, 5)

    # Test read_integer_between_numbers with input outside range
    @patch('builtins.input', side_effect=['0', '11', '5'])
    @patch('builtins.print')
    def test_read_integer_between_outside_range(self, mock_print, mock_input):
        result = read_integer_between_numbers("Enter a number: ", 1, 10)
        mock_print.assert_any_call("Please enter a number between 1 and 10.")
        self.assertEqual(result, 5)

    # Test read_integer_between_numbers with non-integer input
    @patch('builtins.input', side_effect=['abc', '5'])
    @patch('builtins.print')
    def test_read_integer_between_non_integer(self, mock_print, mock_input):
        result = read_integer_between_numbers("Enter a number: ", 1, 10)
        mock_print.assert_called_with("Invalid input. Please enter a valid number.")
        self.assertEqual(result, 5)    

    #Test for race_venues
    @patch('builtins.open', new_callable=mock_open, read_data='Race1,Location1\nRace2,Location2\n')
    @patch('Index.RACES_FILE', 'dummy_races_file.txt')  # Mock the RACES_FILE constant if necessary
    def test_race_venues(self, mock_file):
        venues = race_venues()
        self.assertEqual(venues, ['Race1', 'Race2'])
if __name__ == '__main__':
    unittest.main()
