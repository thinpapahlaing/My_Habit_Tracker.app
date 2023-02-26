"""
This 'analytics.py' module was created based on Python Functional Programming and consists of 7 analytics functions for all habits existed in user account.
It imports os, sqlite3, questionary and texttable.
"""

import os
import sqlite3
import questionary
from texttable import Texttable


def show_all_habits(username):
    """
        Displays a table of all habits created by a given user.

        Args:
        -----
            - username (str): The username whose habits are to be displayed.

        Returns:
        -------
            - None
    """

    # Connect to the database
    connect_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'habit_tracker_db.db')
    conn = sqlite3.connect(connect_db)
    cursor = conn.cursor()

    # Retrieve all habits created by the user
    cursor.execute("SELECT habit_name, habit_creator, habit_type, habit_frequency, created_datetime, "
                   "last_completion_date FROM HabitsData WHERE habit_creator=?", (username,))
    habits_list = cursor.fetchall()

    # If there are no habits in the user account, print a message and return
    if len(habits_list) == 0:
        print("There are no habits to display.")
        return

    # Create a table of habit data
    table_data = [['Habit Name', 'Habit Creator', 'Habit Type', 'Habit Frequency', 'Created Datetime',
                   'Last Completion Date']]
    table_data += list(map(lambda h: [h[0], h[1], h[2], h[3], h[4], h[5]], habits_list))

    # Display the table
    table = Texttable()
    table.set_cols_width([20, 20, 15, 20, 30, 30])
    table.add_rows(table_data)
    print("Your all created habits list is as follows :)")
    print(table.draw())


def show_daily_habits(username):
    """
        Displays a table of all daily habits created by a given user.

        Args:
        -----
            - username (str): The username whose habits are to be displayed.

        Returns:
        -------
            - None
    """

    # Connect to the database
    connect_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'habit_tracker_db.db')
    conn = sqlite3.connect(connect_db)
    cursor = conn.cursor()

    # Retrieve all habits created by the user
    cursor.execute("SELECT habit_name, habit_creator, habit_type, habit_frequency, created_datetime, "
                   "last_completion_date FROM HabitsData WHERE habit_creator=? AND habit_frequency='Daily'",
                   (username,))
    habits_list = cursor.fetchall()

    # If there are no habits in the user account, print a message and return
    if len(habits_list) == 0:
        print("There are no daily habits to display.")
        return

    # Create a table of habit data
    table_data = [['Habit Name', 'Habit Creator', 'Habit Type', 'Habit Frequency', 'Created Datetime',
                   'Last Completion Date']]
    table_data += list(map(lambda h: [h[0], h[1], h[2], h[3], h[4], h[5]], habits_list))

    # Display the table
    table = Texttable()
    table.set_cols_width([20, 20, 15, 20, 30, 30])
    table.add_rows(table_data)
    print("Your all created daily habits list is as follows :)")
    print(table.draw())


def show_weekly_habits(username):
    """
        Displays a table of all weekly habits created by a given user.

        Args:
        -----
            - username (str): The username whose habits are to be displayed.

        Returns:
        -------
            - None
    """

    # Connect to the database
    connect_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'habit_tracker_db.db')
    conn = sqlite3.connect(connect_db)
    cursor = conn.cursor()

    # Retrieve all habits created by the user
    cursor.execute("SELECT habit_name, habit_creator, habit_type, habit_frequency, created_datetime, "
                   "last_completion_date FROM HabitsData WHERE habit_creator=? AND habit_frequency='Weekly'",
                   (username,))
    habits_list = cursor.fetchall()

    # If there are no habits in the user account, print a message and return
    if len(habits_list) == 0:
        print("There are no weekly habits to display.")
        return

    # Create a table of habit data
    table_data = [['Habit Name', 'Habit Creator', 'Habit Type', 'Habit Frequency', 'Created Datetime',
                   'Last Completion Date']]
    table_data += list(map(lambda h: [h[0], h[1], h[2], h[3], h[4], h[5]], habits_list))

    # Display the table
    table = Texttable()
    table.set_cols_width([20, 20, 15, 20, 30, 30])
    table.add_rows(table_data)
    print("Your all created weekly habits list is as follows :)")
    print(table.draw())


def current_streak_summary(username):
    """
        Retrieves the habits data created by the user from the database, and displays a table summarizing the current streaks of
        all habits existed in his account.

        Args:
        -----
            - username (str): The username for whom the streak summary has to be shown.

        Returns:
        -------
            - None

    """
    # Connect to the database
    connect_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'habit_tracker_db.db')
    conn = sqlite3.connect(connect_db)
    cursor = conn.cursor()

    # Retrieve all habits created by the user
    cursor.execute("SELECT habit_name, habit_creator, habit_type, habit_frequency, created_datetime, "
                   "last_completion_date, habit_streak FROM HabitsData WHERE habit_creator=?", (username,))
    habits_list = cursor.fetchall()

    # If there are no habits in the user account, print a message and return
    if len(habits_list) == 0:
        print("There are no habits to display current streaks.")
        return

    # Create a table of habit data
    table_data = [['Habit Name', 'Habit Creator', 'Habit Type', 'Habit Frequency', 'Created Datetime',
                   'Last Completion Date', 'Habit Streak']]
    table_data += list(map(lambda h: [h[0], h[1], h[2], h[3], h[4], h[5], h[6]], habits_list))

    # Display the table
    table = Texttable()
    table.set_cols_width([20, 15, 15, 10, 30, 30, 10])
    table.add_rows(table_data)
    print("Your Current Streak Summary of all created habits list is as follows :)")
    print(table.draw())


