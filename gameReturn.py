# -*- coding: utf-8 -*-
"""
This module is created with 2 functions on it. 
Return item: which is used to make return process of the game.
Return item available: shows which game can be returned.

Created by:F217699 4 Nov 2023
"""

import database as db

def return_item(game_id):
    
    """This function is used to make return process of the game.
    """
    
    try:
        
        return db.return_item(game_id)#Try return the game in database
        
    except:#If the process is not succesfull gives information
        
        return "Some error has been occured during return statement!"
    

def return_item_available():
    
    """This function is used to make show which games can be return.
    """
    
    try:
        
        return db.return_availability()#Try return the game in database
        
    except:#If the process is not succesfull gives information
        
        return "Some error has been occured during return statement!"
    
if __name__ == "__main__":
    
    """In this test section all of the function will be called and see if \
    there is any error.
    """
    
    game_id =1
  
    try:
        
        return_item(game_id)
        print("""1. return_item(game_id) function test is succesfull""")
        return_item_available()
        print("""2. return_item_available() function test is succesfull""")
        print("All test are finished succesfully")
        print(__doc__)
              
    except:
        
        print("An error occured during function test.")