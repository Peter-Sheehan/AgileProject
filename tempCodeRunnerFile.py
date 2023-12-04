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

    #Test sorting where runner came in race 
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Runner1,240\nRunner2,150\nRunner3,180\n")
    def test_sorting_where_runner_came_in_race_valid(self, mock_file, mock_isfile):
        position, number_in_race = sorting_where_runner_came_in_race("test_location", 180)
        self.assertEqual(position, 2)
        self.assertEqual(number_in_race, 3)

    @patch('os.path.isfile', return_value=False)
    def test_sorting_where_runner_came_in_race_invalid_file(self, mock_isfile):
        position, number_in_race = sorting_where_runner_came_in_race("nonexistent_location", 180)
        self.assertIsNone(position)
        self.assertIsNone(number_in_race)

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_sorting_where_runner_came_in_race_empty_file(self, mock_file, mock_isfile):
        position, number_in_race = sorting_where_runner_came_in_race("empty_file", 180)
        self.assertIsNone(position)
        self.assertIsNone(number_in_race)

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Invalid Data")
    def test_sorting_where_runner_came_in_race_malformed_data(self, mock_file, mock_isfile):
        position, number_in_race = sorting_where_runner_came_in_race("malformed_data", 180)
        self.assertIsNone(position)
        self.assertIsNone(number_in_race)

    #Test display_podium_places
        @patch('Index.reading_race_results')
        @patch('Index.get_podium')
        @patch('Index.find_name_of_winner')
        @patch('builtins.print')
        def test_display_podium_places(self, mock_print, mock_find_name_of_winner, mock_get_podium, mock_reading_race_results):
            # Mock data setup
            races_location = ['Race1', 'Race2']
            runners_name = ['Alice', 'Bob', 'Charlie']
            runners_id = ['ID1', 'ID2', 'ID3']

            # Mock responses for reading_race_results
            mock_reading_race_results.side_effect = [
                (['ID1', 'ID2', 'ID3'], [300, 400, 500]),
                (['ID3', 'ID2', 'ID1'], [350, 450, 550])
            ]

            # Mock responses for get_podium
            mock_get_podium.side_effect = [
                ['ID1', 'ID2', 'ID3'],
                ['ID3', 'ID2', 'ID1']
            ]

            # Mock responses for find_name_of_winner
            mock_find_name_of_winner.side_effect = lambda runner_id, names, ids: names[ids.index(runner_id)]

            # Call the function
            display_podium_places(races_location, runners_name, runners_id)

            # Expected print calls
            expected_print_calls = [
                call("Race Podium Places"),
                call("=" * 50),
                call("\nRace1:"),
                call("=" * 30),
                call("| Position | Runner ID | Runner Name | Time (seconds) |"),
                call("|-----------|-----------|-------------|-----------------|"),
                call("| 1         | ID1        | Alice   | 300              |"),
                call("| 2         | ID2        | Bob   | 400              |"),
                call("| 3         | ID3        | Charlie   | 500              |"),
                call("\nRace2:"),
                call("=" * 30),
                call("| Position | Runner ID | Runner Name | Time (seconds) |"),
                call("|-----------|-----------|-------------|-----------------|"),
                call("| 1         | ID3        | Charlie   | 350              |"),
                call("| 2         | ID2        | Bob   | 450              |"),
                call("| 3         | ID1        | Alice   | 550              |"),
                call("\n")
            ]

            mock_print.assert_has_calls(expected_print_calls, any_order=False)

