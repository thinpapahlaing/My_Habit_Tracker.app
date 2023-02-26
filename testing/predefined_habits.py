"""
This module contains functions for creating a 'predefined_db' table in a SQLite database,
inserting 5 predefined habits into the table,
and connecting to the 'habit_tracker_db.db' database to execute these actions.
It imports sqlite3, hashlib and secrets.
"""

import sqlite3
import hashlib
import secrets


class TestData:
    """
        A class for generating test data in the habit tracker database for unit testing purposes.

        Attributes:
        -----------
            - cursor: A cursor object to execute SQL queries.
            - conn: A connection object to the SQLite database.
    """

    def __init__(self):
        """
            Initializes a TestData object with cursor and conn attributes set to None.
        """
        self.cursor = None
        self.conn = None

    def set_up(self):
        """
            Generates test data in the habit tracker database for unit testing purposes.
        """

        # Connect to the database
        self.conn = sqlite3.connect('habit_tracker_db.db')
        self.cursor = self.conn.cursor()

        # Define assistance functions for generating and hashing random passwords
        def generate_password():
            chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
            generated_password = ''.join(secrets.choice(chars) for _ in range(8))
            return generated_password

        def hash_password(password):
            """
                Hashes a password using SHA-256 algorithm.

                Args:
                -----
                    - password: A string representing the password to be hashed.

                Returns:
                --------
                    - A string representing the hashed password.
            """
            sha256 = hashlib.sha256()
            sha256.update(password.encode('utf-8'))
            return sha256.hexdigest()

        password_username1 = generate_password()
        hashed_password1 = hash_password(password_username1)

        self.cursor.execute("SELECT * FROM User WHERE username=?", ('username1',))
        result = self.cursor.fetchone()
        if not result:
            self.cursor.execute("INSERT INTO User (forename, surname, username, password) VALUES (?, ?, ?, ?)",
                                ('Tom', 'Ford', 'username1', hashed_password1))
            self.conn.commit()

            password_username2 = generate_password()
            hashed_password2 = hash_password(password_username2)
            self.cursor.execute("INSERT INTO User (forename, surname, username, password) VALUES (?, ?, ?, ?)",
                                ('Daisy', 'Luna', 'username2', hashed_password2))
            self.conn.commit()

            # All data related to username1 will be used in testing
            # The longest streak summary of all existed habits
            # Show all daily habits
            # Show all weekly habits

            # This data will be used in testing for
            # 1. Daily reset by mocking time to 31 Jan 00:05:00
            # 2. The Longest streak of a selected habit (This habit)
            self.cursor.execute("""
                INSERT INTO HabitsData (habit_name, habit_creator, habit_type, habit_frequency, created_datetime,
                last_completion_date, habit_streak) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('Healthy Diet', 'username1', 'Physical Health', 'Daily', '2023-01-01 00:00:00',
                  '2023-01-28 00:05:00', 12))
            self.conn.commit()
            self.cursor.execute("""
                        INSERT INTO StreaksData (habit_name, habit_creator, habit_type, habit_frequency,
                        streak_start_date, streak_end_date, streak_length) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ('Healthy Diet', 'username1', 'Physical Health', 'Daily', '2023-01-01 00:05:00',
                          '2023-01-14 00:30:00', 13))
            self.conn.commit()
            self.cursor.execute("""
                                INSERT INTO StreaksData (habit_name, habit_creator, habit_type, habit_frequency,
                                streak_start_date, streak_end_date, streak_length) VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, ('Healthy Diet', 'username1', 'Physical Health', 'Daily', '2023-01-17 00:05:00',
                                  'None', 12))
            self.conn.commit()

            self.cursor.execute("""
                        INSERT INTO HabitsData (habit_name, habit_creator, habit_type, habit_frequency, 
                        created_datetime, last_completion_date, habit_streak) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ('Family Time', 'username1', 'Relationships', 'Weekly', '2023-01-01 00:00:00',
                          '2023-01-31 00:05:00', 5))
            self.conn.commit()
            self.cursor.execute("""
                                INSERT INTO StreaksData (habit_name, habit_creator, habit_type, habit_frequency,
                                streak_start_date, streak_end_date, streak_length) VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, ('Family Time', 'username1', 'Relationships', 'Weekly', '2023-01-01 00:05:00',
                                  'None', 5))
            self.conn.commit()

            # This data will be used in testing for Delete habit function.
            self.cursor.execute("""
                                INSERT INTO HabitsData (habit_name, habit_creator, habit_type, habit_frequency, 
                                created_datetime, last_completion_date, habit_streak) VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, ('Self-assessment', 'username1', 'Personal Growth', 'Weekly',
                                  '2023-01-01 00:00:00', '2023-01-31 00:05:00', 5))
            self.conn.commit()
            self.cursor.execute("""
                                        INSERT INTO StreaksData (habit_name, habit_creator, habit_type, habit_frequency,
                                        streak_start_date, streak_end_date, streak_length) VALUES (?, ?, ?, ?, ?, ?, ?)
                                    """,
                                ('Self-assessment', 'username1', 'Personal Growth', 'Weekly',
                                 '2023-01-01 00:05:00', 'None', 5))
            self.conn.commit()

            # This data will be used in testing for marking this habit completed (non completed before) by mocking time to 31 Jan 00:05:00
            self.cursor.execute("""
                        INSERT INTO HabitsData (habit_name, habit_creator, habit_type, habit_frequency, 
                        created_datetime, last_completion_date, habit_streak) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ('Meditation', 'username1', 'Emotional Relaxation', 'Daily', '2023-01-30 00:00:00',
                          'None', 0))
            self.conn.commit()

            # All data related to username2 will be used in testing
            # Current streak summary of all existed habits
            # Show all existed habits

            # This data will be used in testing for Current streak of a selected habit (This Habit)
            self.cursor.execute("""
                INSERT INTO HabitsData (habit_name, habit_creator, habit_type, habit_frequency, created_datetime,
                last_completion_date, habit_streak) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('Meditation', 'username2', 'Emotional Relaxation', 'Daily', '2023-01-01 00:00:00',
                  '2023-01-31 00:05:00', 31))
            self.conn.commit()
            self.cursor.execute("""
                        INSERT INTO StreaksData (habit_name, habit_creator, habit_type, habit_frequency,
                        streak_start_date, streak_end_date, streak_length) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ('Meditation', 'username2', 'Emotional Relaxation', 'Daily', '2023-01-01 00:05:00',
                          'None', 31))
            self.conn.commit()

            # This data will be used in testing for auto Weekly reset of this habit by mocking time to 31 Jan 00:05:00
            self.cursor.execute("""
                INSERT INTO HabitsData (habit_name, habit_creator, habit_type, habit_frequency, created_datetime,
                last_completion_date, habit_streak) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('Self-assessment', 'username2', 'Personal Growth', 'Weekly', '2023-01-01 00:00:00',
                  '2023-01-28 00:05:00', 4))
            self.conn.commit()
            self.cursor.execute("""
                        INSERT INTO StreaksData (habit_name, habit_creator, habit_type, habit_frequency,
                        streak_start_date, streak_end_date, streak_length) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ('Self_assessment', 'username2', 'Personal Growth', 'Weekly', '2023-01-01 00:05:00',
                          'None', 4))
            self.conn.commit()

            # This data will be used in testing for marking this habit completed (completed before) by mocking time to 31 Jan 00:05:00
            self.cursor.execute("""
                        INSERT INTO HabitsData (habit_name, habit_creator, habit_type, habit_frequency, 
                        created_datetime, last_completion_date, habit_streak) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ('Exercise', 'username2', 'Physical Health', 'Daily', '2023-01-02 00:00:00',
                          '2023-01-30 00:05:00', 29))
            self.conn.commit()
            self.cursor.execute("""
                                INSERT INTO StreaksData (habit_name, habit_creator, habit_type, habit_frequency,
                                streak_start_date, streak_end_date, streak_length) VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, ('Exercise', 'username2', 'Physical Health', 'Daily',
                                  '2023-01-02 00:05:00', 'None', 29))
            self.conn.commit()

            # This data will be used in testing for auto Daily reset of this habit by mocking time to 29 Jan 00:10:00
            self.cursor.execute("""
                                    INSERT INTO HabitsData (habit_name, habit_creator, habit_type, habit_frequency, 
                                    created_datetime, last_completion_date, habit_streak) VALUES (?, ?, ?, ?, ?, ?, ?)
                                """, ('Writing Diary', 'username2', 'Personal Growth', 'Daily',
                                      '2023-01-01 00:00:00', '2023-01-27 00:05:00', 27))
            self.conn.commit()
            self.cursor.execute("""
                                            INSERT INTO StreaksData (habit_name, habit_creator, habit_type, habit_frequency,
                                            streak_start_date, streak_end_date, streak_length) VALUES (?, ?, ?, ?, ?, ?, ?)
                                        """, ('Writing Diary', 'username2', 'Personal Growth', 'Daily',
                                              '2023-01-01 00:05:00', 'None', 27))
            self.conn.commit()


test_data = TestData()
test_data.set_up()
