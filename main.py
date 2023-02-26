"""
This module is the main module of the whole habit tracker app.
While running this module, the user can do various functions.
It imports Habit class from Habit module, UserProfile class from functions module, analytics module, os and sqlite3.
"""

import sqlite3
import analytics
from Habit import Habit
from functions import UserProfile


def main(forename=None, surname=None, username=None, password=None, habit_name=None, habit_creator=None,
         habit_type=None, habit_frequency=None, created_datetime=None, last_completion_date=None, habit_streak=0,
         streak_start_date=None, streak_end_date=None, streak_length=0):

    """
        The main function is the entry point of the Habit Tracker App.
        It allows a user to register, login, and select options from the menu to interact with their habits.

        Parameters:
        -----------
            - forename (str): The user's forename.
            - surname (str): The user's surname.
            - username (str): The user's entered username.
            - password (str): The user's entered password.
            - habit_name (str): Name of the habit
            - habit_creator (str): Username of the user who created the habit
            - habit_type (str): Type of the habit (Physical Health, Emotional Relaxation, Personal Growth, Relationships)
            - habit_frequency (str): Frequency of the habit (Daily and Weekly)
            - created_datetime (datetime): Datetime when the habit was created
            - last_completion_date (str): Datetime when the habit was last completed
            - streak_start_date (datetime): Datetime when the first streak starts
            - streak_end_date (datetime): Datetime when the habit streak ends
            - streak_length (int): The length of a habit streak
            - habit_streak(int): The number of a habit streak
    """

    # Connect to the database and Create the necessary tables
    conn = sqlite3.connect('habit_tracker_db.db')
    habit_obj = Habit(habit_name, habit_creator, habit_type, habit_frequency, created_datetime,
                      last_completion_date, streak_start_date, streak_end_date, streak_length, habit_streak)
    habit_obj.habits_table()
    habit_obj.streaks_table()
    habit_obj.users_table()

    # Print out welcome messages to the user in a visual way
    print("\n" * 2)
    print(" /$$      /$$ /$$$$$$$$ /$$        /$$$$$$   /$$$$$$  /$$      /$$ /$$$$$$$$ /$$")
    print("| $$  /$ | $$| $$_____/| $$       /$$__  $$ /$$__  $$| $$$    /$$$| $$_____/| $$")
    print("| $$ /$$$| $$| $$      | $$      | $$  \__/| $$  \ $$| $$$$  /$$$$| $$      | $$")
    print("| $$/$$ $$ $$| $$$$$   | $$      | $$      | $$  | $$| $$ $$/$$ $$| $$$$$   | $$")
    print("| $$$$_  $$$$| $$__/   | $$      | $$      | $$  | $$| $$  $$$| $$| $$__/   |__/")
    print("| $$$/ \  $$$| $$      | $$      | $$    $$| $$  | $$| $$\  $ | $$| $$          ")
    print("| $$/   \  $$| $$$$$$$$| $$$$$$$$|  $$$$$$/|  $$$$$$/| $$ \/  | $$| $$$$$$$$ /$$")
    print("|__/     \__/|________/|________/ \______/  \______/ |__/     |__/|________/|__/")

    print("\nWelcome to the Habit Tracker App! :)"
          "\nThis app helps you track your habits and maintain streaks to achieve your goals. Let's get started! ~~~")
    print("\n" * 3)

    # check if user is logging in or registering for the first time
    while True:
        is_first_time = input("Are you a first-time user? (yes/no)")
        if is_first_time == "yes":
            user_obj = UserProfile(forename, surname, username, password)
            user_obj.register()
            username = user_obj.username
            menu(username, habit_obj, user_obj)
            conn.commit()
            break
        elif is_first_time == "no":
            user_obj = UserProfile(forename, surname, username, password)
            user_obj.login()
            username = user_obj.username
            menu(username, habit_obj, user_obj)
            conn.commit()
            break
        else:
            print("Please type only 'yes' or 'no'")


