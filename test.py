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
    @patch('Index.read_nonempty_string', side_effect=['NewLocation', '0', '15', '0'])  # Include 0 as time for the first runner
    @patch('Index.read_integer', side_effect=[0, 15, 0])  # The first runner's time is 0, which should trigger the writing
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.input', side_effect=['Newlocation', '0', '15', '0'])
    def test_users_venue(self, mock_input, mock_file_open, mock_read_integer, mock_read_nonempty_string):
        runners_id = ['ID1', 'ID2']
        races_location = ['OldLocation']

        users_venue(races_location, runners_id)

        # Check if the new location was added
        self.assertIn('Newlocation', races_location)  # Match the case with the mock input

        # Check if the file was opened correctly
        mock_file_open.assert_called_once_with('Newlocation.txt', 'a')

        # Check the write calls to the file
        mock_file_open().write.assert_has_calls([
            call('ID1,0,'),
            call('\n')
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
            call('Race1'),
            call('\n'),
            call('Race2'),
            call('\n'),
            call('Race3'),
            call('\n')
        ], any_order=False)

    #Test winner_of_race
    def test_winner_of_race(self):
            # Test with normal data
            ids, times = ['ID1', 'ID2', 'ID3'], [300, 400, 200]
            winner = winner_of_race(ids, times)
            self.assertEqual(winner, 'ID3')  # ID3 has the minimum time (200)

            # Test with empty ids
            ids, times = [], [300, 400, 500]
            winner = winner_of_race(ids, times)
            self.assertIsNone(winner)

            # Test with empty times
            ids, times = ['ID1', 'ID2', 'ID3'], []
            winner = winner_of_race(ids, times)
            self.assertIsNone(winner)

            # Test with both ids and times as empty
            ids, times = [], []
            winner = winner_of_race(ids, times)
            self.assertIsNone(winner)

            # Test with ids as None
            winner = winner_of_race(None, [300, 400, 500])
            self.assertIsNone(winner)

            # Test with times as None
            winner = winner_of_race(['ID1', 'ID2', 'ID3'], None)
            self.assertIsNone(winner)

            # Test with both ids and times as None
            winner = winner_of_race(None, None)
            self.assertIsNone(winner)
    #Test fine_name_of_winner
    
    def test_find_name_of_winner(self):
        # Setup mock data
        runners_name = ['Alice', 'Bob', 'Charlie']
        runners_id = ['ID1', 'ID2', 'ID3']

        # Test with a matching winner_id
        winner_id = 'ID2'
        winner_name = find_name_of_winner(winner_id, runners_name, runners_id)
        self.assertEqual(winner_name, 'Bob')

        # Test with no matching winner_id
        winner_id = 'ID4'
        winner_name = find_name_of_winner(winner_id, runners_name, runners_id)
        self.assertIsNone(winner_name)

        # Test with empty lists
        winner_id = 'ID1'
        winner_name = find_name_of_winner(winner_id, [], [])
        self.assertIsNone(winner_name)

        #Test convert_time_to_minute_and_seconds
        def test_convert_time_to_minutes_and_seconds(self):
            # Test with normal data
            time_taken = 125  # 2 minutes and 5 seconds
            minutes, seconds = convert_time_to_minutes_and_seconds(time_taken)
            self.assertEqual(minutes, 2)
            self.assertEqual(seconds, 5)

            # Test with time_taken as zero
            time_taken = 0
            minutes, seconds = convert_time_to_minutes_and_seconds(time_taken)
            self.assertEqual(minutes, 0)
            self.assertEqual(seconds, 0)

            # Test with time_taken exactly 60 seconds
            time_taken = 60
            minutes, seconds = convert_time_to_minutes_and_seconds(time_taken)
            self.assertEqual(minutes, 1)
            self.assertEqual(seconds, 0)

            # Test with a large value of time_taken
            time_taken = 3665  # 61 minutes and 5 seconds
            minutes, seconds = convert_time_to_minutes_and_seconds(time_taken)
            self.assertEqual(minutes, 61)
            self.assertEqual(seconds, 5)

    #Test sorting_where_runner_came_in_race
    def test_sorting_where_runner_came_in_race(self):
        with patch('os.path.isfile', return_value=True):
            with patch('builtins.open', new_callable=mock_open, read_data="Runner1,300\nRunner2,200\nRunner3,250\n"):
                # Test with valid data
                position, number_in_race = sorting_where_runner_came_in_race("valid_location", 250)
                self.assertEqual(position, 2)
                self.assertEqual(number_in_race, 3)

            with patch('builtins.open', new_callable=mock_open, read_data=""):
                # Test with empty file
                position, number_in_race = sorting_where_runner_came_in_race("empty_location", 250)
                self.assertIsNone(position)
                self.assertIsNone(number_in_race)

        with patch('os.path.isfile', return_value=False):
            # Test with invalid file path
            position, number_in_race = sorting_where_runner_came_in_race("invalid_location", 250)
            self.assertIsNone(position)
            self.assertIsNone(number_in_race)

        with patch('os.path.isfile', return_value=True):
            with patch('builtins.open', new_callable=mock_open, read_data="Runner1,xyz\nRunner2,200\n"):
                # Test with file containing invalid data
                position, number_in_race = sorting_where_runner_came_in_race("invalid_data_location", 200)
                self.assertIsNone(position)
                self.assertIsNone(number_in_race)

        
        with patch('os.path.isfile', return_value=True):
            with patch('builtins.open', new_callable=mock_open, read_data="Runner1,300\nRunner2,200\n"):
                # Test searching for non-existent time
                position, number_in_race = sorting_where_runner_came_in_race("valid_location", 400)
                self.assertIsNone(position)
                self.assertIsNone(number_in_race)  # Expect None for both position and number_in_race if time is not found

    #Test get_podium
    def test_get_podium(self):
        # Test with normal data
        ids = ['ID1', 'ID2', 'ID3', 'ID4']
        times = [300, 250, 400, 200]
        podium = get_podium(ids, times)
        self.assertEqual(podium, ['ID4', 'ID2', 'ID1'])  # ID4, ID2, ID1 have the lowest times

        # Test with empty lists
        ids = []
        times = []
        podium = get_podium(ids, times)
        self.assertEqual(podium, [])

        # Test with fewer than three participants
        ids = ['ID1', 'ID2']
        times = [300, 250]
        podium = get_podium(ids, times)
        self.assertEqual(podium, ['ID2', 'ID1'])  # Only two participants

        # Test with tie times (optional)
        ids = ['ID1', 'ID2', 'ID3']
        times = [300, 300, 300]
        podium = get_podium(ids, times)
        self.assertEqual(podium, ['ID1', 'ID2', 'ID3'])  # All have the same time




if __name__ == '__main__':
    unittest.main()
