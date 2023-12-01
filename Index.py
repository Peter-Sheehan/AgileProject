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

def display_podium_places(races_location):
    print("Race Podium Places")
    print("=" * 30)

    for location in races_location:
        ids, times = reading_race_results(location)

        print(f"{location}:")
        for position, (runner_id, time) in enumerate(zip(ids, times), 1):
            print(f"   {position}. {runner_id} - Time: {time} seconds")
        print()

def get_podium(ids, times):
    podium = []
    sorted_results = sorted(zip(ids, times), key=lambda x: x[1])[:3]

    for result in sorted_results:
        podium.append(result[0])

    return podium

def display_race_times_for_competitor(races_location, runners_name, runners_id):
    print("Select a competitor:")
    for i, name in enumerate(runners_name):
        print(f"{i + 1}. {name}")

    selected_index = read_integer_between_numbers("Enter the competitor's number: ", 1, len(runners_name))
    selected_runner_id = runners_id[selected_index - 1]
    selected_runner_name = runners_name[selected_index - 1]

    print(f"\nRace times for {selected_runner_name} ({selected_runner_id}):")
    print("=" * 45)

    for location in races_location:
        ids, times = reading_race_results(location)
        try:
            index = ids.index(selected_runner_id)
            time_taken = times[index]
            if time_taken is not None:
                minutes, seconds = convert_time_to_minutes_and_seconds(time_taken)
                came_in_race, number_in_race = sorting_where_runner_came_in_race(location, time_taken)
                print(f"{location}: {minutes} mins {seconds} secs")
            else:
                print(f"{location}: 0")
        except ValueError:
            print(f"{location}: 0")

def display_runners_who_won(races_location, runners_names, runners_ids):
    print("Competitors who have won at least one race:")
    print("=" * 45)

    winners = set()
    for location in races_location:
        results = reading_race_results(location)
        if results[0]:  # Check if there are results for the race
            fastest_runner = results[0][0]
            winners.add(fastest_runner)

    if not winners:
        print("No winners found.")
    else:
        for winner_id in winners:
            winner_name = find_name_of_winner(winner_id, runners_names, runners_ids)
            if winner_name:
                print(f"{winner_name} ({winner_id})")
            else:
                print(f"Runner with ID {winner_id} not found in the runners data.")


def display_runners_without_podium(races_location, runners_name, runners_id):
    print("Competitors who have not taken a podium position:")
    print("=" * 45)

    podium_runners = set()
    for location in races_location:
        ids, _ = reading_race_results(location)
        podium = get_podium(ids, _)
        podium_runners.update(podium)

    non_podium_runners = set(runners_id) - podium_runners

    for non_podium_runner_id in non_podium_runners:
        non_podium_runner_name = find_name_of_winner(non_podium_runner_id, runners_name, runners_id)
        print(f"{non_podium_runner_name} ({non_podium_runner_id})")

def main():
    MENU = "1. View Race Venues\n2. View Runners\n3. View Race Results\n4. Podium Places\n5. Race Times for Competitor\n6. Runners Who Won\n7. Runners Without Podium\n8. Quit\nEnter your choice:\n"
    input_menu = 0

    while input_menu != 8:
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
        elif input_menu == 4:
            venues = race_venues()
            display_podium_places(venues)
        elif input_menu == 5:
            venues = race_venues()
            runners_names, runners_ids = runners_data()
            display_race_times_for_competitor(venues, runners_names, runners_ids)
        elif input_menu == 6:
            venues = race_venues()
            runners_names, runners_ids = runners_data()
            display_runners_who_won(venues, runners_names, runners_ids)
        elif input_menu == 7:
            venues = race_venues()
            runners_names, runners_ids = runners_data()
            display_runners_without_podium(venues, runners_names, runners_ids)

        input_menu = read_integer_between_numbers(MENU, 1, 8)

if __name__ == "__main__":
    main()