def menu(username, habit_obj, user_obj):
    """
        Displays the menu options included in the habit tracker app and prompts the user for their choice.
        Depending on the user's input, the function calls other methods in the habit_obj and user_obj objects
        to perform various actions within the program related to habits tracking.

        Parameters:
        -----------
            - username (str): A string representing the username of the current user.
            - habit_obj: An object representing the Habit class that contains methods related to managing habits.
            - user_obj: An object representing the User class that contains methods related to managing user profiles.

        Return:
        -------
            - None
    """
    print("\n" * 2)
    choice = input("Select an option (1-8):\n1. Choose predefined habits\n2. Create a new habit\n3. "
                   "Mark a habit as completed\n4. Adjust habits\n5. Habit list overview\n6. Habit performance statistics\n7. "
                   "User profile\n8. Quit and log out")
    conn = sqlite3.connect('habit_tracker_db.db')

    # In Option 1, from the list of 7 predefined habits, the user can choose a habit or many as he likes.
    if choice == "1":
        print("\n" * 1)
        user_obj.choose_predefined_habits()
        menu(username, habit_obj, user_obj)

    # In Option 2, the user can create a new habit on his own.
    elif choice == "2":
        print("\n" * 1)
        user_obj.create_habit()
        menu(username, habit_obj, user_obj)

    # In Option 3, the user can mark the habits completed.
    elif choice == "3":
        print("\n" * 1)
        user_obj.complete_habit()
        menu(username, habit_obj, user_obj)

    # In Option 4, there are 4 sub-options.
    elif choice == "4":
        print("\n" * 2)
        adjust_choice = input("Select an option (1-4):\n1. Change habit type\n2. Change habit frequency\n3. "
                              "Delete habit\n4. Go back to main menu")
        # In sub-option 1, the user can change the habits' types.
        if adjust_choice == "1":
            print("\n" * 1)
            user_obj.change_habit_type()
            menu(username, habit_obj, user_obj)
        # In sub-option 2, the user can change the habits' frequencies.
        elif adjust_choice == "2":
            print("\n" * 1)
            user_obj.change_habit_frequency()
            menu(username, habit_obj, user_obj)
        # In sub-option 3, the user can delete the habits.
        elif adjust_choice == "3":
            print("\n" * 1)
            user_obj.delete_habit()
            menu(username, habit_obj, user_obj)
        # In sub-option 4, the user will be taken back to menu page.
        elif adjust_choice == "4":
            print("\n" * 1)
            menu(username, habit_obj, user_obj)

    # In Option 5, there are 4 sub-options.
    elif choice == "5":
        print("\n" * 2)
        habit_list_choice = input("Select an option (1-4):\n1. All habits list\n2. All daily habits list\n3. "
                                  "All weekly habits list\n4. Go back to main menu")
        username = user_obj.username
        # In sub-option 1, the user can see all habits existed in his account.
        if habit_list_choice == "1":
            print("\n" * 1)
            analytics.show_all_habits(username)
            menu(username, habit_obj, user_obj)
        # In sub-option 2, the user can see all daily habits existed in his account.
        elif habit_list_choice == "2":
            print("\n" * 1)
            analytics.show_daily_habits(username)
            menu(username, habit_obj, user_obj)
        # In sub-option 3, the user can see all weekly habits existed in his account.
        elif habit_list_choice == "3":
            print("\n" * 1)
            analytics.show_weekly_habits(username)
            menu(username, habit_obj, user_obj)
        # In sub-option 4, the user will be taken back to menu page.
        elif habit_list_choice == "4":
            print("\n" * 1)
            menu(username, habit_obj, user_obj)

    # In Option 6, there are 5 sub-options.
    elif choice == "6":
        print("\n" * 2)
        performance_choice = input("Select an option (1-5):\n1. Current streak summary\n2. "
                                   "Current streak of selected habit\n3. Longest streak summary\n4. "
                                   "Longest streak of selected habit\n5. Go back to main menu")
        username = user_obj.username
        # In sub-option 1, the user can see current streak summary of all habits existed in his account.
        if performance_choice == "1":
            print("\n" * 1)
            analytics.current_streak_summary(username)
            menu(username, habit_obj, user_obj)
        # In sub-option 2, the user can see current streak of his selected habit.
        elif performance_choice == "2":
            print("\n" * 1)
            analytics.current_streak_of_selected_habit(username)
            menu(username, habit_obj, user_obj)
        # In sub-option 3, the user can see the longest run streak summary of all habits existed in his account.
        elif performance_choice == "3":
            print("\n" * 1)
            analytics.longest_streak_summary(username)
            menu(username, habit_obj, user_obj)
        # In sub-option 4, the user can see the longest run streak of his selected habit.
        elif performance_choice == "4":
            print("\n" * 1)
            analytics.longest_streak_of_selected_habit(username)
            menu(username, habit_obj, user_obj)
        # In sub-option 5, the user will be taken back to menu page.
        elif performance_choice == "5":
            print("\n" * 1)
            menu(username, habit_obj, user_obj)

    # In Option 7, the user can edit their user account profile.
    elif choice == "7":
        print("\n" * 1)
        user_obj.edit_profile()
        menu(username, habit_obj, user_obj)

    # In Option 3, this will make th user logout from the program and closes all the connections.
    elif choice == "8":
        print("\n" * 1)
        user_obj.logout()
        conn.close()


main()
