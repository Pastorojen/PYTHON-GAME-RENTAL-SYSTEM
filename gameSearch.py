# -*- coding: utf-8 -*-
"""
This module has two functions for searching purposes.
image_shower: This function is created to show searched games pictures.
available_game_list: This function is created to see all available \
games for showing costumer what he/she can rent.

Created By: F217699 4 Nov 2023
"""

import database as db
from PIL import Image
from io import BytesIO

def available_game_list(searched_game =""):
    
    """ This function is created to see all available games for showing \
    costumer what he/she can rent.
    """
    alist = db.game_availability_regardless_search_name()#Apply db control
    
    if str(searched_game) == "":#If there is no search value typed

        return alist #return the all list.
    
    else:#If some value typed from user
        
        return_list=[]#Initial return list is empty
        
        for i in range(len(alist)): #For loop to check all variables
            #If the value comes from user is in the title of the game
            if str(searched_game).lower() in str(alist[i][3].lower()):
                #append this game to show list
                return_list.append(alist[i])
                
        return return_list#return the show list

def image_shower(ID):
    
    """This function is created to show picture of the games to the user
    """
    image_blob=db.image_shower_db(ID)#Take BLOB value of picture with db module
    image = Image.open(BytesIO(image_blob))#Convert into image shape this value   
    return image #Return the image value      

if __name__ == "__main__":
    
    """In this test section all of the function will be called and see if \
    there is any error.
    """
    
    ID='PS4AdventureMarvels Spider-Man 2'
    
    try:
        
        available_game_list(searched_game ="")
        print("""1. available_game_list(searched_game ="") \
function test is succesfull""")
        image_shower(ID)
        print("""2. image_shower(ID) function test is succesfull""")
        print("All test are finished succesfully")
        print(__doc__)
              
    except:
        
        print("An error occured during function test.")