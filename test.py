import unittest
from unittest.mock import patch, mock_open, call
import os
from Index import*

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

    # Test for runners_data
    @patch('builtins.open', new_callable=mock_open, read_data='Runner1,ID1\nRunner2,ID2\n')
    @patch('Index.RUNNERS_FILE', 'dummy_runners_file.txt')  # Mock the RUNNERS_FILE constant if necessary
    def test_runners_data(self, mock_file):
        names, ids = runners_data()
        self.assertEqual(names, ['Runner1', 'Runner2'])
        self.assertEqual(ids, ['ID1', 'ID2'])

    @patch('builtins.open', new_callable=mock_open, read_data='InvalidLine\nRunner1,ID1\n')
    @patch('builtins.print')
    @patch('Index.RUNNERS_FILE', 'dummy_runners_file.txt')
    def test_runners_data_invalid_line(self, mock_print, mock_file):
        names, ids = runners_data()
        self.assertEqual(names, ['Runner1'])
        self.assertEqual(ids, ['ID1'])
        mock_print.assert_called_with("Invalid line in runners file: InvalidLine\n")

    #Test for competitors_by_county
    @patch('builtins.print')
    def test_competitors_by_county(self, mock_print):
        names = ['Alice', 'Bob', 'Charlie']
        ids = ['AB123', 'AB456', 'CD789']
        competitors_by_county(names, ids)

        expected_calls = [
            call('AB runners'),
            call('===================='),
            call('Alice (AB123)'),
            call('Bob (AB456)'),
            call('CD runners'),
            call('===================='),
            call('Charlie (CD789)')
        ]

        mock_print.assert_has_calls(expected_calls, any_order=False)
    
    # Test for user_venue
@patch('Index.read_nonempty_string', side_effect=['NewLocation', '10', '15', '0'])  # Updated to 'NewLocation'
@patch('Index.read_integer', side_effect=[10, 15, 0])  # Sample times for runners, 0 to stop
@patch('builtins.open', new_callable=mock_open)
@patch('builtins.input', side_effect=['Newlocation', '10', '15', '0'])  # Define mock_input here
def test_users_venue(self, mock_input, mock_file_open, mock_read_integer, mock_read_nonempty_string):
        runners_id = ['ID1', 'ID2']
        races_location = ['OldLocation']

        users_venue(races_location, runners_id)

        # Check if the new location was added
        self.assertIn('NewLocation', races_location)

        # Check if the file was opened correctly
        mock_file_open.assert_called_once_with('NewLocation.txt', 'a')

        # Check the write calls to the file
        mock_file_open().write.assert_has_calls([
            call('ID1,10,\n'),
            call('ID2,15,\n')
        ], any_order=False)

        # Check if read_integer was called correctly
        mock_read_integer.assert_has_calls([
            call('Time for ID1 >>'),
            call('Time for ID2 >>')
        ], any_order=False)

    #Test updating_race_file
@patch('builtins.open', new_callable=mock_open)
def test_updating_races_file(self, mock_file_open):
    races_location = ['Race1', 'Race2', 'Race3']

    # Import the updating_races_file function here or provide the necessary import

    # Call the function
    updating_races_file(races_location)

    # Check if the file was opened correctly
    mock_file_open.assert_called_once_with('races.txt', 'w')

    # Check the write calls to the file
    mock_file_open().write.assert_has_calls([
        call('Race1\n'),
        call('Race2\n'),
        call('Race3\n')
    ], any_order=False)




if __name__ == '__main__':
    unittest.main()
