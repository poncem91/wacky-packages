import numpy as np
import csv

# ---------------------------------------------
# CSCI 127, Joy and Beauty of Data      
# Program 5: Wacky Packages
# Mariafe Ponce      
# Last Modified: November 13, 2019               
# ---------------------------------------------
# Program reads from a 'Wacky Packages' csv file
# and loads the series' information into an instance
# of the WackyPackageSeries class called my_collection.
# Then it reads from another csv file and updates
# my_collection with the number of cards already owned.
# Program is able to print the collection's info
# in a readable format, is also able to calculate the
# total value of the owned collection, the amount
# of cards missing to complete the collection, and
# how much it would cost to complete it.
#
# HONOR'S ADDITION: The program also lets user sell
# cards they already own and use the money earned
# from selling them to buy other cards
# ---------------------------------------------

class WackyPackageSeries:
    """ constructor initializes object with manufacturer, year, number of items (how_many)
        and creates a np array of 1 row, and how_many columns, each cell with enough
        space to fit a WackyPackageCard object """
    def __init__(self, manufacturer, year, how_many):
        self.manufacturer = manufacturer
        self.year = year
        self.how_many = how_many
        self.cards = np.ndarray(how_many, dtype=WackyPackageCard)
        self.cash_value = 0

    """ creates desired formatted string output """
    def __str__(self):
        output = "My {} collection of {} Wacky Packages\n\n".format(self.year, self.manufacturer)
        output += "Number    Description                   Value     Owned\n"
        output += "------    -----------                   -----     -----\n"
        # itirates over every item in np array and uses each object's instance str method
        for item in self.cards:
            output += str(item) + "\n"
        return output

    """ opens csv file, iterates over every line in csv file and
        adds an object instance of WackyPackageCard with the csv file line's
        values into each index in the np array"""
    def read_series_information(self, file):
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0 # keeps index count to access each np array item in self.cards
            for line in csv_reader:
                self.cards[line_count] = WackyPackageCard(int(line[0]), line[1], float(line[2]))
                line_count += 1
                
    """ opens csv file and iterates over every line, reformats line to match
        series information, and adds one to np array object's cards_owned every
        time it appears on the np array object's description"""            
    def read_collection_information(self, file):
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                reformatted_line = " ".join(line[0].split()).lower() # gets rid of weird cases and extra spaces
                for card in self.cards:
                    if card.get_description().lower() == reformatted_line: # compares lower case of both
                        card.set_cards_owned(card.get_cards_owned() + 1) # updates cards_owned count
                        break # breaks out of loop if card was already found

    """ iterates over every card in collection, checks for each if cards_owned is 0,
        if so update count and update cost. Returns two values"""
    def determine_missing_information(self):
        missing_cards_count = 0
        missing_cards_cost = 0
        for card in self.cards:
            if card.get_cards_owned() == 0:
                missing_cards_count += 1
                missing_cards_cost += card.get_value()
        return missing_cards_count, missing_cards_cost

    """ iterates over every card in collection, access each card's value,
        multiply that by cards_owned and add result to total"""
    def collection_value(self):
        total = 0
        for card in self.cards:
            total += (card.get_value() * card.get_cards_owned())
        return total

    """ prompts user to see if they want to buy or sell a card, asks which card
        they wish to buy/sell, and calls the buy_card_update or sell_card_update
        methods accordingly """
    def buy_sell(self):
        print("Your current funds are: ${:.2f}".format(self.cash_value))
        user_continue = ""
        # prompts user until valid input is entered
        while user_continue.lower() != "y" and user_continue.lower() != "n":
            user_continue = input("Would you like to buy or sell a card? (Y/N): ")
        if user_continue.lower() == "y":
            card = ""
            sell_or_buy = ""
            while card == "": # prompts user until card name is entered
                card = input("Which card would you like to buy or sell? ")
            # prompts user until valid input is entered
            while sell_or_buy.lower() != "s" and sell_or_buy.lower() != "b":
                sell_or_buy = input("Would you like to Sell or Buy? (S/B): ")
            if sell_or_buy.lower() == "s":
                self.sell_card_update(card)
            else:
                self.buy_card_update(card)
        else:
            pass

    """ checks if card is available to sell, if so, updates collection,
        updates cash fund amount, and prints new updated collection.
        if card is not available, prints message saying so """
    def sell_card_update(self, card_description):
        reformatted_description = " ".join(card_description.split()).lower()
        card_avail = False
        for card in self.cards: # iterates over every card in collection
            if card.get_description().lower() == reformatted_description: # checks if card in collection
                if card.get_cards_owned() > 0: # checks if user owns card
                    card_avail = True
                    card.set_cards_owned(card.get_cards_owned() - 1) # updates cards owned
                    self.cash_value += card.get_value() # updates cash value funds
                    print("\nYou have sold {}\n".format(card.get_description()))
                    print("Your updated Collection is:\n")
                    print(self)
                    self.buy_sell()
                else:
                    break
        if not card_avail:
            print("You do not have that card to sell")
            self.buy_sell()
        
    """ checks if enough funds are available to buy desired card and checks if
        card exists in collection, if either situation is not successful it
        prints message saying there's an error.
        If there are enough funds and card exists, collection is update and
        cash value funds are updated. Then updated collection is printed """
    def buy_card_update(self,card_description):
        card_avail = False
        if self.cash_value == 0:
            print("You do not have enough funds to buy this card")
            self.buy_sell()
        else:
            reformatted_description = " ".join(card_description.split()).lower()
            for card in self.cards: # iterates over every card in collection
                if card.get_description().lower() == reformatted_description: # checks if card in collection
                    card_avail = True
                    if card.get_value() <= self.cash_value: # checks if enough funds
                        card.set_cards_owned(card.get_cards_owned() + 1) # updates cards_owned
                        self.cash_value -= card.get_value() # updates cash value funds
                        print("\nYou have bought {}\n".format(card.get_description()))
                        print("Your updated Collection is:\n")
                        print(self)
                        self.buy_sell()
                    else:
                        print("You do not have enough funds to buy this card")
                        self.buy_sell()
                    break
            if not card_avail:
                print("Card does not exist to buy")
                self.buy_sell()
                
# ---------------------------------------------

class WackyPackageCard:
    def __init__(self, number, description, value):
        self.number = number
        self.description = description
        self.value = value
        self.cards_owned = 0

    def __str__(self):
        return "{:<10d}{:25}{:10.2f}{:10d}".format(self.number, self.description, self.value, self.cards_owned)

    def get_number(self):
        return self.number

    def get_description(self):
        return self.description

    def get_value(self):
        return self.value

    def get_cards_owned(self):
        return self.cards_owned

    def set_cards_owned(self, number):
        self.cards_owned = number

# ---------------------------------------------

def main():
    my_collection = WackyPackageSeries("Topps", 1973, 30)
    my_collection.read_series_information("series1.csv")
    print(my_collection)
    my_collection.read_collection_information("mycards.csv")
    print(my_collection)
    print("Value of collection = ${:.2f}".format(my_collection.collection_value()))
    number_of_missing_cards, cost_of_missing_cards = my_collection.determine_missing_information()
    print("Number of missing cards =", number_of_missing_cards)
    print("Cost of purchasing missing cards = ${:.2f}".format(cost_of_missing_cards))
    my_collection.buy_sell()
    
# ---------------------------------------------

main()
