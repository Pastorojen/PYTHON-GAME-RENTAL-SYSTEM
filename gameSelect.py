# -*- coding: utf-8 -*-
"""
This module has two functions for analyze new game buy purposes.
suggestion_of_buying: This function is created to make analyze about what \
games should buy from manager.
graphs: This function is created to show graphs related rental history.

Created By: F217699 4 Nov 2023
"""

import database as db
import pandas as pd
import matplotlib.pyplot as plt


def suggestion_of_buying(budget):
    
    """This function is created to give manager advise about what games \
    they should buy. To analyze it past rent enquiry data is used.
    """
    
    new_buy = [] # return list created here initialy empty version
    data = db.rental_history() # upload all the rental history data
    df = pd.DataFrame(data) # convert data into dataframe
    # gives column names
    column_names = ['How many times rented', 'Platform','Genre',
                    'Title','Purchase_Price','Purchase_Date']
    df.columns=column_names
    #Since some games have coppies. Group each game with summing copies as well
    df["grouped"] = df["Platform"]+df["Genre"]+df["Title"]
    #rename grouped df
    df_group= df.groupby('grouped').sum(numeric_only=False).reset_index() 
    #calculate the income rates buy using their purchase price and rental times
    #in this section rate is calculated the way manager can make most income
    rate = df_group['How many times rented']/df_group['Purchase_Price'] 
    df_group["rate"] = rate
    #sort the new df values high to low to start with best income maker games
    df_group = df_group.sort_values(by='rate', ascending=False)
    
    #The loop is created to calculate new rate after purching best rate game
    #Because rate will change depends on how many copies store has.
    #If we do not do this process, this function suggest to buy same most rated
    #game with all of the money which does not make sense at all.

    while budget > min(df["Purchase_Price"]):
        
        
        index_group = df_group['rate'].idxmax()#find index row of max value
        game  = df_group["grouped"][index_group]#find game is most popular        
        index = df[df["grouped"]==game].index[0]#find game in general df
        price = df["Purchase_Price"][index]#find this game's price
        #Set new price for further calculations(to not buy same game many)
        n_price = df_group["Purchase_Price"][index_group] + price 
        #Declare the new price in grouped df
        df_group.loc[index_group,"Purchase_Price"] = n_price
        #find how many times this game rented for calculation
        num_of_rent = df_group["How many times rented"][index_group]
        #find new rate after we buy this game
        new_rate =  num_of_rent / n_price
        #declare new rate point for further calculations
        df_group.loc[index_group,"rate"] = new_rate
        #spend the budget
        if budget > price: #check if there is enough money
            budget -= price 
            #add new game that suggested to buy into return list
            new_buy.append([df["Platform"][index],df["Genre"][index],
                        df["Title"][index],df["Purchase_Price"][index]])
        
    return new_buy, budget #Returns new_buy list and left budget


def graphs():
    
    """ This function is created to draw 2 graphs that show most rented genres \
    and platforms. This function is not directly related the suggested games \
    to buy. But it shows the way for the future trends.
    """
    
    data = db.rental_history() # upload all the rental history data
    df = pd.DataFrame(data) # convert data into dataframe
    # gives column names
    column_names = ['How many times rented', 'Platform','Genre',
                    'Title','Purchase_Price','Purchase_Date']
    df.columns=column_names    
    # Group data depending on their platforms
    grouped = df.groupby('Platform')['How many times rented']
    # Give index to the grouped data
    grouped = grouped.mean().reset_index()# Mean has been took to show rent 
    # Draw a bar graph to show platform and rental rates
    plt.bar(grouped['Platform'], grouped['How many times rented'])
    plt.xlabel('Platform')#X label is named platform
    plt.ylabel('Values')#Y label is named Values
    plt.title('Rent Chance Depending on Platform') # The title is given
    plt.show() # Graph is shown
    
    # Group data depending on their Genre
    grouped_genre = df.groupby('Genre')['How many times rented']
    # Give index to the grouped data
    grouped_genre = grouped_genre.mean().reset_index()    
    # Draw a bar graph to show platform and rental rates
    plt.bar(grouped_genre['Genre'], grouped_genre['How many times rented'])
    plt.xlabel('Genre')#X label is named genre
    plt.ylabel('Rate')#Y label is named Values
    plt.title('Rent Chance Depending on Genre')# The title is given
    plt.xticks(rotation=90)#Labels rotate 90 degrees
    plt.show()# Graph is shown
    
if __name__ == "__main__":
    
    """In this test section all of the function will be called and see if \
    there is any error.
    """
    
    budget = 100
    
    try:
        
        suggestion_of_buying(budget)
        print("""1. suggestion_of_buying(budget) \
function test is succesfull""")
        graphs()
        print("""2. graphs() function test is succesfull""")
        print("All test are finished succesfully")
        print(__doc__)
              
    except:
        
        print("An error occured during function test.")