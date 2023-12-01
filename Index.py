import os

RACES_FILE = "races.txt"
RUNNERS_FILE = "runners.txt"


# Task 1

def read_integer_between_numbers(prompt, min_value, max_value):
    while True:
        try:
            user_input = int(input(prompt))
            if min_value <= user_input <= max_value:
                return user_input
            else:
                print(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            
def read_nonempty_string(prompt):
    while True:
        user_input = input(prompt)
        if len(user_input) > 0 and user_input.isalpha():
            return user_input
        else:
            print("Invalid input. Please enter a non-empty string with alphabetic characters.")

def read_integer(prompt):
    while True:
        try:
            user_input = int(input(prompt))
            if user_input >= 0:
                return user_input
            else:
                print("Sorry - number only, please.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            

def race_venues():
    with open(RACES_FILE) as input_file:
        lines = input_file.readlines()
        races_location = [line.split(",")[0].strip("\n") for line in lines]

    return races_location

def reading_race_results(location):
    file_path = f"{location}.txt"
    if not os.path.isfile(file_path):
        print(f"Invalid file path: {file_path}")
        return [], []

    ids = []
    time_taken = []

    with open(file_path) as input_type:
        lines = input_type.readlines()

        for line in lines:
            split_line = line.strip().split(",")
            if len(split_line) >= 2:
                try:
                    runner_id = split_line[0]
                    time_value = int(split_line[1])
                    ids.append(runner_id)
                    time_taken.append(time_value)
                except (ValueError, IndexError):
                    print(f"Invalid line in {file_path}: {line}")
            elif line.strip():  # Check if the line is not empty
                print(f"Invalid line in {file_path}: {line}")

    if not ids or not time_taken:
        print(f"No valid data in {file_path}")
        return [], []

    # Sort ids and time_taken together based on time_taken
    sorted_results = sorted(zip(time_taken, ids), key=lambda x: x[0])
    time_taken, ids = zip(*sorted_results)

    return ids, time_taken

def race_results(races_location):
    for i in range(len(races_location)):
        print(f"{i + 1}:{races_location[i]}")

    user_input = read_integer_between_numbers("Choose a race (enter the number): ", 1, len(races_location))
    selected_race = races_location[user_input - 1]

    id, time_taken = reading_race_results(selected_race)

    return id, time_taken, selected_race

def race_venues():
    with open(RACES_FILE) as input_file:
        lines = input_file.readlines()
        races_location = [line.split(",")[0].strip("\n") for line in lines]

    return races_location


def runners_data():
    with open(RUNNERS_FILE) as input_file:
        lines = input_file.readlines()
        runners_name = []
        runners_id = []

        for line in lines:
            split_line = line.strip().split(",")
            if len(split_line) >= 2:
                runners_name.append(split_line[0])
                runner_id = split_line[1].strip("\n")
                runners_id.append(runner_id)
            else:
                print(f"Invalid line in runners file: {line}")

    return runners_name, runners_id


def competitors_by_county(name, id):
    county_runners = {}

    for i in range(len(name)):
        county_code = id[i][:2]  
        if county_code in county_runners:
            county_runners[county_code].append((name[i], id[i]))
        else:
            county_runners[county_code] = [(name[i], id[i])]

    for county_code, runners in sorted(county_runners.items()):
        print(f"{county_code} runners")
        print("=" * 20)
        for runner in sorted(runners, key=lambda x: x[0]):  # Sort by name
            print(f"{runner[0]} ({runner[1]})")
            
            
            
            
def users_venue(races_location, runners_id):
    while True:
        user_location = read_nonempty_string("Where will the new race take place?").capitalize()
        if user_location not in races_location:
            break
    connection = open(f"{user_location}.txt", "a")
    races_location.append(user_location)
    time_taken = []
    updated_runners = []
    for i in range(len(runners_id)):
        time_taken_for_runner = read_integer(f"Time for {runners_id[i]} >>")
        if time_taken_for_runner == 0:  # Use double equals for comparison
            time_taken.append(time_taken_for_runner)
            updated_runners.append(runners_id[i])
            print(f"{runners_id[i]},{time_taken_for_runner},", file=connection)
    connection.close()

def updating_races_file(races_location):
    connection = open("races.txt", "w")
    for i in range(len(races_location)):
        print(races_location[i], file=connection)
    connection.close()

def winner_of_race(ids, times):
    if not ids or not times:
        return None

    min_time_index = times.index(min(times))
    return ids[min_time_index]

def find_name_of_winner(winner_id, runners_name, runners_id):
    for i in range(len(runners_id)):
        if winner_id == runners_id[i]:
            return runners_name[i]
        
def convert_time_to_minutes_and_seconds(time_taken):
    MINUTE = 60
    minutes = time_taken // MINUTE
    seconds = time_taken % MINUTE
    return minutes, seconds

def sorting_where_runner_came_in_race(location, time):
    file_path = f"{location}.txt"

    if not os.path.isfile(file_path):
        print(f"Invalid file path: {file_path}")
        return None, None

    try:
        with open(file_path) as input_type:
            lines = input_type.readlines()

        if not lines:
            print(f"No data available for {location}")
            return None, None

        time_taken = [int(line.split(",")[1].strip("\n")) for line in lines]
        time_taken.sort()

        position = time_taken.index(time) + 1
        number_in_race = len(lines)

        return position, number_in_race
    except (ValueError, IndexError):
        print(f"")
        return None, None


def main():
    MENU = "1. View Race Venues\n2. View Runners\n3. View Race Results\n7. Quit\nEnter your choice:\n"
    input_menu = 0
    
    while input_menu != 7:
        if input_menu == 1:
            venues = race_venues()
            print("Race Venues:")
            for venue in venues:
                print(venue)
        elif input_menu == 2:
            runners_names, runners_ids = runners_data()
            print("Runners:")

            competitors_by_county(runners_names, runners_ids)
            
        elif input_menu == 3:
            venues = race_venues()
            print("Race Venues:")
            for venue in venues:
                print(venue)
            id, time_taken, selected_race = race_results(venues)
            print(f"Results for {selected_race}:")
            for runner_id, time in zip(id, time_taken):
                print(f"Runner ID: {runner_id}, Time Taken: {time} seconds")
        input_menu = read_integer_between_numbers(MENU, 1, 7)

if __name__ == "__main__":
    main()
