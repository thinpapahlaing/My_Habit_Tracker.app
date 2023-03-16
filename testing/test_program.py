"""
This module contains an unittest.TestCase class for testing 15 functions of the whole habit tracker app.
It imports several libraries and necessary modules.
"""

import io
import sys
import sqlite3
import unittest
import analytics
from io import StringIO
from contextlib import redirect_stdout
from datetime import datetime
from unittest import mock
from unittest.mock import patch
from freezegun import freeze_time
from functions import UserProfile


class TestHabitTracker(unittest.TestCase):
    """
        This class defines unit tests for the HabitTracker program.
        It inherits from the unittest.TestCase class and contains 15 test methods.
    """

    def setUp(self):
        """
            This method sets up a StringIO object to capture standard output and redirects sys.stdout to this object.
        """
        self.output = io.StringIO()
        sys.stdout = self.output

    def test_choose_predefined_habits(self):
        """
            This method defines a unit test for the choose_predefined_habits() function of the UserProfile class. It
            mocks the input function to simulate user input and checks that the selected habit is correctly inserted
            into the database and that the correct message is displayed to the user.
        """

        with patch('builtins.input', side_effect=[6, -1]):
            # Define the references which are expected to get result like these
            habit_name = "Cleaning House"
            username = "username1"
            habit_type = "Emotional Relaxation"
            habit_frequency = "Weekly"
            created_datetime = datetime.now().replace(microsecond=0)
            string_created_datetime = datetime.strftime(created_datetime, "%Y-%m-%d %H:%M:%S")
            last_completion_date = None
            habit_streak = 0

            with sqlite3.connect("habit_tracker_db.db") as conn:
                user = UserProfile("Tom", "Ford", "username1",
                                   "d8b2d6602b97dfe655ccb90f8292c4508708211fd2cf38015ac2e53189add9f1")
                # Call the choose_predefined_habits() function with the 'conn' argument
                user.choose_predefined_habits()

                # Verify that the selected habit is inserted into the database
                cur = conn.cursor()
                cur.execute("SELECT * FROM HabitsData WHERE habit_name = ? and habit_creator = ? "
                            "and habit_type = ? and habit_frequency = ? and created_datetime = ? "
                            "and last_completion_date = ? and habit_streak = ?",
                            (habit_name, username, habit_type, habit_frequency, string_created_datetime,
                             last_completion_date, habit_streak))
                result = cur.fetchall()
                if result:
                    self.assertEqual(result[0][0], habit_name)
                    self.assertEqual(result[0][1], username)
                    self.assertEqual(result[0][2], habit_type)
                    self.assertEqual(result[0][3], habit_frequency)
                    self.assertEqual(result[0][4], string_created_datetime)
                    self.assertEqual(result[0][5], last_completion_date)
                    self.assertEqual(result[0][6], habit_streak)

                # Verify that the correct message is displayed after the selected habits are inserted
                expected_output = f"\n{habit_name} was successfully added to your habits!\n"
                self.assertIn(expected_output, self.output.getvalue())

                # Clear data changes that were processed while running the test
                cur.execute("DELETE FROM HabitsData WHERE habit_name = ? and habit_creator = ? ",
                            (habit_name, username))
                conn.commit()

    def test_create_habit(self):
        """
            This method defines a unit test for the create_habit() function of the UserProfile class. It mocks the input
            and questionary.select functions to simulate user input and checks that the created habit is correctly inserted
            into the database and that the correct message is displayed to the user.
        """

        with mock.patch('builtins.input', side_effect=["Resting"]):
            with mock.patch("functions.questionary.select") as mock_select:
                mock_select.return_value = mock.MagicMock(ask=mock.Mock(side_effect=["Physical Health", "Daily"]))
                # Define the references which are expected to get result like these
                habit_name = "Resting"
                username = "username2"
                habit_type = "Physical Health"
                habit_frequency = "Daily"
                created_datetime = datetime.now().replace(microsecond=0)
                string_created_datetime = datetime.strftime(created_datetime, "%Y-%m-%d %H:%M:%S")
                last_completion_date = None
                habit_streak = 0

                with sqlite3.connect("habit_tracker_db.db") as conn:
                    user = UserProfile("Daisy", "Luna", "username2",
                                       "6b6b681e6617c2d34d5bc96d5bdc23020b5a81e88f150d89968d96750227bf7a")
                    # Call the create_habit() function with the 'conn' argument
                    user.create_habit()

                    # Verify that the selected habit is inserted into the database
                    cur = conn.cursor()
                    cur.execute(
                        "SELECT * FROM HabitsData WHERE habit_name = ? and habit_creator = ? and habit_type = ? "
                        "and habit_frequency = ? and created_datetime = ? and last_completion_date is ? and "
                        "habit_streak = ?", (habit_name, username, habit_type, habit_frequency, created_datetime,
                                             string_created_datetime, habit_streak))
                    result = cur.fetchall()
                    if result:
                        self.assertEqual(result[0][0], habit_name)
                        self.assertEqual(result[0][1], username)
                        self.assertEqual(result[0][2], habit_type)
                        self.assertEqual(result[0][3], habit_frequency)
                        self.assertEqual(result[0][4], string_created_datetime)
                        self.assertEqual(result[0][5], last_completion_date)
                        self.assertEqual(result[0][6], habit_streak)

                    # Verify that the correct message is displayed after the selected habits are inserted
                    expected_output = "Success! A new habit Resting was added to the list:)"
                    self.assertIn(expected_output, self.output.getvalue())

                    # Clear data changes that were processed while running the test
                    cur.execute("DELETE FROM HabitsData WHERE habit_name = ? and habit_creator = ?",
                                (habit_name, username))
                    conn.commit()

    def test_complete_habit_uncompleted_before(self):
        """
            This function tests the complete_habit() method of the UserProfile class where that mock chosen habit has not been completed before.
            It uses mock objects to simulate user input and database calls, and checks that the database has been
            updated correctly and the expected output message has been printed.
        """
        with mock.patch("functions.questionary.select") as mock_select:
            mock_select.return_value = mock.MagicMock(ask=mock.Mock(
                side_effect=["Meditation ~~~ Daily ~~~ Emotional Relaxation"]))
            with mock.patch("functions.UserProfile.is_habit_completed_before", return_value=False):
                # Define the references which are expected to get result like these
                habit_name = "Meditation"
                username = "username1"
                habit_type = "Emotional Relaxation"
                habit_frequency = "Daily"
                created_datetime = '2023-01-30 00:00:00'
                last_completion_date = datetime.now().replace(microsecond=0)
                string_last_completion_date = datetime.strftime(last_completion_date, "%Y-%m-%d %H:%M:%S")
                habit_streak = 1
                streak_start_date = datetime.now().replace(microsecond=0)
                string_streak_start_date = datetime.strftime(streak_start_date, "%Y-%m-%d %H:%M:%S")
                streak_end_date = None
                streak_length = 1
                with sqlite3.connect("habit_tracker_db.db") as conn:
                    user = UserProfile("Tom", "Ford", "username1",
                                       "d8b2d6602b97dfe655ccb90f8292c4508708211fd2cf38015ac2e53189add9f1")
                    # Call the complete_habit() function with the 'conn' argument
                    user.complete_habit()

                    # Verify that the selected habit is updated properly at HabitsData table in the database
                    cur = conn.cursor()
                    cur.execute(
                        "SELECT * FROM HabitsData WHERE habit_name = ? AND habit_creator = ? AND habit_type = ? "
                        "AND habit_frequency = ? AND created_datetime = ? ",
                        [habit_name, username, habit_type, habit_frequency, created_datetime])
                    result = cur.fetchall()
                    if result:
                        self.assertEqual(result[0][0], habit_name)
                        self.assertEqual(result[0][1], username)
                        self.assertEqual(result[0][2], habit_type)
                        self.assertEqual(result[0][3], habit_frequency)
                        self.assertEqual(result[0][4], created_datetime)
                        self.assertEqual(result[0][5], string_last_completion_date)
                        self.assertEqual(result[0][6], habit_streak)

                    # Verify that the selected habit is updated properly at StreaksData table in the database
                    cur.execute(
                        "SELECT * FROM StreaksData WHERE habit_name = ? and habit_creator = ? and habit_type = ? "
                        "and habit_frequency = ? and streak_start_date = ? and streak_end_date = ? and "
                        "streak_length = ?", (habit_name, username, habit_type, habit_frequency, streak_start_date,
                                              streak_start_date, streak_length))
                    result = cur.fetchall()
                    if result:
                        self.assertEqual(result[0][0], habit_name)
                        self.assertEqual(result[0][1], username)
                        self.assertEqual(result[0][2], habit_type)
                        self.assertEqual(result[0][3], habit_frequency)
                        self.assertEqual(result[0][4], string_streak_start_date)
                        self.assertEqual(result[0][5], streak_end_date)
                        self.assertEqual(result[0][6], streak_length)

                    # Verify that the correct message is displayed
                    expected_output = "Hooray! You completed Meditation."
                    self.assertIn(expected_output, self.output.getvalue())

                    # Clear data changes that were processed while running the test
                    cur.execute("UPDATE HabitsData SET last_completion_date = ?, habit_streak = 0 "
                                "WHERE habit_name = ? AND habit_creator = ? AND habit_type = ? "
                                "AND habit_frequency = ? AND created_datetime = ?",
                                (None, habit_name, username, habit_type, habit_frequency, created_datetime))
                    conn.commit()
                    cur.execute("DELETE FROM StreaksData WHERE habit_name = ? and habit_creator = ?",
                                (habit_name, username))
                    conn.commit()

    @freeze_time('2023-01-31 00:10:00')
    def test_complete_habit_completed_before_option1(self):
        """
            This function tests the complete_habit() method of the UserProfile class where that mock chosen habit has been completed before.
            It uses mock objects to simulate user input and database calls, and checks that the database has been
            updated correctly and the expected output message has been printed.

            The test case uses the `@freeze_time` decorator to freeze the time to a specific date and time.
        """
        with mock.patch("functions.questionary.select") as mock_select:
            mock_select.return_value = mock.MagicMock(ask=mock.Mock(
                side_effect=["Exercise ~~~ Daily ~~~ Physical Health"]))
            with mock.patch("functions.UserProfile.is_habit_completed_before", return_value=True):
                # Define the references which are expected to get result like these
                habit_name = "Exercise"
                username = "username2"
                habit_type = "Physical Health"
                habit_frequency = "Daily"
                created_datetime = '2023-01-02 00:00:00'
                habit_streak = 30
                last_completion_date = datetime.now().replace(microsecond=0)
                string_last_completion_date = datetime.strftime(last_completion_date, "%Y-%m-%d %H:%M:%S")
                streak_start_date = '2023-01-02 00:05:00'
                streak_end_date = None
                streak_length = 30
                with sqlite3.connect("habit_tracker_db.db") as conn:
                    user = UserProfile("Daisy", "Luna", "username2",
                                       "6b6b681e6617c2d34d5bc96d5bdc23020b5a81e88f150d89968d96750227bf7a")
                    # Call the complete_habit() function with the 'conn' argument
                    user.complete_habit()

                    # Verify that the selected habit is updated properly at HabitsData table in the database
                    cur = conn.cursor()
                    cur.execute(
                        "SELECT * FROM HabitsData WHERE habit_name = ? AND habit_creator = ? AND habit_type = ? "
                        "AND habit_frequency = ? AND created_datetime = ? ",
                        [habit_name, username, habit_type, habit_frequency, created_datetime])
                    result = cur.fetchall()
                    if result:
                        self.assertEqual(result[0][0], habit_name)
                        self.assertEqual(result[0][1], username)
                        self.assertEqual(result[0][2], habit_type)
                        self.assertEqual(result[0][3], habit_frequency)
                        self.assertEqual(result[0][4], created_datetime)
                        self.assertEqual(result[0][5], string_last_completion_date)
                        self.assertEqual(result[0][6], habit_streak)

                    # Verify that the selected habit is updated properly at StreaksData table in the database
                    cur.execute(
                        "SELECT * FROM StreaksData WHERE habit_name = ? and habit_creator = ? and habit_type = ? "
                        "and habit_frequency = ? and streak_start_date = ? and streak_end_date = ? and "
                        "streak_length = ?", (habit_name, username, habit_type, habit_frequency, streak_start_date,
                                              streak_start_date, streak_length))
                    result = cur.fetchall()
                    if result:
                        self.assertEqual(result[0][0], habit_name)
                        self.assertEqual(result[0][1], username)
                        self.assertEqual(result[0][2], habit_type)
                        self.assertEqual(result[0][3], habit_frequency)
                        self.assertEqual(result[0][4], streak_start_date)
                        self.assertEqual(result[0][5], streak_end_date)
                        self.assertEqual(result[0][6], streak_length)

                    # Verify that the correct message is displayed
                    expected_output = "Hooray! You completed Exercise."
                    self.assertIn(expected_output, self.output.getvalue())

                    # Clear data changes that were processed while running the test
                    cur.execute(
                        "UPDATE HabitsData SET last_completion_date = ?, habit_streak = 29 WHERE habit_name = ? "
                        "and habit_creator = ? ",
                        ['2023-01-30 00:05:00', habit_name, username])
                    conn.commit()
                    cur.execute("UPDATE StreaksData SET streak_end_date = ?, streak_length = 29 "
                                "WHERE habit_name = ? and habit_creator = ?",
                                (None, habit_name, username))
                    conn.commit()

    @freeze_time('2023-01-30 12:00:00')
    def test_complete_habit_completed_before_option2(self):
        """
            This function tests the complete_habit() method of the UserProfile class
            where the mock chosen habit will be mark completed on the same day as its last completion date.

            It uses mock objects to simulate user input and database calls, and checks that the expected output message has been printed.
            The test case uses the `@freeze_time` decorator to freeze the time to a specific date and time.
        """

        with mock.patch("functions.questionary.select") as mock_select:
            mock_select.return_value = mock.MagicMock(ask=mock.Mock(
                side_effect=["Exercise ~~~ Daily ~~~ Physical Health"]))
            with mock.patch("functions.UserProfile.is_habit_completed_before", return_value=True):
                with sqlite3.connect("habit_tracker_db.db"):
                    user = UserProfile("Daisy", "Luna", "username2",
                                       "6b6b681e6617c2d34d5bc96d5bdc23020b5a81e88f150d89968d96750227bf7a")
                    # Call the complete_habit() function with the 'conn' argument
                    user.complete_habit()

                    # Verify that the correct message is displayed
                    expected_output = "There is no 24 hours long from the last completion date of this daily habit. " \
                                      "Only 1 streak is counted for Daily habits in 24 hours."
                    self.assertIn(expected_output, self.output.getvalue())

    def test_delete_habit(self):
        """
            This method defines a unit test for the delete_habit() function of the UserProfile class. It mocks the input
            and questionary.select functions to simulate user input and checks that the mock selected habit is correctly deleted
            at the database and that the correct message is displayed to the user.
        """

        with mock.patch("functions.questionary.select") as mock_select:
            mock_select.return_value = mock.MagicMock(ask=mock.Mock(
                side_effect=["Self-assessment ~~~ Weekly ~~~ Personal Growth"]))
            # Define the references which are expected to get result like these
            habit_name = "Self-assessment"
            username = "username1"
            habit_type = "Personal Growth"
            habit_frequency = "Weekly"
            habit_streak = 5
            streak_end_date = None
            streak_length = 5
            with sqlite3.connect("habit_tracker_db.db") as conn:
                user = UserProfile("Tom", "Ford", "username1",
                                   "d8b2d6602b97dfe655ccb90f8292c4508708211fd2cf38015ac2e53189add9f1")
                # Call the delete_habit() function with the 'conn' argument
                user.delete_habit()

                # Verify that the selected habit is deleted properly at HabitsData table in the database
                cur = conn.cursor()
                cur.execute(
                    "SELECT * FROM HabitsData WHERE habit_name = ? AND habit_creator = ? AND habit_type = ? "
                    "AND habit_frequency = ?",
                    (habit_name, username, habit_type, habit_frequency))
                result = cur.fetchall()
                self.assertFalse(result)

                # Verify that the selected habit is deleted properly at StreaksData table in the database
                cur.execute(
                    "SELECT * FROM StreaksData WHERE habit_name = ? AND habit_creator = ? AND habit_type = ? "
                    "AND habit_frequency = ?",
                    (habit_name, username, habit_type, habit_frequency))
                result = cur.fetchall()
                self.assertFalse(result)

                # Verify that the correct message is displayed
                expected_output = "Success! Habit, Self-assessment has been deleted."
                self.assertIn(expected_output, self.output.getvalue())

                # Clear data changes that were processed while running the test
                cur.execute("INSERT INTO HabitsData (habit_name, habit_creator, habit_type, habit_frequency, "
                            "created_datetime, last_completion_date, habit_streak) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (habit_name, username, habit_type, habit_frequency, '2023-01-01 00:00:00',
                             '2023-01-31 00:05:00', habit_streak))
                conn.commit()
                cur.execute("INSERT INTO StreaksData (habit_name, habit_creator, habit_type, habit_frequency, "
                            "streak_start_date, streak_end_date, streak_length) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (habit_name, username, habit_type, habit_frequency, '2023-01-01 00:05:00', streak_end_date,
                             streak_length))
                conn.commit()

    @freeze_time('2023-01-29 00:10:00')
    def test_reset_daily_streak(self):
        """
            This method defines a unit test for the reset_daily_streak() function of the UserProfile class.
            It mocks the output of is_last_completion_date_present to True and checks that the mock selected daily habit is correctly made reset the streaks
            at the database and checks that the expected output message has been printed.
            The test case uses the `@freeze_time` decorator to freeze the time to a specific date and time.
        """

        with mock.patch("functions.UserProfile.is_last_completion_date_present", return_value=True):
            # Define the references which are expected to get result like these
            habit_name = "Writing Diary"
            username = "username2"
            habit_type = "Personal Growth"
            habit_frequency = "Daily"
            created_datetime = '2023-01-01 00:00:00'
            last_completion_date = None
            habit_streak = 0
            streak_start_date = '2023-01-01 00:05:00'
            streak_end_date = datetime.now().replace(microsecond=0)
            string_streak_end_date = datetime.strftime(streak_end_date, "%Y-%m-%d %H:%M:%S")
            streak_length = 27
            with sqlite3.connect("habit_tracker_db.db") as conn:
                user = UserProfile("Daisy", "Luna", "username2",
                                   "6b6b681e6617c2d34d5bc96d5bdc23020b5a81e88f150d89968d96750227bf7a")
                # Call the reset_daily_streak() function with the 'conn' argument
                user.reset_daily_streak()

                # Verify that the streak of mock selected habit is updated properly at HabitsData table in the database
                cur = conn.cursor()
                cur.execute(
                    "SELECT * FROM HabitsData WHERE habit_name = ? AND habit_creator = ? AND habit_type = ? "
                    "AND habit_frequency = ? AND created_datetime = ? AND last_completion_date = ? "
                    "AND habit_streak = ?",
                    [habit_name, username, habit_type, habit_frequency, created_datetime, last_completion_date,
                     habit_streak])
                result = cur.fetchall()
                if result:
                    self.assertEqual(result[0][0], habit_name)
                    self.assertEqual(result[0][1], username)
                    self.assertEqual(result[0][2], habit_type)
                    self.assertEqual(result[0][3], habit_frequency)
                    self.assertEqual(result[0][4], created_datetime)
                    self.assertEqual(result[0][5], last_completion_date)
                    self.assertEqual(result[0][6], habit_streak)

                # Verify that the streak of mock selected habit is updated properly at StreaksData table in the database
                cur.execute(
                    "SELECT * FROM StreaksData WHERE habit_name = ? and habit_creator = ? and habit_type = ? "
                    "and habit_frequency = ? and streak_start_date = ? ",
                    (habit_name, username, habit_type, habit_frequency, streak_start_date))
                result = cur.fetchall()
                if result:
                    self.assertEqual(result[0][0], habit_name)
                    self.assertEqual(result[0][1], username)
                    self.assertEqual(result[0][2], habit_type)
                    self.assertEqual(result[0][3], habit_frequency)
                    self.assertEqual(result[0][4], streak_start_date)
                    self.assertEqual(result[0][5], string_streak_end_date)
                    self.assertEqual(result[0][6], streak_length)

                # Verify that the correct message is displayed
                expected_output = f"The streaks of {habit_name} have been auto-reset to 0 " \
                                  f"since there is no marking completed during last 24 hours."
                self.assertIn(expected_output, self.output.getvalue().strip())

                # Clear data changes that were processed while running the test
                cur.execute("UPDATE HabitsData set last_completion_date = ?, habit_streak = 27 WHERE habit_name = ?"
                            "AND habit_creator = ?",
                            ('2023-01-27 00:05:00', habit_name, username))
                conn.commit()
                cur.execute(
                    "UPDATE StreaksData SET streak_end_date = ? "
                    "WHERE habit_name = ? AND habit_creator = ?",
                    [None, habit_name, username])
                conn.commit()

    @freeze_time('2023-02-05 00:05:00')
    def test_reset_weekly_streak(self):
        """
            This method defines a unit test for the reset_weekly_habit() function of the UserProfile class.
            It mocks the output of is_last_completion_date_present to True and checks that the mock selected weekly habit is correctly made reset the streaks
            at the database and checks that the expected output message has been printed.
            The test case uses the `@freeze_time` decorator to freeze the time to a specific date and time.
        """
        with mock.patch("functions.UserProfile.is_last_completion_date_present", return_value=True):
            # Define the references which are expected to get result like these
            habit_name = "Self-assessment"
            username = "username2"
            habit_type = "Personal Growth"
            habit_frequency = "Weekly"
            created_datetime = '2023-01-01 00:00:00'
            last_completion_date = None
            habit_streak = 0
            streak_start_date = '2023-01-01 00:05:00'
            streak_end_date = datetime.now().replace(microsecond=0)
            string_streak_end_date = datetime.strftime(streak_end_date, "%Y-%m-%d %H:%M:%S")
            streak_length = 4
            with sqlite3.connect("habit_tracker_db.db") as conn:
                user = UserProfile("Daisy", "Luna", "username2",
                                   "6b6b681e6617c2d34d5bc96d5bdc23020b5a81e88f150d89968d96750227bf7a")
                # Call the reset_weekly_habit() function with the 'conn' argument
                user.reset_weekly_streak()

                # Verify that the streak of mock selected habit is updated properly at HabitsData table in the database
                cur = conn.cursor()
                cur.execute(
                    "SELECT * FROM HabitsData WHERE habit_name = ? AND habit_creator = ? AND habit_type = ? "
                    "AND habit_frequency = ? AND created_datetime = ? AND last_completion_date = ? "
                    "AND habit_streak = ?",
                    [habit_name, username, habit_type, habit_frequency, created_datetime, last_completion_date,
                     habit_streak])
                result = cur.fetchall()
                if result:
                    self.assertEqual(result[0][0], habit_name)
                    self.assertEqual(result[0][1], username)
                    self.assertEqual(result[0][2], habit_type)
                    self.assertEqual(result[0][3], habit_frequency)
                    self.assertEqual(result[0][4], created_datetime)
                    self.assertEqual(result[0][5], last_completion_date)
                    self.assertEqual(result[0][6], habit_streak)

                # Verify that the streak of mock selected habit is updated properly at StreaksData table in the database
                cur.execute(
                    "SELECT * FROM StreaksData WHERE habit_name = ? and habit_creator = ? and habit_type = ? "
                    "and habit_frequency = ? and streak_start_date = ? ",
                    (habit_name, username, habit_type, habit_frequency, streak_start_date))
                result = cur.fetchall()
                if result:
                    self.assertEqual(result[0][0], habit_name)
                    self.assertEqual(result[0][1], username)
                    self.assertEqual(result[0][2], habit_type)
                    self.assertEqual(result[0][3], habit_frequency)
                    self.assertEqual(result[0][4], streak_start_date)
                    self.assertEqual(result[0][5], string_streak_end_date)
                    self.assertEqual(result[0][6], streak_length)

                # Verify that the correct message is displayed
                expected_output = f"The streaks of {habit_name} have been auto-reset to 0 " \
                                  f"since there is no marking completed during last 7 days."
                self.assertIn(expected_output, self.output.getvalue().strip())

                # Clear data changes that were processed while running the test
                cur.execute("UPDATE HabitsData set last_completion_date = ?, habit_streak = 4 WHERE habit_name = ?"
                            "AND habit_creator = ?",
                            ('2023-01-28 00:05:00', habit_name, username))
                conn.commit()
                cur.execute(
                    "UPDATE StreaksData SET streak_end_date = ? "
                    "WHERE habit_name = ? AND habit_creator = ?",
                    [None, habit_name, username])
                conn.commit()

    def test_show_all_habits(self):
        """
            This method defines a unit test for the show_all_habits() function of the analytics module.
            This test function is to verify that the show_all_habits() function correctly displays all the habits
            created by a user as a table format.

            In this test, the associated user account is username2.
        """

        # Set up test data
        username = "username2"
        expected_output = ("Your all created habits list is as follows :)\n"
            '+----------------------+----------------------+-----------------+----------------------+--------------------------------+--------------------------------+\n'
            '|      Habit Name      |    Habit Creator     |   Habit Type    |   Habit Frequency    |        Created Datetime        |      Last Completion Date      |\n'
            '+======================+======================+=================+======================+================================+================================+\n'
            '| Meditation           | username2            | Emotional       | Daily                | 2023-01-01 00:00:00            | 2023-01-31 00:05:00            |\n'
            '|                      |                      | Relaxation      |                      |                                |                                |\n'
            '+----------------------+----------------------+-----------------+----------------------+--------------------------------+--------------------------------+\n'
            '| Self-assessment      | username2            | Personal Growth | Weekly               | 2023-01-01 00:00:00            | 2023-01-28 00:05:00            |\n'
            '+----------------------+----------------------+-----------------+----------------------+--------------------------------+--------------------------------+\n'
            '| Exercise             | username2            | Physical Health | Daily                | 2023-01-02 00:00:00            | 2023-01-30 00:05:00            |\n'
            '+----------------------+----------------------+-----------------+----------------------+--------------------------------+--------------------------------+\n'
            '| Writing Diary        | username2            | Personal Growth | Daily                | 2023-01-01 00:00:00            | 2023-01-27 00:05:00            |\n'
            '+----------------------+----------------------+-----------------+----------------------+--------------------------------+--------------------------------+\n'
        )

        # Redirect stdout to a StringIO object
        with StringIO() as buf, redirect_stdout(buf):
            # Call the function
            analytics.show_all_habits(username)

            # Get the printed output
            actual_output = buf.getvalue()

        # Compare the actual and expected outputs
        self.assertEqual(actual_output, expected_output)

    def test_show_daily_habits(self):
        """
            This method defines a unit test for the show_daily_habits() function of the analytics module.
            This test function is to verify that the show_daily_habits() function correctly displays all the habits
            created by a user as a table format.

            In this test, the associated user account is username1.
        """
        # Set up test data
        username = "username1"
        expected_output = ("Your all created daily habits list is as follows :)\n"
            '+----------------------+----------------------+-----------------+----------------------+--------------------------------+--------------------------------+\n'
            '|      Habit Name      |    Habit Creator     |   Habit Type    |   Habit Frequency    |        Created Datetime        |      Last Completion Date      |\n'
            '+======================+======================+=================+======================+================================+================================+\n'
            '| Healthy Diet         | username1            | Physical Health | Daily                | 2023-01-01 00:00:00            | 2023-01-28 00:05:00            |\n'
            '+----------------------+----------------------+-----------------+----------------------+--------------------------------+--------------------------------+\n'
            '| Meditation           | username1            | Emotional       | Daily                | 2023-01-30 00:00:00            | None                           |\n'
            '|                      |                      | Relaxation      |                      |                                |                                |\n'
            '+----------------------+----------------------+-----------------+----------------------+--------------------------------+--------------------------------+\n'
        )

        # Redirect stdout to a StringIO object
        with StringIO() as buf, redirect_stdout(buf):
            # Call the function
            analytics.show_daily_habits(username)

            # Get the printed output
            actual_output = buf.getvalue()

        # Compare the actual and expected outputs
        self.assertEqual(actual_output, expected_output)

    def test_show_weekly_habits(self):
        """
            This method defines a unit test for the show_weekly_habits() function of the analytics module.
            This test function is to verify that the show_weekly_habits() function correctly displays all the habits
            created by a user as a table format.

            In this test, the associated user account is username1.
        """
        # Set up test data
        username = "username1"
        expected_output = ("Your all created weekly habits list is as follows :)\n"
            '+----------------------+----------------------+-----------------+----------------------+--------------------------------+--------------------------------+\n'
            '|      Habit Name      |    Habit Creator     |   Habit Type    |   Habit Frequency    |        Created Datetime        |      Last Completion Date      |\n'
            '+======================+======================+=================+======================+================================+================================+\n'
            '| Family Time          | username1            | Relationships   | Weekly               | 2023-01-01 00:00:00            | 2023-01-31 00:05:00            |\n'
            '+----------------------+----------------------+-----------------+----------------------+--------------------------------+--------------------------------+\n'
            '| Self-assessment      | username1            | Personal Growth | Weekly               | 2023-01-01 00:00:00            | 2023-01-31 00:05:00            |\n'
            '+----------------------+----------------------+-----------------+----------------------+--------------------------------+--------------------------------+\n'
        )

        # Redirect stdout to a StringIO object
        with StringIO() as buf, redirect_stdout(buf):
            # Call the function
            analytics.show_weekly_habits(username)

            # Get the printed output
            actual_output = buf.getvalue()

        # Compare the actual and expected outputs
        self.assertEqual(actual_output, expected_output)

    def test_current_streak_summary(self):
        """
            This method defines a unit test for the current_streak_summary() function of the analytics module.
            This test function is to verify that the current_streak_summary() function correctly displays current streaks of all habits
            created by a user as a table format.

            In this test, the associated user account is username2.
        """
        # Set up test data
        username = "username2"
        expected_output = ("Your Current Streak Summary of all created habits list is as follows :)\n"
            '+----------------------+-----------------+-----------------+------------+--------------------------------+--------------------------------+------------+\n'
            '|      Habit Name      |  Habit Creator  |   Habit Type    |   Habit    |        Created Datetime        |      Last Completion Date      |   Habit    |\n'
            '|                      |                 |                 | Frequency  |                                |                                |   Streak   |\n'
            '+======================+=================+=================+============+================================+================================+============+\n'
            '| Meditation           | username2       | Emotional       | Daily      | 2023-01-01 00:00:00            | 2023-01-31 00:05:00            | 31         |\n'
            '|                      |                 | Relaxation      |            |                                |                                |            |\n'
            '+----------------------+-----------------+-----------------+------------+--------------------------------+--------------------------------+------------+\n'
            '| Self-assessment      | username2       | Personal Growth | Weekly     | 2023-01-01 00:00:00            | 2023-01-28 00:05:00            | 4          |\n'
            '+----------------------+-----------------+-----------------+------------+--------------------------------+--------------------------------+------------+\n'
            '| Exercise             | username2       | Physical Health | Daily      | 2023-01-02 00:00:00            | 2023-01-30 00:05:00            | 29         |\n'
            '+----------------------+-----------------+-----------------+------------+--------------------------------+--------------------------------+------------+\n'
            '| Writing Diary        | username2       | Personal Growth | Daily      | 2023-01-01 00:00:00            | 2023-01-27 00:05:00            | 27         |\n'
            '+----------------------+-----------------+-----------------+------------+--------------------------------+--------------------------------+------------+\n'
        )

        # Redirect stdout to a StringIO object
        with StringIO() as buf, redirect_stdout(buf):
            # Call the function
            analytics.current_streak_summary(username)

            # Get the printed output
            actual_output = buf.getvalue()

        # Compare the actual and expected outputs
        self.assertEqual(actual_output, expected_output)

    def test_current_streak_of_selected_habit(self):
        """
            This method defines a unit test for the current_streak_of_selected_habit() function of the analytics module.
            This test function is to verify that the current_streak_of_selected_habit() function correctly displays the current streak of mock selected habit in the user account.

            In this test, the associated user account is username2.
        """
        with mock.patch("analytics.questionary.select") as mock_select:
            mock_select.return_value = mock.MagicMock(ask=mock.Mock(
                side_effect=["Meditation ~~~ Daily ~~~ Emotional Relaxation"]))
            username = "username2"

            # Call the function
            analytics.current_streak_of_selected_habit(username)

            # Verify that the correct message is displayed
            expected_output = ("The current streak of your selected habit is as follows.\n"
                f"Current streak of Meditation ~~~ Daily ~~~ Emotional Relaxation: 31")
            self.assertIn(expected_output, self.output.getvalue().strip())

    def test_longest_streak_summary(self):
        """
            This method defines a unit test for the longest_streak_summary() function of the analytics module.
            This test function is to verify that the longest_streak_summary() function correctly displays the longest run streaks of all habits
            created by a user as a table format.

            In this test, the associated user account is username1.
        """
        # Set up test data
        username = "username1"
        expected_output = ("Your Longest run Streak Summary of all created habits list is as follows :)\n"
            '+----------------------+-----------------+-----------------+------------+--------------------------------+--------------------------------+------------+\n'
            '|      Habit Name      |  Habit Creator  |   Habit Type    |   Habit    |       Streak Start Date        |        Streak End Date         |   Habit    |\n'      
            '|                      |                 |                 | Frequency  |                                |                                |   Streak   |\n'       
            '+======================+=================+=================+============+================================+================================+============+\n'       
            '| Family Time          | username1       | Relationships   | Weekly     | 2023-01-01 00:05:00            | None                           | 5          |\n'       
            '+----------------------+-----------------+-----------------+------------+--------------------------------+--------------------------------+------------+\n'       
            '| Healthy Diet         | username1       | Physical Health | Daily      | 2023-01-01 00:05:00            | 2023-01-14 00:30:00            | 13         |\n'
            '+----------------------+-----------------+-----------------+------------+--------------------------------+--------------------------------+------------+\n'
            '| Self-assessment      | username1       | Personal Growth | Weekly     | 2023-01-01 00:05:00            | None                           | 5          |\n'
            '+----------------------+-----------------+-----------------+------------+--------------------------------+--------------------------------+------------+\n'
        )

        # Redirect stdout to a StringIO object
        with StringIO() as buf, redirect_stdout(buf):
            # Call the function
            analytics.longest_streak_summary(username)

            # Get the printed output
            actual_output = buf.getvalue()

        # Compare the actual and expected outputs
        self.assertEqual(actual_output, expected_output)

    def test_longest_streak_of_selected_habit(self):
        """
            This method defines a unit test for the longest_streak_of_selected_habit() function of the analytics module.
            This test function is to verify that the longest_streak_of_selected_habit() function correctly displays the longest run streak of mock selected habit in the user account.

            In this test, the associated user account is username1.
        """
        with mock.patch("analytics.questionary.select") as mock_select:
            mock_select.return_value = mock.MagicMock(ask=mock.Mock(
                side_effect=["Healthy Diet ~~~ Daily ~~~ Physical Health"]))
            username = "username1"

            # Call the function
            analytics.longest_streak_of_selected_habit(username)

            # Verify that the correct message is displayed
            expected_output = ("The longest run streak of your selected habit is as follows.\n"
                f"Longest streak of Healthy Diet ~~~ Daily ~~~ Physical Health: 13")
            self.assertIn(expected_output, self.output.getvalue().strip())
