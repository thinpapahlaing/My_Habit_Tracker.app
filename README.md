# Project: 'My Habit Tracker' app
## By Thin Pa Pa Hlaing
## Program Description
'My Habit Tracker' is a Python program that will help users track their habits and measure the progress toward important goals that the users want to achieve no matter whether to obtain a healthy lifestyle or to make improvements towards personal growth. Users can perform 8 main functions and their associated sub-functions within the program and all of these will make to keep the user on track to making progress toward their goals. The unique part of this program is that the visual display was emphasized while creating it by using ASCII art. Have fun with the program!

*This program is a university project for the Bachelor of Science in Data Science degree program.

### Motto of this app
Use 'My Habit Tracker' to ensure that each and every day that passes is productive!

## Features
* Seven Predefined habits with already defined types and frequencies
* Four habit types to choose when creating a habit (Physical Health, Emotional Relaxation, Personal Growth, Relationships)
* Two habit frequencies the users can select in creating a new habit (Daily and Weekly)
* Can easily mark a habit completed from the list of all existing habits in the user account which will be displayed to the user
* Only 1 streak count for marking a Daily habit completed within the 1-day period 
* Only 1 streak count for marking a Weekly habit completed within the 7-day period 
* Auto-reset streaks if the habits were not marked completed during their frequency range (Daily or Weekly)
* Show the habits statistics to the user in a visual table format using ASCII art.

## Let's get started
### Prerequisites
* Python version 3.7 or later
* PyCharm or another Python IDE to see the codes
* Libraries to install: questionary, texttable, freezegun

### Installation
1. Clone the repository by typing in your terminal or command prompt like this. 
```shell
git clone https://github.com/thinpapahlaing/My_Habit_Tracker.app.git
```
2. Open the project in PyCharm or another Python IDE to see the codes.
3. Install the required libraries using pip
```shell
pip install questionary texttable freezegun
```

**If git hasn't been installed yet on your device, 
please follow this link 'https://git-scm.com/downloads' and download one 
which is compatible with your device type. After this, you can follow the upper steps 1, 2, 3.

### Usage
After the users finished downloading the necessary libraries and successfully cloned the repository, the program can be started running. 

To run the program, **open your computer/laptop terminal or command prompt 
and first, navigate into the program directory as follows.**
This will make sure that all the habits' data, analyzing them, 
interacting and storing in the database will be within this directory, 
preventing for overlap database files. [Since you will clone the whole repository from GitHub, 
you can copy the following code and don't need to make adjustments to the repository name :) ]
```shell
cd My_Habit_Tracker.app/
```

After this step, and now you are in the directory of My_Habit_Tracker.app, you can continue typing this code in the terminal or command prompt 
and starts enjoying the program:
```shell
Python main.py
```

So after you saw the welcoming messages, if you are a first-time user, you must create an account first. 
Then login with earlier registered credentials, and you will see the list of menu options like this:
```shell
Select an option (1-8):
1. Choose predefined habits
2. Create a new habit
3. Mark a habit as completed
4. Adjust habits
5. Habit list overview
6. Habit performance statistics
7. User profile
8. Quit and log out
```
Type the function numbers which you want to interact with your habits like 1 or 2 or any function number within 1 to 8.

The followings are a brief description of the functions of what you can do with them.

* Function 1: When you type 1, the system will give you a list of seven predefined habits 
and if you want to have one or some of those habits in your account, you can select them by entering their id numbers 
and leave this function by entering -1. 


* Function 2: When you type 2, you can create a new habit on your own including choosing habit's type and frequency range as you want.


* Function 3: When you type 3, you can mark a habit as completed from the displayed list from the system 
and 1 streak will be counted for that habit.


* Function 4: This function has 4 sub-functions as follows. In this function, you can change the habit type, and habit frequency and 
even delete the already created habit in your account.
```shell
Select an option (1-4):
1. Change habit type
2. Change habit frequency
3. Delete habit
4. Go back to main menu
```


* Function 5: This function also has 4 sub-functions as follows. By choosing this function 5, 
you can see 1. all habits list, 2. all daily habits list, 3. all weekly habits list you have created in your account 
in a visual table format.
```shell
Select an option (1-4):
1. All habits list
2. All daily habits list
3. All weekly habits list
4. Go back to main menu
```

* Function 6: This function has 5 sub-functions as follows. 
In this function, you can choose an option to see 
the current streaks and longest-run streaks of all habits or only one habit you want to check. 
These data will also be shown to you in a visual table format.
```shell
Select an option (1-5):
1. Current streak summary
2. Current streak of selected habit
3. Longest streak summary
4. Longest streak of selected habit
5. Go back to main menu
```

* Function 7: This function is about managing your user account. 
In this function, you can edit your forename, surname, username, and password by selecting one option using the arrow key. 
You can find the 4 options to select like this:
```shell
? Which sector do you want to edit? (Use arrow keys)
 » (1) Forename
   (2) Surname
   (3) Username
   (4) Password
```

* Function 8: This is the last function within the program and by typing 8, you will log out from the program
and all the connections will be closed.

### Testing
You are also welcome to run the tests for this program.

**Please again make sure to be within My_Habit_Tracker.app directory before running any tests and predefined_habits module. 
If you are not in this directory, you can copy **'cd My_Habit_Tracker.app/'** which I described earlier in the Usage stage.

In order to perform testing, first please run the 'predefined_habits.py' module in PyCharm or another Python IDE.
You can also run this module in the terminal or command prompt by copying the below code:
```shell
Python testing/predefined_habits.py
```
After running this module, you can simply copy the testing call in your terminal as follows:
```shell
Python -m unittest testing/test_program.py
```

After running the unittest, you will see all 15 tests are passed. You can also additionally have a look at the CSV files 
which I attached in the testing folder of this page at GitHub. Those data were utilized for the whole 15 tests.

## Contributing
Contributions are welcome! 
Please open an issue or pull request for any bugs, feature requests, or other feedback.
This is my first Python project and I appreciate all of your feedback.

## License
This program is free for personal use only. 
It is part of a university project for a B.Sc. degree and 
should not be used for commercial purposes.
For educational uses, please include my name in the credits.
