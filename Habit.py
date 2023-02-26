"""
This module defines a Habit class for managing information about habits in a database.
It imports os, and sqlite3.
"""

import os
import sqlite3


# HABIT CLASS
class Habit:
    """
    Creating a Habit class.

    Attributes:
    -----------
        - habit_name (str): The name of the habit.
        - habit_creator (str): The user who created the habit.
        - habit_type (str): The type of habit (e.g., Physical Health, Emotional Relaxation, etc.).
        - habit_frequency (str): The frequency at which the habit is performed (e.g., daily and weekly.).
        - created_datetime (datetime): The date and time at which the habit was created.
    """

    # INIT METHOD
    def __init__(self, habit_name, habit_creator, habit_type, habit_frequency, created_datetime,
                 last_completion_date, streak_start_date, streak_end_date, streak_length, habit_streak=0):
        """
        Initializes a new instance of the Habit class.

        Args:
        -----
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

        self.habit_name = habit_name
        self.habit_creator = habit_creator
        self.habit_type = habit_type
        self.habit_frequency = habit_frequency
        self.created_datetime = created_datetime
        if last_completion_date is None:
            self.last_completion_date = None
        else:
            self.last_completion_date = last_completion_date
        self.habit_streak = habit_streak
        self.streak_start_date = streak_start_date
        self.streak_end_date = streak_end_date
        self.streak_length = streak_length

        # Build the file path for the database file
        connect_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'habit_tracker_db.db')

        # Connect to the database
        self.conn = sqlite3.connect(connect_db)

        # Create a cursor for executing SQL commands
        self.cur = self.conn.cursor()

    def habits_table(self):
        """
            Create the Habits Data table in the database.
        """
        conn = sqlite3.connect('habit_tracker_db.db')
        self.cur = conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS HabitsData "
            "(habit_name TEXT, habit_creator TEXT, habit_type TEXT, habit_frequency TEXT, created_datetime DATETIME, "
            "last_completion_date DATETIME, habit_streak INTEGER)"
        )
        self.cur.close()
        self.conn.close()

    def streaks_table(self):
        """
            Create the Streak History table in the database.
        """
        conn = sqlite3.connect('habit_tracker_db.db')
        self.cur = conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS StreaksData "
            "(habit_name TEXT, habit_creator TEXT, habit_type TEXT, habit_frequency TEXT, streak_start_date DATETIME, "
            "streak_end_date DATETIME, streak_length INTEGER)"
        )
        self.cur.close()
        self.conn.close()

    def users_table(self):
        """
            Create the user information table in the database.
        """
        conn = sqlite3.connect('habit_tracker_db.db')
        self.cur = conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS User "
            "(forename TEXT, surname TEXT, username VARCHAR, password VARCHAR)"
        )
        self.cur.close()
        self.conn.close()


# Predefined Habits List which be a list of choices in the program for the user to select
predefined_habits_list = [
    ('Exercise', 'Physical Health', 'Daily'),
    ('Meditation', 'Emotional Relaxation', 'Daily'),
    ('Self-assessment', 'Personal Growth', 'Weekly'),
    ('Family Time', 'Relationships', 'Weekly'),
    ('Healthy Diet', 'Physical Health', 'Daily'),
    ('Writing Diary', 'Personal Growth', 'Daily'),
    ('Cleaning House', 'Emotional Relaxation', 'Weekly')
]
