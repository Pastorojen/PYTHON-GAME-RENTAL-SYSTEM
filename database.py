# -*- coding: utf-8 -*-
"""
This module provides functionalities to manage database system.
It includes functions that called; 

initialization_tables,
initialization_information_from_txt,
insert_rental_history,
return_item,
how_many_games_reserverd,
game_availability_regardless_search_name,
return_availability,
game_availability,
rental_history,
image_shower_db

Created by F217699 4 Nov 2023
"""
# Import modules 
import sqlite3 # For database connections
from datetime import datetime # To use date data

def initialization_tables():
    
    """ This function is created to create / clear the tables in the db. \
    \ According to CW specifications db game_info and game_rental_history \
    tables must come empty. With using this function this tables will be \
    created or if they are already exist they will be cleaned.
    """   
    
    conn = sqlite3.connect('GameRental.db') # Connects the Database
    cursor = conn.cursor() #creates a cursor
  
    # initialization the table of game_info_db_table
    # Table has 6 columns which are ID, Platform, Genre, Title, Purchase price
    # and purchase date
    cursor.execute('''CREATE TABLE if not exists game_info_db_table
                 (id INT PRIMARY KEY NOT NULL,
                  Platform text,
                  Genre text,
                  Title text,
                  Purchase_Price_£ integer,
                  Purchase_Date text)''')
    conn.commit() #applies for execute command  
                          
    # initialization the table of rental_history_db_table
    # Table has 5 columns which are order_ID, Game_ID, Rental_Date
    # Return_Date and Costumer_ID         
    cursor.execute('''CREATE TABLE if not exists rental_history_db_table
                 (Order_ID integer PRIMARY KEY NOT NULL,
                  Game_ID integer,
                  Rental_Date text,
                  Return_Date text,
                  Costumer_ID integer)''')   
    conn.commit()#applies for execute command 
       
    try:
        # Clear if there is any existing data for initial statement
        cursor.execute('''DELETE FROM game_info_db_table;''')  
        conn.commit()  #applies for execute command              
        # Clear if there is any existing data for initial statement
        cursor.execute('''DELETE FROM rental_history_db_table;''') 
        conn.commit()#applies for execute command 
        conn.close()#closes the db connection
        return "Database Cleared Succesfully!"
    except:
        conn.close()#closes the db connection
        return """An Error Occured During Process! \
    If it is not fixed please restart kernel!"""