def current_streak_of_selected_habit(username):
    """
        Retrieves and displays the current streak for a habit selected by the user.

        Args:
        -----
           - username (str): The username of the user.

        Returns:
        -------
            - The current streak of the selected habit.
    """

    # Connect to the database
    connect_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'habit_tracker_db.db')
    conn = sqlite3.connect(connect_db)
    cursor = conn.cursor()

    # Get a list of the user's habits
    cursor.execute("SELECT habit_name, habit_frequency, habit_type FROM HabitsData WHERE habit_creator=?", (username,))
    habits = cursor.fetchall()

    # If the user has not created any habits yet, inform them and exit
    if not habits:
        print("You have not created any habits yet.")
        return

    # Create a list of habit names, frequencies, and types to display to the user
    habit_list = list(map(lambda h: f"{h[0]} ~~~ {h[1]} ~~~ {h[2]}", habits))

    # Prompt the user to select a habit from the list
    selected_habit = questionary.select("Select a habit from the list:", choices=habit_list).ask()
    selected_habit_name = selected_habit.split("~~~")[0].strip()
    selected_habit_frequency = selected_habit.split("~~~")[1].strip()
    selected_habit_type = selected_habit.split("~~~")[2].strip()

    # Retrieve the current streak for the selected habit
    result = cursor.execute("SELECT habit_streak FROM HabitsData WHERE habit_name= ? and habit_creator= ? "
                            "and habit_type= ? and habit_frequency= ?",
                            (selected_habit_name, username, selected_habit_type, selected_habit_frequency)).fetchone()
    current_streak = result[0]

    # Display the current streak to the user and return the result
    print("The current streak of your selected habit is as follows.")
    print(f"Current streak of {selected_habit}: {current_streak}")
    return result


def longest_streak_summary(username):
    """
        Retrieves the habits data created by the user from the database, and displays a table summarizing the longest run streaks of
        all habits existed in his account.

        Args:
        -----
            - username (str): The username for whom the streak summary has to be shown.

        Returns:
        -------
            - None

    """

    # Connect to the database
    connect_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'habit_tracker_db.db')
    conn = sqlite3.connect(connect_db)
    cursor = conn.cursor()

    # Retrieve all habits created by the user
    cursor.execute("SELECT habit_name, habit_creator, habit_type, habit_frequency, streak_start_date, "
                   "streak_end_date, MAX(streak_length) as longest_streak "
                   "FROM StreaksData WHERE habit_creator=? "
                   "GROUP BY habit_name, habit_creator, habit_type, habit_frequency", (username,))
    habits_list = cursor.fetchall()

    # If there are no habits in the user account, print a message and return
    if len(habits_list) == 0:
        print("There are no habits to display longest run streaks.")
        return

    # Create a table of habit data
    table_data = [['Habit Name', 'Habit Creator', 'Habit Type', 'Habit Frequency', 'Streak Start Date',
                   'Streak End Date', 'Habit Streak']]
    table_data += list(map(lambda h: [h[0], h[1], h[2], h[3], h[4], h[5], h[6]], habits_list))

    # Display the table
    table = Texttable()
    table.set_cols_width([20, 15, 15, 10, 30, 30, 10])
    table.add_rows(table_data)
    print("Your Longest run Streak Summary of all created habits list is as follows :)")
    print(table.draw())


def longest_streak_of_selected_habit(username):
    """
        Retrieves and displays the longest run streak for a habit selected by the user.

        Args:
        -----
            - username (str): The username of the user.

        Returns:
        -------
            - The longest run streak of the selected habit.
    """

    # Connect to the database
    connect_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'habit_tracker_db.db')
    conn = sqlite3.connect(connect_db)
    cursor = conn.cursor()

    # Get a list of the user's habits
    cursor.execute("SELECT habit_name, habit_frequency, habit_type FROM HabitsData WHERE habit_creator=?", (username,))
    habits = cursor.fetchall()

    # If the user has not created any habits yet, inform them and exit
    if not habits:
        print("You have not created any habits yet.")
        return

    # Create a list of habit names, frequencies, and types to display to the user
    habit_list = list(map(lambda h: f"{h[0]} ~~~ {h[1]} ~~~ {h[2]}", habits))

    # Prompt the user to select a habit from the list
    selected_habit = questionary.select("Select a habit from the list:", choices=habit_list).ask()
    selected_habit_name = selected_habit.split("~~~")[0].strip()
    selected_habit_frequency = selected_habit.split("~~~")[1].strip()
    selected_habit_type = selected_habit.split("~~~")[2].strip()

    # Retrieve the longest run streak for the selected habit
    result = cursor.execute("SELECT MAX(streak_length) as longest_streak FROM StreaksData "
                            "WHERE habit_name= ? and habit_creator= ? and habit_type= ? and habit_frequency= ?",
                            (selected_habit_name, username, selected_habit_type, selected_habit_frequency)).fetchone()
    longest_streak = result[0]

    # Display the longest run streak to the user and return the result
    print("The longest run streak of your selected habit is as follows.")
    print(f"Longest streak of {selected_habit}: {longest_streak}")
    return result
