# Your name: Devin Vowels
# Your student id: 7797 8257
# Your email: dvowels@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    dir = os.path.dirname(__file__) + os.sep
    conn = sqlite3.connect(dir + db)
    cur = conn.cursor()
    
    #Getting restaurant info
    cur.execute('SELECT * FROM restaurants')
    restaurants_lst = []
    for row in cur:
        restaurants_lst.append(row)
    
    #Getting restaurant category info
    cur.execute('SELECT * FROM categories')
    categories_dct = {}
    for row in cur:
        categories_dct[row[0]] = row[1]
    
    #Getting restaurant buildings info
    cur.execute('SELECT * FROM buildings')
    buildings_dct = {}
    for row in cur:
        buildings_dct[row[0]] = row[1]   
    
    #Putting restaurant details into a nested dictionary
    restaurant_dct = {}
    for restaurant in restaurants_lst:
        category = categories_dct.get(restaurant[2])
        building = buildings_dct.get(restaurant[3])
        rating = restaurant[4]
        
        restaurant_dct[restaurant[1]] = {'category': category, 'building': building, 'rating': rating}
    
    return restaurant_dct


def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    dir = os.path.dirname(__file__) + os.sep
    conn = sqlite3.connect(dir + db)
    cur = conn.cursor()

    #Getting restaurant category info
    cur.execute('SELECT * FROM categories')
    categories_lst = []
    for row in cur:
        categories_lst.append(row)
    
    #Getting restaurant info
    cur.execute('SELECT * FROM restaurants')
    restaurants_lst = []
    for row in cur:
        restaurants_lst.append(row)    
    
    #Counting categories
    count_dct = {}
    for i in range(1, len(categories_lst) + 1):
        count_dct[i] = 0
    
    for c in restaurants_lst:
        for k,v in count_dct.items():
            if c[2] == k:
                count_dct.update({k: (v + 1)})
    
    #Replacing category IDs with names
    category_counts = {}
    row = 0
    for k, v in count_dct.items():
        category_counts[categories_lst[row][1]] = v
        row += 1


    #VISUALIZATION
    fig = plt.figure()
    
    #sorting categories in descending order
    sort = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_category_counts = {}
    for x in sort:
        sorted_category_counts.update({x[0]: x[1]})
    
    #creating x and y axis
    restaurant_categories = []
    counts = []
    for k,v in sorted_category_counts.items():
        restaurant_categories.append(k)
        counts.append(v)

    #plotting
    plt.barh(restaurant_categories, counts)
    
    plt.ylabel("Restaurant Categories")
    plt.xlabel("Number of Restaurants")
    plt.title("Types of Restaurants on South University Ave")
    


    fig.savefig("Restaurant_Types.png")
    plt.show()
    return category_counts


def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    dir = os.path.dirname(__file__) + os.sep
    conn = sqlite3.connect(dir + db)
    cur = conn.cursor()

    #Getting building info
    cur.execute('SELECT * FROM buildings')
    buildings_dct = {}
    for row in cur:
        buildings_dct[row[0]] = row[1]    

    #Getting restaurant info
    cur.execute('SELECT * FROM restaurants')
    restaurants_lst = []
    for row in cur:
        restaurants_lst.append(row)
    
    #Getting building number id
    key_list=list(buildings_dct.keys())
    val_list=list(buildings_dct.values())
    ind=val_list.index(building_num)
    building_type = key_list[ind]

    building_dct = {}
    for r in restaurants_lst:
        if building_type == r[3]:
            building_dct[r[1]] = r[4]

    #sorting categories in descending order
    sort_restaurants_dct = sorted(building_dct.items(), key=lambda x: x[1], reverse=True)

    final_lst = []
    for x in sort_restaurants_dct:
        final_lst.append(x[0])
    
    return final_lst

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    dir = os.path.dirname(__file__) + os.sep
    conn = sqlite3.connect(dir + db)
    cur = conn.cursor()

    #Getting restaurant info
    cur.execute('SELECT * FROM restaurants')
    restaurants_lst = []
    for row in cur:
        restaurants_lst.append(row)

    #Getting restaurant category info
    cur.execute('SELECT * FROM categories')
    categories_dct = {}
    for row in cur:
        categories_dct[row[0]] = row[1]
    
    #Getting restaurant buildings info
    cur.execute('SELECT * FROM buildings')
    buildings_dct = {}
    for row in cur:
        buildings_dct[row[0]] = row[1]



    #Ratings per category
    avg_category = {}
    for i in range(1, len(categories_dct) + 1):
        avg_category[i] = 0

    for r in restaurants_lst:
        avg_category[r[2]] = avg_category[r[2]] + r[4]

    category_ids = []
    for x in restaurants_lst:
        category_ids.append(x[2])
    
    for k,v in avg_category.items():
        count = category_ids.count(k)
        avg = v/count
        avg_category.update({k: round(avg, 1)})

    avg_category_final = sorted(avg_category.items(), key=lambda x: x[1], reverse=True)
    
    category = []
    c_rating = []
    for x in avg_category_final:
        category.append(x[0])
        c_rating.append(x[1])



    #Ratings per building
    avg_building = {}
    for i in range(1, len(buildings_dct) + 1):
        avg_building[i] = 0

    for r in restaurants_lst:
        avg_building[r[3]] = avg_building[r[3]] + r[4]

    building_ids = []
    for x in restaurants_lst:
        building_ids.append(x[3])
    
    for k,v in avg_building.items():
        count = building_ids.count(k)
        avg = v/count
        avg_building.update({k: round(avg, 1)})
   
    avg_building_final = sorted(avg_building.items(), key=lambda x: x[1], reverse=True)
    
    building = []
    b_rating = []
    for x in avg_building_final:
        building.append(x[0])
        b_rating.append(x[1])

    

    #VISUALIZATIONS
    fig = plt.figure()

    #Categories
    ax1 = fig.add_subplot(121)
    ax1.barh(category, c_rating, label = "Average Restaurant Ratings by Category")
    ax1.set_title("Average Restaurant Ratings by Category")
    ax1.set_xlim(0, 5)

    #Buildings
    ax1 = fig.add_subplot(122)
    ax1.barh(building, b_rating, label = "Average Restaurant Ratings by Category")
    ax1.set_title("Average Restaurant Ratings by Category")
    ax1.set_xlim(0, 5)
    
    fig.savefig("Category_Buidling_Ratings.png")
    plt.show()


#Try calling your functions here
def main():
    load_rest_data("South_U_Restaurants.db")
    plot_rest_categories("South_U_Restaurants.db")
    find_rest_in_building(1140, "South_U_Restaurants.db")
    get_highest_rating("South_U_Restaurants.db")

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