def initialization_informations_from_txt():
    
    """ This function is created to move initial datas from txt files into \
    database. It firstly read data from txt and insert them into database. \
    This function also fixes if there is bad data in txt file.
    """
    
    conn = sqlite3.connect('GameRental.db') # Connects the Database
    cursor = conn.cursor() #creates a cursor    

    with open('Game_Info.txt', 'r') as file: #reads data from Game_Info.txt
        head_lap = True # it created to take data without headers 
        for line in file: #read data from file line by line
            
            if head_lap: #skip the header
                head_lap = False #after header line take the other data
                continue #do not do anything when it is header line
            line_data = line.strip().split(',')#split data with using , 
            #The code below takes all seperated data into a list
            split_data = [item.split(',') for item in line_data]
            #The code below insert the split data into database
            cursor.execute( 
            	'''INSERT INTO game_info_db_table 
                (id,Platform, Genre,Title, Purchase_Price_£,Purchase_Date) 
            	VALUES (?,?,?,?,?,?)''',(int(split_data[0][0]),
                str(split_data[1][0]),str(split_data[2][0]),
                str(split_data[3][0]),int(split_data[4][0]),
                str(split_data[5][0]))) 
            conn.commit() #applies for execute command     
            
    file.close()#closes the file connection
    
    #reads data from Rental_History.txt
    with open('Rental_History.txt', 'r') as file:
        head_lap = True# it created to take data without headers 
        for line in file:#read data from file line by line
            
            if head_lap: #skip the header
                head_lap = False#after header line take the other data
                continue#do not do anything when it is header line
           
            line_data = line.strip().split(',') #split data with using ,  
            #The code below takes all seperated data into a list
            split_data = [item.split(',') for item in line_data]
            #The code below take last order_id in the table
            order_id = cursor.execute( '''select Order_ID from 
                                          rental_history_db_table 
                                          ORDER BY Order_ID DESC
                                          LIMIT 1;''' )
            order_id = order_id.fetchone()#Took the order_id  
            try:
                if len(order_id) == 0 : order_id = 1#Make order_id 1 if it is 0 
                else :  order_id = order_id[0]+1#Order_ID should increase 1   
            except:
                order_id = 0#If there is no order id exist before make it first
                
            ################ THIS SECTION IS FOR FIXING TXT BUGS##############
            
            ### FIXING NUMBER 1: FILL THE WRONG FORMAT DATES IN RETURN DATE ###
            
            # Return date is took from database dataframe    
            date_string = split_data[2][0]
            # Define the format of date string
            date_format = "%Y-%m-%d"
            try:
                # The date value comes from database Formatted as date 
                date_obj = datetime.strptime(date_string, date_format) 
            except:
                # If there is wrong format data fix it 
                split_data[2][0] = datetime.now().strftime("%Y-%m-%d")               
            # Return date is took from database dataframe    

            ### FIXING NUMBER 2: FILL THE WRONG FORMAT DATES IN RENTAL DATE ###
            
            # Return date is took from database dataframe    
            date_string = split_data[1][0]
            # Define the format of date string
            date_format = "%Y-%m-%d"
            try:
                # The date value comes from database Formatted as date 
                date_obj = datetime.strptime(date_string, date_format) 
            except:
                # If there is wrong format data or missing value fix it 
                split_data[1][0] = datetime.now().strftime("%Y-%m-%d")               
            # Return date is took from database dataframe    
                
            ########FIXING NUMBER 3 FIX THE FUTURE DATES####################
                
            date_string = split_data[2][0]
            # Define the format of date string
            date_format = "%Y-%m-%d"
            # The date value comes from database Formatted as date 
            date_obj = datetime.strptime(date_string, date_format)    
            if date_obj > datetime.now(): # if return has been done in future
                # Change the future date with todays date
                split_data[2][0] = datetime.now().strftime("%Y-%m-%d")     
                
            ################ END OF THE FIXING TXT BUGS ##############  
                          
            #The code below insert the split data into database
            cursor.execute( 
            	'''INSERT INTO rental_history_db_table 
                (Order_ID,Game_ID, Rental_Date,Return_Date, Costumer_ID) 
            	VALUES (?,?,?,?,?)''',(order_id,int(split_data[0][0]),
                str(split_data[1][0]),str(split_data[2][0]),
                int(split_data[3][0]))) 
            conn.commit() #applies for execute command 
    file.close()  #closes the file connection        
    conn.close() #closes the database connection 
    return "Upload Process Has Finished Succesfully!"



def insert_rental_history(game_id,costumer_id):
    
    """ This function created to insert a new enquiry after rental \
    statement. Function connects database and add new enquiry.
    """
    date = datetime.now().strftime("%Y-%m-%d")# Creates today's date to add db
    conn = sqlite3.connect('GameRental.db')# Connects the Database
    cursor = conn.cursor()#creates a cursor
    #The code below checks last added enquiry to add next enquiry after that
    order_id = cursor.execute( '''select Order_ID from rental_history_db_table 
                                  ORDER BY Order_ID DESC
                                  LIMIT 1;''' )
    order_id = order_id.fetchone() # see the last enquiry line 
    if len(order_id) == 0 : order_id = 1 #if there is not enquiry in db set 1
    else :  order_id = order_id[0]+1#other case set order_id with one upper 
    #The code below inserts the new rental history into db 
    #Game ID and costumer ID comes from user the other 2 param. created in func      
    cursor.execute( 
    	'''INSERT INTO rental_history_db_table 
        (Order_ID,Game_ID, Rental_Date, Costumer_ID) 
    	VALUES (?,?,?,?)''',(order_id,game_id,date,costumer_id)) 
    conn.commit()#applies for execute command
    conn.close()#closes the db connection
    
    
