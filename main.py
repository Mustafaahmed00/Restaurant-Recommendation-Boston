from data import types, restaurant_data
from welcome import print_welcome
from linkedlist import LinkedList

print_welcome()

# Function to insert food types into a LinkedList
def insert_food_types():
    food_type_list = LinkedList()
    for food_type in types:
        food_type_list.insert_beginning(food_type)
    return food_type_list

# Function to insert restaurant data into a LinkedList of LinkedLists
def insert_restaurant_data():
    restaurant_data_list = LinkedList()
    for food_type in types:
        restaurant_sublist = LinkedList()
        for restaurant in restaurant_data:
            if restaurant[0] == food_type:
                restaurant_sublist.insert_beginning(restaurant)
        restaurant_data_list.insert_beginning(restaurant_sublist)
    return restaurant_data_list

my_food_list = insert_food_types()
my_restaurant_list = insert_restaurant_data()
favorites = LinkedList()
search_history = []

def sort_restaurants(restaurant_list, sort_by="rating"):
    restaurants = []
    head = restaurant_list.get_head_node()
    while head:
        restaurants.append(head.get_value())
        head = head.get_next_node()
    if sort_by == "rating":
        restaurants.sort(key=lambda x: float(x[3]), reverse=True)
    elif sort_by == "price":
        restaurants.sort(key=lambda x: float(x[2]))
    sorted_list = LinkedList()
    for restaurant in restaurants:
        sorted_list.insert_beginning(restaurant)
    return sorted_list

def display_restaurants(sublist_head):
    while sublist_head:
        print("--------------------------")
        print("Name: " + sublist_head.get_value()[1])
        print("Price: " + sublist_head.get_value()[2] + "/5")
        print("Rating: " + sublist_head.get_value()[3] + "/5")
        print("Address: " + sublist_head.get_value()[4])
        print("--------------------------\n")
        sublist_head = sublist_head.get_next_node()

def add_to_favorites(restaurant):
    favorites.insert_beginning(restaurant)
    print(f"{restaurant[1]} has been added to your favorites.\n")

def view_favorites():
    if favorites.get_head_node() is None:
        print("You have no favorite restaurants yet.\n")
    else:
        print("Your Favorite Restaurants:")
        display_restaurants(favorites.get_head_node())

def view_search_history():
    if not search_history:
        print("No search history available.\n")
    else:
        print("Your Search History:")
        for entry in search_history:
            print(entry)

def view_all_restaurants():
    restaurant_list_head = my_restaurant_list.get_head_node()
    while restaurant_list_head:
        display_restaurants(sort_restaurants(restaurant_list_head.get_value()).get_head_node())
        restaurant_list_head = restaurant_list_head.get_next_node()

selected_food_type = ""

# User interaction loop
while True:
    user_input = str(input(
        "\nWhat would you like to do?\n1. Search for restaurants by food type\n2. View all restaurants\n3. View favorite restaurants\n4. View search history\n5. Exit\nEnter your choice (1-5):\n")).lower()

    if user_input == '1':
        user_input = str(input(
            "\nWhat type of food would you like to eat?\nType the beginning of that food type and press enter to see if "
            "it's here.\n")).lower()
        
        search_history.append(user_input)

        # Search for user_input in food types data structure
        matching_types = []
        type_list_head = my_food_list.get_head_node()
        while type_list_head is not None:
            if str(type_list_head.get_value()).startswith(user_input):
                matching_types.append(type_list_head.get_value())
            type_list_head = type_list_head.get_next_node()

        # Print list of matching food types
        if matching_types:
            print("Matching food types:")
            for food in matching_types:
                print(food)
        else:
            print("No matching food types found. Please try again.")
            continue

        # Ask user to select food type if there are multiple matches
        if len(matching_types) > 1:
            selected_food_type = str(input("\nMultiple matches found. Please type the exact food type you want:\n")).lower()
        else:
            select_type = str(input(
                "\nThe only matching type for the specified input is " + matching_types[0] + ". \nDo you want to look at " +
                matching_types[0] + " restaurants? Enter y for yes and n for no\n")).lower()
            if select_type == 'y':
                selected_food_type = matching_types[0]
            else:
                continue

        # Retrieve and display restaurant data
        restaurant_list_head = my_restaurant_list.get_head_node()
        while restaurant_list_head:
            sublist_head = restaurant_list_head.get_value().get_head_node()
            if sublist_head and sublist_head.get_value()[0] == selected_food_type:
                sort_option = str(input("\nHow would you like to sort the restaurants? Enter 'rating' or 'price':\n")).lower()
                sorted_list = sort_restaurants(restaurant_list_head.get_value(), sort_by=sort_option)
                display_restaurants(sorted_list.get_head_node())
                
                # Allow user to add to favorites
                add_favorite = str(input("\nDo you want to add any of these restaurants to your favorites? Enter the name or 'n' for no:\n")).lower()
                if add_favorite != 'n':
                    sublist_head = sorted_list.get_head_node()
                    while sublist_head:
                        if sublist_head.get_value()[1].lower() == add_favorite:
                            add_to_favorites(sublist_head.get_value())
                            break
                        sublist_head = sublist_head.get_next_node()
                break
            restaurant_list_head = restaurant_list_head.get_next_node()

    elif user_input == '2':
        view_all_restaurants()

    elif user_input == '3':
        view_favorites()

    elif user_input == '4':
        view_search_history()

    elif user_input == '5':
        confirm_exit = str(input("\nAre you sure you want to exit? Enter y for yes and n for no:\n")).lower()
        if confirm_exit == 'y':
            print("Thank you for using Mustafa's Boston Restaurant Recommendations. Goodbye!")
            break
    else:
        print("Invalid choice. Please try again.")
