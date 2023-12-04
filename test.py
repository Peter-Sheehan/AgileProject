import unittest
from unittest.mock import patch, mock_open
import os
from Index import read_integer, reading_race_results  # Adjust import if necessary

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
def test_reading_race_results_valid(self, mock_file, mock_isfile):
    ids, times = reading_race_results('valid_data')
    self.assertEqual(ids, ('1', '3', '2'))
    self.assertEqual(times, (300, 400, 600))


    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='1,300\ninvalid,line\n3,400')
    @patch('builtins.print')
    def test_reading_race_results_invalid_line(self, mock_print, mock_file, mock_isfile):
        ids, times = reading_race_results('invalid_line')
        self.assertEqual(ids, ('3', '1'))
        self.assertEqual(times, (400, 300))
        mock_print.assert_called_with("Invalid line in invalid_line.txt: invalid,line\n")

    @patch('os.path.isfile', return_value=False)
    @patch('builtins.print')
    def test_reading_race_results_nonexistent_file(self, mock_print, mock_isfile):
        ids, times = reading_race_results('nonexistent')
        self.assertEqual(ids, [])
        self.assertEqual(times, [])
        mock_print.assert_called_with("Invalid file path: nonexistent.txt")

if __name__ == '__main__':
    unittest.main()