def return_item(Game_ID):
    
    """ This function is created to return the rental game which is taken \
    previously. According to CW Specification in this process only allowed \
    value that can be taken from user is Game_ID. That is why function only \
    take the value of the Game_ID from user.
    """

    conn = sqlite3.connect('GameRental.db') # Connects the Database
    cursor = conn.cursor() #creates a cursor
    date = datetime.now().strftime("%Y-%m-%d")# Creates today's date to add db
    #The code below select the related enquiry.      
    cursor.execute( 
    	'''select Order_ID from rental_history_db_table
            WHERE Return_Date IS NULL and Game_ID = ?
            order by Order_ID desc
            LIMIT 1;''',(Game_ID,)) 
    try:
        #The code below selects the order id for update statement.
        order_id = int(cursor.fetchall()[0][0])
        #The code below update the related rental history's return date
        cursor.execute( 
        	'''UPDATE rental_history_db_table
                SET Return_Date = ?
                WHERE order_id = ?;''',(date,order_id)) 
        conn.commit()#applies for execute command
        conn.close()#closes the db connection  
        return """Return have been completed succesfully! \
Thank you for choosing us:)"""
    except:
        return """There is no game id is waiting for \
return which is called: %2d"""%(Game_ID)
        
 
def how_many_games_reserverd(costumer_id):
    
    """This function is created to see how many games rented by asked \
    costumer ID. This information will be used to analyze if the user has \
    right the rent more games or not.
    """
    
    conn = sqlite3.connect('GameRental.db')#database connection
    cursor = conn.cursor() #creates cursor
    #The code below return the how many games rented by costumer data
    cursor.execute( 
    	'''select count(Order_ID) as coi from rental_history_db_table
            WHERE Return_Date is NULL and Costumer_ID = ?;''',(costumer_id,))  
    searched_number = cursor.fetchall()[0]#takes the exact number      
    conn.close() #closes the db connection     
            
    return int(searched_number[0])#Return the number of rented games from cos.  

def game_availability_regardless_search_name():
    
    """This function is created to show costumers that what games are \
    available and they can rent.
    """
    
    conn = sqlite3.connect('GameRental.db')#database connection
    cursor = conn.cursor() #creates cursor 
    #The code below returns the games data which have not been rented already.
    cursor.execute( 
    	''' SELECT id,Platform,Genre,Title FROM game_info_db_table
        WHERE id NOT IN 
        (SELECT Game_ID FROM rental_history_db_table
         WHERE Return_Date IS NULL);''')              
    all_list = cursor.fetchall()#Takes datas into a list   
    conn.close() #closes the db connection 
    return all_list#Return the list

def return_availability():
    
    """This function is created to show costumers that what games are \
    available to return.
    """
    
    conn = sqlite3.connect('GameRental.db')#database connection
    cursor = conn.cursor() #creates cursor 
    #The code below returns the games data which have been rented already.
    cursor.execute( 
    	''' SELECT id,Platform,Genre,Title FROM game_info_db_table
        WHERE id IN 
        (SELECT Game_ID FROM rental_history_db_table
         WHERE Return_Date IS NULL);''')   
  
    all_list = cursor.fetchall()#Takes datas into a list   
    conn.close() #closes the db connection 
    return all_list#Return the list
   

