# -*- coding: utf-8 -*-
"""
This module created to make rental process. Module has 2 function in it.
rent_subcriptions_checker: controls the subcription and database parameters \
to observe if the game can be rented.
rental_proces: make the rental process with connection db file.

Created By: F217699 4 Nov 2023
"""

import subscriptionManager as r
import database as db
from datetime import datetime

def rent_subcriptions_checker(game_id,Costumer_ID):
    
    """ This function is created to check if costumer have right to rent a \
    game and if the game which costumer would like the rent is available or \
    not. In this function subscriptionManager.pyc is used to check validation \
    informations. And some other database controls applied.
    """

    subscriptions_dic = r.load_subscriptions()#loads costumers informations  
    
    try:#checks the given costumer id's informations
        
        # Upload subscriptiontypes informations
        ST= subscriptions_dic[str(Costumer_ID)]["SubscriptionType"] 
        
        # Upload subscription date informations
        SED = subscriptions_dic[str(Costumer_ID)]["EndDate"]
        SED = SED.strftime("%Y-%m-%d") 
        
    except:#if there is no costumer like given return false statement.
        
        return False,("There is no costumer defined %2d"%(Costumer_ID))
    
    #The code below checks how many games reserved from database
    Games_reserved = db.how_many_games_reserverd(Costumer_ID)
    
    if ST == "Basic":#If Subscription Type is basic
        rental_limit = r.BASIC_LIMIT#set the rental limit basic limit
    elif ST == "Premium":#If Subscription Type is premium
        rental_limit = r.PREMIUM_LIMIT#set the rental limit premium limit
       
    date = datetime.now().strftime("%Y-%m-%d")#Takes today's date   
    
    #Checks if date is exits and the rental limit is lower than rented games
    if (SED > date and rental_limit > Games_reserved
    and db.game_availability(game_id)): 
           
        return True,"Have right to rent!" #If true returns true
    
    else: #Checks if not date and rental limit is not matched  
        
        #The code below checks what condition is not match
        if not (db.game_availability(game_id) and 
        (SED > date or rental_limit > Games_reserved)):
            
            return False,"The game is not available!"#if game is not available
        
        else:#If subscription is not valid or not have right.
            
            return False,"""Subscription date is passed or have rent maximum \
number of games according to plan!"""
    
  
    
def rental_proces(game_id,Costumer_ID):
    
    """ This function is created to make rental process."""
    
    # The code below apply the validation procedure
    situation = rent_subcriptions_checker(game_id,Costumer_ID)
    if situation[0]: #If condition True(right the rent)  
        try:
            
            #Code below tries to make enquiry into database
            db.insert_rental_history(game_id,Costumer_ID)
            return (str(situation[1]) + " Rental process have been completed!")
        except:
            
            #If process is not complate succesfully gives information
            return "Something wrong in database please try again later!"
    else:
        return(situation[1])#If costumer can not rent the game, gives info.
        
        
if __name__ == "__main__":
    
    """In this test section all of the function will be called and see if \
    there is any error.
    """
    
    game_id =1
    Costumer_ID=0
    
    try:
        
        rent_subcriptions_checker(game_id,Costumer_ID)
        print("""1. rent_subcriptions_checker(game_id,Costumer_ID) \
function test is succesfull""")
        rental_proces(game_id,Costumer_ID)
        print("""2. rental_proces(game_id,Costumer_ID) \
function test is succesfull""")
        print("All test are finished succesfully")
        print(__doc__)
              
    except:
        
        print("An error occured during function test.")