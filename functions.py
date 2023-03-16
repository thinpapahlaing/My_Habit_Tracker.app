"""
This module provides a class for representing user profiles in a habit tracking application and habit functions to use the app.
It imports hashlib, re, sqlite3, getpass, datetime, questionary, and predefined_habits_list from Habit module.
"""
import hashlib
import re
import sqlite3
import questionary

from datetime import datetime
from Habit import predefined_habits_list


class UserProfile:
    """
    Creating a class representing a user profile for a habit tracking application.

    Attributes:
    -----------
        - forename (str): The user's forename.
        - surname (str): The user's surname.
        - username (str): The user's entered username.
        - password (str): The user's entered password.
    """

    def __init__(self, forename, surname, username, password):
        """
        Initializes a UserProfile object with the given forename, surname, username, and password.

        Args:
        -----
            - forename (str): The user's forename.
            - surname (str): The user's surname.
            - username (str): The user's entered username.
            - password (str): The user's entered password.
        """
        self.forename = forename
        self.surname = surname
        self.username = username
        self.password = password

        # Connect to the database
        self.conn = sqlite3.connect('habit_tracker_db.db')

        # Create a cursor for executing SQL commands
        self.cur = self.conn.cursor()

    def register(self):
        """
            Creates an account for the user by taking their forename, surname, and username.

            Validates the username's availability and checks the password strength by validating the minimum criteria.
            The required criteria for passwords is at least 8 characters long, to contain upper and lower case letters,
            a minimum of one number and one special character.
            The password is hashed and stored in the User table of the database.

            Prints a success message and redirects to the login after successful registration.
        """

        print("\nLet's create your account!")

        # Create a user account
        forename = input("Enter your forename: ")
        surname = input("Enter your surname: ")
        username = input("Enter your username: ")
        self.cur.execute("SELECT username FROM User WHERE username=?", (username,))
        username_exists = self.cur.fetchone()

        # Check whether the entered username already existed
        if username_exists:
            print("This username already exists. :("
                  "\nPlease retry with a different username.")
            self.register()
        else:

            # Check whether the entered password fulfill the minimum criteria
            def password_is_valid(p):
                if len(p) < 8:
                    return "Your password must be at least 8 characters long."
                if not re.search(r'[A-Z]', p):
                    return "Your password must contain at least one uppercase letter."
                if not re.search(r'[a-z]', p):
                    return "Your password must contain at least one lowercase letter."
                if not re.search(r'\d', p):
                    return "Your password must contain at least one number."
                if not re.search(r'[^A-Za-z0-9]', p):
                    return "Your password must contain at least one special character."
                return True

            password = questionary.password("Enter your password: ", validate=password_is_valid).ask()

            # Hash the entered password
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            # Store user information in User table in the database
            self.cur.execute("INSERT INTO User (forename, surname, username, password) VALUES (?, ?, ?, ?)",
                             (forename, surname, username, hashed_password))
            self.conn.commit()
            print("Your account has been created. You can now login :)")
            print("\n" * 3)
            self.login()

    def login(self):
        """
            Logs in the user by taking their username and password and validating it against the User table of the database.
            If the credentials are correct, a success message is printed and the user is redirected to the main menu.
            If the credentials are incorrect, the function is recursively called and user is prompted to enter their credentials again.
        """

        # Process Login
        username = input("Enter your username: ")
        password = questionary.password("Enter your password: ").ask()
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        self.cur.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, hashed_password))

        # Check whether the entered user credentials correct
        if self.cur.fetchone():
            print("\nLogin successful")
            self.username = username
            self.reset_daily_streak()
            self.reset_weekly_streak()
        else:
            print("Username or password is incorrect :(")
            self.login()

    def logout(self):
        """
            Commits any pending transactions and closes the connection with the database.
            Prints a logout message.
        """
        self.conn.commit()
        self.conn.close()
        print("\nLogout successful"
              "\nIt was so great to have you here. See you soon and Wishing all the best for your health!")

    def edit_profile(self):
        """
            Edit the profile of the current user.

            This function allows the user to select which part of their profile they want to edit
            including forename, surname, username and password, and then prompts them to enter the new value.
            The chosen field is then updated in the database.
        """
        sector = questionary.select("Which sector do you want to edit?", choices=[
            "(1) Forename",
            "(2) Surname",
            "(3) Username",
            "(4) Password"
        ]).ask()

        if sector == "(1) Forename":
            changed_forename = questionary.text("Type your new forename: ").ask()
            self.cur.execute("UPDATE User SET forename=? WHERE username=?", (changed_forename, self.username))
            self.conn.commit()
            print(f"\nYour new forename, '{changed_forename},' was successfully updated!\n")
        elif sector == "(2) Surname":
            changed_surname = questionary.text("Type your new surname: ").ask()
            self.cur.execute("UPDATE User SET surname=? WHERE username=?", (changed_surname, self.username))
            self.conn.commit()
            print(f"\nYour new surname, '{changed_surname},' was successfully updated!\n")
        elif sector == "(3) Username":
            changed_username = questionary.text("Type your new username: ").ask()
            self.cur.execute("SELECT username from User WHERE username=?", (changed_username,))
            username_exists = self.cur.fetchone()
            # Check whether the username already exists
            if username_exists:
                print("This username already exists. Please retry with a different username.")
            else:
                self.cur.execute("UPDATE User SET username=? WHERE username=?", (changed_username, self.username))
                self.conn.commit()
                self.cur.execute("UPDATE HabitsData SET habit_creator=? WHERE habit_creator=?",
                                 (changed_username, self.username))
                self.conn.commit()
                self.cur.execute("UPDATE StreaksData SET habit_creator=? WHERE habit_creator=?",
                                 (changed_username, self.username))
                self.conn.commit()
                self.username = changed_username
                print(f"\nYour new username, '{changed_username},' was successfully updated!\n")
        elif sector == "(4) Password":
            def password_is_valid(p):
                if len(p) < 8:
                    return "Your password must be at least 8 characters long."
                if not re.search(r'[A-Z]', p):
                    return "Your password must contain at least one uppercase letter."
                if not re.search(r'[a-z]', p):
                    return "Your password must contain at least one lowercase letter."
                if not re.search(r'\d', p):
                    return "Your password must contain at least one number."
                if not re.search(r'[^A-Za-z0-9]', p):
                    return "Your password must contain at least one special character."
                return True

            changed_password = questionary.password("Type your new password: ", validate=password_is_valid).ask()

            # The newly updated password is hashed again and stored in the database.
            hashed_password = hashlib.sha256(changed_password.encode('utf-8')).hexdigest()
            self.cur.execute("UPDATE User SET password = ? WHERE username=?", (hashed_password, self.username))
            self.conn.commit()
            print(f"\nYour new password was successfully updated!\n")

    def choose_predefined_habits(self):
        """
            Shows a list of predefined habits to the user in a visual way and prompts the user to select one or more habits.
            The selected habits are stored into the database.
        """
        print("\n The followings are the predefined habits list with already defined frequency and type.")
        # Show the predefined habits to the user
        for selected_habit, habit in enumerate(predefined_habits_list):
            habit_name, habit_type, habit_frequency = habit
            habit_string = f"{habit_name} ~~~ {habit_frequency} ~~~ {habit_type}"
            print(f"{selected_habit}: {habit_string}")

        # Prompt the user to select one or more habits by index number
        while True:
            try:
                index = int(input("Select a habit by index number (enter -1 to finish): "))
                if index == -1:
                    break
                elif index < 0 or index >= len(predefined_habits_list):
                    raise ValueError("Invalid index number")
                selected_habit = predefined_habits_list[index]
                # Get the habit name from the user's selection
                habit_name = selected_habit[0].strip()
                habit_type = selected_habit[1].strip()
                habit_frequency = selected_habit[2].strip()
                created_datetime = datetime.now().replace(microsecond=0)
                last_completion_date = None
                habit_streak = 0

                # Insert the selected habit into the database
                self.cur.execute(
                    "INSERT INTO HabitsData (habit_name,habit_creator,habit_type,habit_frequency,created_datetime, "
                    "last_completion_date, habit_streak) VALUES (?,?,?,?,?,?,?)",
                    (habit_name, self.username, habit_type, habit_frequency, created_datetime, last_completion_date,
                     habit_streak))
                self.conn.commit()
                print(f"\n{habit_name} was successfully added to your habits!\n")
            except ValueError as e:
                print(f"Error: {e}")

    def create_habit(self):
        """
            Prompt the user to create a new habit and add it to the HabitsData table in the database.

            This method prompts the user to enter a habit name, type, and frequency using questionary. It then adds the new
            habit to the HabitsData table in the database, along with the habit creator's username, the creation datetime, and
            initial values of last_completion_date and habit_streak.

            If a habit with the same name and frequency already exists for the user, this method will print an error message
            and prompt the user to try again.
        """

        # Prompt the user to enter a new habit name, type, and frequency using questionary
        habit_name = input("Which habit do you want to create? ").strip()
        habit_type = questionary.select("Select habit type:",
                                        choices=["Physical Health", "Emotional Relaxation", "Personal Growth",
                                                 "Relationships", ]).ask()
        habit_frequency = questionary.select("Select habit frequency:",
                                             choices=["Daily", "Weekly"]).ask()

        # Get the current datetime, and initialize the habit_streak and last_completion_date values
        created_datetime = datetime.now().replace(microsecond=0)
        habit_streak = 0
        last_completion_date = None

        # Check if a habit with the same name and frequency already exists for the user
        self.cur.execute(
            "SELECT COUNT(*) FROM HabitsData WHERE habit_name = ? AND habit_creator= ? And habit_frequency= ?",
            (habit_name, self.username, habit_frequency))
        habit_count = self.cur.fetchone()[0]
        if habit_count > 0:
            # If a habit with the same name and frequency already exists, print an error message and prompt the user to try again
            print("This habit already exists. Try again!")
        else:
            # Insert the new habit into the HabitsData table in the database
            self.cur.execute(
                "INSERT INTO HabitsData(habit_name, habit_creator, habit_type, habit_frequency, created_datetime, "
                "last_completion_date, habit_streak) VALUES(?, ?, ?, ?, ?, ?, ?)",
                (habit_name, self.username, habit_type, habit_frequency, created_datetime, last_completion_date,
                 habit_streak))
            self.conn.commit()
            print(f"Success! A new habit {habit_name} was added to the list:)")

    def is_habit_completed_before(self, habit_name, username):
        """
            Checks if a habit has been completed before by a user.

            Args:
            -----
                - habit_name (str): the name of the habit to check.
                - username (str): the name of the user who created the habit.

            Returns:
            --------
                - True if the habit has been completed before by the user, False otherwise.
        """
        self.cur.execute("SELECT habit_streak FROM HabitsData WHERE habit_name = ? AND habit_creator = ?",
                         (habit_name, username))
        habit_streak = self.cur.fetchone()
        if habit_streak:
            habit_streak = habit_streak[0]
        else:
            habit_streak = 0
        return habit_streak > 0

    def complete_habit(self):
        """
            Prompts the user to select a habit he has completed from the all habits list
            Updates the habit's streak information in StreaksData table in the database
            Prints a success message

            Use is_habit_completed_before(habit_name, username) to check whether the habit was completed before
            If the habit was completed before,
            last completion date, habit streak, the streak length and streak end date are updated
            based on that habit's frequency: Daily or Weekly.
            Functions for only 1 streak for 1-day priod of all daily habits and only 1 streak for 7-day period of all weekly habits

            Otherwise, a new streak data row is started in StreaksData table and
            a value of current datetime for last completion date is inserted in HabitsData table,
            also habit streak becomes 1 from 0.
        """
        # Get a list of all habits in the user's account
        self.cur.execute("SELECT habit_name, habit_frequency, habit_type FROM HabitsData WHERE habit_creator=?",
                         (self.username,))
        habits_list = self.cur.fetchall()

        # Create a list of choices for the user
        choices = []
        for habit in habits_list:
            habit_name = habit[0]
            habit_frequency = habit[1]
            habit_type = habit[2]
            choices.append(f"{habit_name} ~~~ {habit_frequency} ~~~ {habit_type}")

        if not choices:
            print("You have no habits to complete.")
            return

        # Ask the user to select a habit from the list
        completed_habit_name = questionary.select("Amazing! Which habit did you accomplish? :)", choices).ask()
        selected_habit = completed_habit_name.split("~~~")[0].strip()
        selected_habit_type = completed_habit_name.split("~~~")[2].strip()
        selected_habit_frequency = completed_habit_name.split("~~~")[1].strip()
        habit_completed_before = self.is_habit_completed_before(selected_habit, self.username)

        # Check if the habit has been completed before
        if habit_completed_before:
            if selected_habit_frequency == 'Daily':
                # If the habit is a daily habit, check whether the user is trying to check-off the selected habit on the next day after last completion date
                self.cur.execute(f"SELECT last_completion_date FROM HabitsData WHERE habit_name= ? AND "
                                 f"habit_creator= ?", (selected_habit, self.username))
                last_completion_date = self.cur.fetchone()[0]
                if (datetime.now().replace(microsecond=0) - datetime.strptime(last_completion_date,
                                                                              "%Y-%m-%d %H:%M:%S")).days <= 1 \
                        and (datetime.now().replace(microsecond=0) - datetime.strptime(last_completion_date,
                                                                                       "%Y-%m-%d %H:%M:%S")) \
                        .days > 0:

                    # If the user is trying to check-off the selected habit on the next day after last completion date,
                    # last completion date, habit streak, the streak length and streak end date are updated in database.
                    self.cur.execute(
                        "UPDATE HabitsData SET last_completion_date = ?, habit_streak = habit_streak + 1 "
                        "WHERE habit_name = ? AND habit_creator = ?", [datetime.now().replace(microsecond=0),
                                                                       selected_habit, self.username])
                    self.conn.commit()
                    self.cur.execute(
                        "UPDATE StreaksData SET streak_end_date = NULL, streak_length = streak_length + 1 "
                        "WHERE habit_name = ? AND habit_creator = ? AND habit_type = ? AND habit_frequency = ?",
                        (selected_habit, self.username, selected_habit_type, selected_habit_frequency))
                    self.conn.commit()
                    print(f"Hooray! You completed {selected_habit}.")
                else:
                    # If the user is trying to mark completed the selected daily habit more than once in same day where its last completion date is not 24 hours long from current datetime,
                    # The bottom statement will be printed out as only 1 streak is counted in 1-day period for Daily habits.
                    print("There is no 24 hours long from the last completion date of this daily habit. "
                          "Only 1 streak is counted for Daily habits in 24 hours.")
            if selected_habit_frequency == 'Weekly':
                # If the habit is a weekly habit, check whether the user is trying to check-off the selected habit on 8th day after last completion date
                self.cur.execute(f"SELECT last_completion_date FROM HabitsData WHERE habit_name= ? AND "
                                 f"habit_creator= ?", (selected_habit, self.username))
                last_completion_date = self.cur.fetchone()[0]
                if (datetime.now().replace(microsecond=0) - datetime.strptime(last_completion_date,
                                                                              "%Y-%m-%d %H:%M:%S")).days <= 7 \
                        and (datetime.now().replace(microsecond=0) - datetime.strptime(last_completion_date,
                                                                                       "%Y-%m-%d %H:%M:%S")) \
                        .days > 6:

                    # If the user is trying to check-off the selected habit on 8th day after last completion date,
                    # last completion date, habit streak, the streak length and streak end date are updated in database.
                    self.cur.execute(
                        "UPDATE HabitsData SET last_completion_date = ?, habit_streak = habit_streak + 1 "
                        "WHERE habit_name = ? AND habit_creator = ?",
                        [datetime.now().replace(microsecond=0), selected_habit, self.username])
                    self.conn.commit()
                    self.cur.execute(
                        "UPDATE StreaksData SET streak_end_date = NULL, streak_length = streak_length + 1 "
                        "WHERE habit_name = ? AND habit_creator = ? AND habit_type = ? AND habit_frequency = ?",
                        (selected_habit, self.username, selected_habit_type, selected_habit_frequency))
                    self.conn.commit()
                    print(f"Hooray! You completed {selected_habit}.")
                else:
                     # If the user is trying to mark completed the selected daily habit more than once in same week where its last completion date is not 7 days long from current datetime,
                    # The bottom statement will be printed out as only 1 streak is counted in 7-day period for Weekly habits.
                    print("There is no 7 days long from the last completion date of this weekly habit. "
                          "Only 1 streak is counted for Weekly habits marked completed within 7 days.")
        else:
            # If the habit was not completed before,
            # A new streak data row is started in StreaksData table
            # A value of current datetime for last completion date is inserted in HabitsData table,
            # Also habit streak becomes 1 from 0.
            re_last_completion_date = datetime.now().replace(microsecond=0)
            re_habit_streak = 1
            self.cur.execute(
                "UPDATE HabitsData SET last_completion_date = ?, habit_streak = ? WHERE habit_name = ? "
                "AND habit_creator = ?",
                [re_last_completion_date, re_habit_streak, selected_habit, self.username])
            self.conn.commit()
            self.cur.execute(
                "INSERT INTO StreaksData (habit_name, habit_creator, habit_type, habit_frequency, "
                "streak_start_date, streak_end_date, streak_length) "
                "VALUES (?,?,?,?,?,?,?)", (selected_habit, self.username, selected_habit_type,
                                           selected_habit_frequency, datetime.now().replace(microsecond=0), None, 1))
            self.conn.commit()
            print(f"Hooray! You completed {selected_habit}.")

    def change_habit_type(self):
        """
            Allows the user to change the type of habit.
            Retrieves a list of existed habits in the user account and presents them to the user for selection.
            Asks the user to choose a habit from the list and then to choose a new habit type.
            Updates the selected habit's habit_type field in the HabitsData table and the StreaksData table with the new habit type.
        """

        self.cur.execute(f"SELECT habit_name, habit_type, habit_frequency FROM HabitsData WHERE habit_creator= ?",
                         (self.username,))
        habits_list = self.cur.fetchall()

        # Create a list of choices for the user
        choices = []
        for habit in habits_list:
            habit_name = habit[0]
            habit_frequency = habit[1]
            habit_type = habit[2]
            choices.append(f"{habit_name} ~~~ {habit_frequency} ~~~ {habit_type}")

        if not choices:
            print("You have no habits to change.")
            return

        # Ask the user to select a habit from the list which he wants to change the type
        desired_habit = questionary.select("Which habit do you want to change type?", choices).ask()

        # Get the habit name from the user's selection
        selected_habit = desired_habit.split("~~~")[0].strip()

        # Ask the user to select the new habit type
        habit_type_list = ["Physical Health", "Emotional Relaxation", "Personal Growth", "Relationships"]
        habit_type = questionary.select("Select the new habit type?", habit_type_list).ask()

        # Store the new habit type in the HabitsData table
        self.cur.execute("UPDATE HabitsData SET habit_type= ? WHERE habit_name= ? AND habit_creator= ?;",
                         (habit_type, selected_habit, self.username))
        self.conn.commit()
        self.cur.execute("UPDATE StreaksData SET habit_type= ? WHERE habit_name= ? AND habit_creator= ?;",
                         (habit_type, selected_habit, self.username))
        self.conn.commit()
        print(f"Success! The type of \"{selected_habit}\" has been updated to \"{habit_type}\".")

    def change_habit_frequency(self):
        """
            Allows the user to change the frequency of habit.
            Retrieves a list of existed habits in the user account and presents them to the user for selection.
            Asks the user to choose a habit from the list and then to choose a new habit frequency.
            Updates the selected habit's habit_frequency field in the HabitsData table and the StreaksData table with the new habit frequency.
        """
        self.cur.execute(f"SELECT habit_name, habit_frequency, habit_type FROM HabitsData WHERE habit_creator= ?",
                         (self.username,))
        habits_list = self.cur.fetchall()

        # Create a list of choices for the user
        choices = []
        for habit in habits_list:
            habit_name = habit[0]
            habit_frequency = habit[1]
            habit_type = habit[2]
            choices.append(f"{habit_name} ~~~ {habit_frequency} ~~~ {habit_type}")

        if not choices:
            print("You have no habits to change.")
            return

        # Ask the user to select a habit from the list which he wants to change the frequency
        desired_habit = questionary.select("Which habit do you want to change frequency?", choices).ask()

        # Get the habit name from the user's selection
        selected_habit = desired_habit.split("~~~")[0].strip()

        # Ask the user to select the new habit frequency
        habit_frequency = questionary.text("For which frequency do you want to change? D for Daily, W for Weekly").ask()

        # Convert the user input to full words
        if habit_frequency.upper() == 'D':
            habit_frequency = "Daily"
        elif habit_frequency.upper() == 'W':
            habit_frequency = "Weekly"
        else:
            print("Invalid input, frequency should be either D for Daily or W for Weekly.")
            return

        # Store the new habit frequency in the HabitsData table
        self.cur.execute("UPDATE HabitsData SET habit_frequency= ? WHERE habit_name= ? AND habit_creator= ?;",
                         (habit_frequency, selected_habit, self.username))
        self.conn.commit()
        self.cur.execute("UPDATE StreaksData SET habit_frequency= ? WHERE habit_name= ? AND habit_creator= ?;",
                         (habit_frequency, selected_habit, self.username))
        self.conn.commit()
        print(f"Success! The frequency of \"{selected_habit}\" has been updated to \"{habit_frequency}\".")

    def delete_habit(self):
        """
            Allows the user to delete any habits existed in his account.
            Retrieves a list of existed habits in the user account and presents them to the user for selection.
            Asks the user to choose a habit from the list.
            Delete the selected habit in both HabitsData table and the StreaksData table in the database.
        """
        self.cur.execute(f"SELECT habit_name, habit_frequency, habit_type FROM HabitsData WHERE habit_creator= ?;",
                         (self.username,))
        habits_list = self.cur.fetchall()

        # Create a list of choices for the user
        choices = []
        for habit in habits_list:
            habit_name = habit[0]
            habit_frequency = habit[1]
            habit_type = habit[2]
            choices.append(f"{habit_name} ~~~ {habit_frequency} ~~~ {habit_type}")

        if not choices:
            print("You have no habits to delete.")
            return

        # Ask the user to select a habit from the list which he wants to delete
        desired_habit = questionary.select("Which habit do you want to delete?", choices).ask()

        # Get the habit name from the user's selection
        selected_habit = desired_habit.split("~~~")[0].strip()
        selected_habit_frequency = desired_habit.split("~~~")[1].strip()
        selected_habit_type = desired_habit.split("~~~")[2].strip()

        # Delete the habit from the HabitsData table
        self.cur.execute(
            "DELETE FROM HabitsData WHERE habit_name = ? AND habit_creator = ? AND habit_type = ? AND habit_frequency = ?",
            (selected_habit, self.username, selected_habit_type, selected_habit_frequency))
        self.conn.commit()
        self.cur.execute(
            "DELETE FROM StreaksData WHERE habit_name = ? AND habit_creator = ? AND habit_type = ? AND habit_frequency = ?",
            (selected_habit, self.username, selected_habit_type, selected_habit_frequency))
        self.conn.commit()
        print("Success! Habit, {} has been deleted.".format(selected_habit))

    def is_last_completion_date_present(self, habit_name, username):
        """
            Check if the last completion date is present for a given habit.

            Args:
            -----
                - habit_name (str): The name of the habit for which the last completion date needs to be checked.
                - username (str): The name of the user who created the habit.

            Returns:
            --------
                - last_completion_date (str or None): The last completion date of the habit, if present, else None.
        """
        self.cur.execute("SELECT last_completion_date FROM HabitsData WHERE habit_name = ? AND habit_creator = ?",
                         (habit_name, username))
        last_completion_date = self.cur.fetchone()[0]
        if last_completion_date:
            last_completion_date = last_completion_date[0]
        else:
            last_completion_date = None
        return last_completion_date

    def reset_daily_streak(self):
        """
            Auto-Reset the streak of daily habits if the user miss to check-off a daily habit on the next day after last completion date

            First by using is_last_completion_date_present(habit_name, username) function to check
            whether a habit already starts making streaks and has last completion date

            If there is already last completion date,
                For each habit that has a daily frequency and was missed to check-off on the next day after last completion date,
                This function resets the habit streak in HabitsData table to 0,
                Resets the last completion date of that habit in HabitsData table to None
                Updates the streak end date to current datetime and streak length in the StreaksData table.
        """
        # Get a list of all daily habits in the user's account
        self.cur.execute(
            "SELECT habit_name, habit_type, last_completion_date, habit_streak FROM HabitsData "
            "WHERE habit_creator= ? AND habit_frequency = 'Daily'", (self.username,))
        habits_list = self.cur.fetchall()
        for habit in habits_list:
            habit_name = habit[0]
            habit_type = habit[1]
            last_completion_date = habit[2]
            habit_streak = habit[3]

            # Checks whether the habits existed in the user account already has last completion date
            past_completion_date = self.is_last_completion_date_present(habit_name, self.username)

            if past_completion_date:
                # If there are last completion dates,
                # Checks whether there is check-off on the next day after last completion date
                # If the user miss to check-off,
                # Resets habit streak and last completion date in HabitsData table
                # Updates streak end date and streak length in StreaksData table
                if (datetime.now().replace(microsecond=0) - datetime.strptime(last_completion_date,
                                                                              "%Y-%m-%d %H:%M:%S")).days > 1:
                    streak_length = habit_streak
                    self.cur.execute(
                        "UPDATE StreaksData SET streak_end_date = ?, streak_length = ? WHERE habit_name = ? "
                        "AND habit_type = ? AND habit_creator = ?",
                        (datetime.now().replace(microsecond=0), streak_length, habit_name, habit_type, self.username))
                    self.conn.commit()
                    re_habit_streak = 0
                    self.cur.execute(
                        "UPDATE HabitsData SET last_completion_date = ? , habit_streak = ? WHERE habit_name = ?"
                        "AND habit_type = ? AND habit_creator = ?",
                        (None, re_habit_streak, habit_name, habit_type, self.username))
                    self.conn.commit()
                    print(f"The streaks of {habit_name} have been auto-reset to 0 "
                          f"since there is no marking completed during last 24 hours.")
                    print("\n" * 1)

    def reset_weekly_streak(self):
        """
            Auto-Reset the streak of weekly habits if the user miss to check-off a weekly habit on 8th day after last completion date

            First by using is_last_completion_date_present(habit_name, username) function to check
            whether a habit already starts making streaks and has last completion date

            If there is already last completion date,
                For each habit that has a weekly frequency and was missed to check-off on 8th day after last completion date,
                This function resets the habit streak in HabitsData table to 0,
                Resets the last completion date of that habit in HabitsData table to None
                Updates the streak end date to current datetime and streak length in the StreaksData table.
        """
        # Get a list of all weekly habits in the user's account
        self.cur.execute(
            "SELECT habit_name, habit_type, last_completion_date, habit_streak FROM HabitsData "
            "WHERE habit_creator= ? AND habit_frequency = 'Weekly'", (self.username,))
        habits_list = self.cur.fetchall()
        for habit in habits_list:
            habit_name = habit[0]
            habit_type = habit[1]
            last_completion_date = habit[2]
            habit_streak = habit[3]

            # Checks whether the habits existed in the user account already has last completion date
            past_completion_date = self.is_last_completion_date_present(habit_name, self.username)

            if past_completion_date:
                # If there are last completion dates,
                # Checks whether there is check-off on 8th day after last completion date
                # If the user miss to check-off,
                # Resets habit streak and last completion date in HabitsData table
                # Updates streak end date and streak length in StreaksData table
                if (datetime.now().replace(microsecond=0) - datetime.strptime(last_completion_date,
                                                                              "%Y-%m-%d %H:%M:%S")).days > 7:
                    streak_length = habit_streak
                    self.cur.execute(
                        "UPDATE StreaksData SET streak_end_date = ?, streak_length = ? WHERE habit_name = ? "
                        "AND habit_type = ? AND habit_creator = ?",
                        (datetime.now().replace(microsecond=0), streak_length, habit_name, habit_type, self.username))
                    self.conn.commit()
                    re_habit_streak = 0
                    self.cur.execute(
                        "UPDATE HabitsData SET last_completion_date = ? , habit_streak = ? WHERE habit_name = ?"
                        "AND habit_type = ? AND habit_creator = ?",
                        (None, re_habit_streak, habit_name, habit_type, self.username))
                    self.conn.commit()
                    print(f"The streaks of {habit_name} have been auto-reset to 0 "
                          f"since there is no marking completed during last 7 days.")
                    print("\n" * 1)