def game_availability(Game_ID):
    
    """ This function is created to check if the game which user want to rent \
    is available. If the game is not exist anymore or rented to someone else \
    this function is give massage. Normally user cannot select the game which \
    is not in database or rented. But for the bugs and technical error that \
    could happen in db, this function makes double check.
    """
    conn = sqlite3.connect('GameRental.db') #database connection
    cursor = conn.cursor() #creates cursor
    #The code below returns the games data which match with given id.
    cursor.execute( 
    	''' SELECT COUNT(*) FROM game_info_db_table
            WHERE id = ?;''',(Game_ID,)) 
    
    ifexist = cursor.fetchone()[0] #Checks if the game in database or not

    if ifexist :#If the games in database check if it is rented or not
        #The code below returns value which has no return date
        cursor.execute( 
        	'''select Game_ID from rental_history_db_table
                WHERE Return_Date IS NULL and Game_ID = ?
                order by Order_ID desc
                LIMIT 1;''',(Game_ID,)) 
        #if there is any value without return date it is rented already
        searched_number = len(cursor.fetchall())
        return not bool(searched_number)#Return boolen statement.
    
    else:
        print("there is no game id called: %2d" %(Game_ID))                    
        return False#Return false means that the game can not be rented
    conn.close()#closes the db connection      
    
def rental_history():
    
    """This function is created to get all of the rental history information \
    from database. The data is used to make analyze of new game purchases.
    """
    
    try:
        conn = sqlite3.connect('GameRental.db') #database connection
        cursor = conn.cursor() #creates cursor
        
        # Rented quantity, platform, genre, title, purchase price and date
        # data wanted from database
        cursor.execute( 
         	'''SELECT  count(r.Game_ID) as quantity,g.Platform,g.Genre,g.Title,
                g.Purchase_Price_£,purchase_date
                FROM rental_history_db_table as r
                LEFT JOIN game_info_db_table as g on r.Game_ID = g.ID
                group by r.Game_ID;''')  
                
        queries = cursor.fetchall()#All of the data has been sent into queries
        conn.close()#Close the database connection
        return queries # return all the values
    except: # If an error is occur during process give the massage
        return "An error occured during process!" 


def image_shower_db(ID):
    
    """ This function is created to take pictures from database.
    """
    conn = sqlite3.connect('GameRental.db')# Connects the Database
    cursor = conn.cursor()#creates a cursor
    #Take picture's depending on its ID number
    cursor.execute("SELECT Picture FROM Pictures WHERE Picture_ID = ?", (ID,))
    #Take picture's BLOB value
    image_blob = cursor.fetchone()[0]   
    conn.close()#Close the Database connection  
    
    return image_blob#returns the picture's BLOB value
    
    
if __name__ == "__main__":
    
    """In this test section all of the function will be called and see if \
    there is any error.
    """
    
    Game_ID,game_id = 1,1
    costumer_id =0
    ID='PS4AdventureMarvels Spider-Man 2'
    
    try:
        
        initialization_tables()
        print('1. initialization_tables() function test is succesfull.')
        initialization_informations_from_txt()
        print('''2. initialization_information_from_txt() \
function test is succesfull.''')
        insert_rental_history(game_id,costumer_id)
        print('''3. insert_rental_history(game_id,costumer_id) \
function test is succesfull.''')
        return_item(Game_ID)
        print('4. return_item() function test is succesfull.')
        how_many_games_reserverd(costumer_id)
        print('''5. how_many_games_reserverd(costumer_id) \
function test is succesfull.''')
        game_availability_regardless_search_name()
        print('''6. game_availability_regardless_search_name() \
function test is succesfull.''')
        return_availability()
        print('7. return_availability() function test is succesfull.')
        game_availability(Game_ID)
        print('8. game_availability(Game_ID) function test is succesfull.')
        rental_history()
        print('9. rental_history() function test is succesfull.')
        image_shower_db(ID)
        print('10. image_shower_db(ID) function test is succesfull.')
        print('All tests are applied and there is no error')
        print(__doc__)
    except:
        
        print('Error occured during function test')    
    
    