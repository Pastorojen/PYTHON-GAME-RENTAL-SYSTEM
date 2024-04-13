# PYTHON-GAME-RENTAL-SYSTEM
It is example of game rental system in language of python. It has user interface which can be shown in jupyter notebook.

In the following part, there are some important explanations and
information about the project.

1) The Project Elements

-database.py, gameRent.py, gameReturn.py, gameSearch.py,
gameSelect.py python files
-menu.ipynb ipython file
-Game_Info.txt which stores games for initialization,
-Rental_History.txt which stores rental inquiries for initialization,
-Subscription_Info which stores customers information,
-subscriptionManager.pyc to check customer criteria
-GameRental.db which stores database tables.

2) GUI Explanation

The menu.ipynb file has ipywidgets GUI in it. When user run this file
there will be displayed enterence screen with 6 buttons and these are;

a) Rent Game: When this button is clicked there will be rent game page opened
user can see a list of games available that they can rent, user can type what
game they want to rent with doing it they can see shorter list and easy to find
-And also they can see the game's image
-If user want to rent the game they should enter their customer ID
the code will check if the ID is valid if so rental statement will occur.
-There is also go back main button which returns main screen.

b) Return Game: When this button is clicked there will be rent page opened
user can see a list of games which are waiting for return, and they can select what game they want to return, after they choose game and clicked return button the game return statement will be apply. There is also go back button

c) Buy New Game: When this button is clicked there will be buy new game page
opened that manager give budget to make analyze. After given budget there will be shown list of games that the manager should buy. It is calculated with rental history and picked best income maker ones. So the list based on most income makers. And it shows money left after purchase is completed.
And there will be also 2 graphs shows trends of genres and platforms.

d) Clear Database: When this button is clicked there will be clear database
page opened that manager clear all database and initiate empty tables to the
database again. There is also go back button.

e) Populate Data From TXT: When this button is clicked there will be populate data page opened. Manager can populate the data from TXT files into the database.

f) Information: When this button is clicked there will be information page will be opened. This page has same information with this TXT file.

3) Important Notes

-Game_Info.txt contains 94 games 
-Rental_History.txt contains 330 enquiries
-GameRental.db contains 3 tables (games, enquiries, images) populate them is available
-There is gameSearch file that can give user ability to search what games they are looking
for and it only shows available searched values which makes user life easier.
-There is always information massage When applied function is not succesfull and succesfull.
-There is selecting games for purchase order section that manager can give budget and see what games they need to buy. This section formula is to buy most income make games.
-Database also stores images of the games as well.

