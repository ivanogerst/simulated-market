import random
import matplotlib.pyplot as plt
from functions import apply_inflation, negotiate_price


class Buyer:
    """ Buyer class representing the buyer's behavior in the negotiation process. """
    
    def __init__(self, max_price, expected_price):
        """ Initializes the buyer's attributes like maximum price, expected price, and surplus. """
        self.max_price = max_price  # Maximum price the buyer is willing to pay
        self.expected_price = expected_price  # The buyer's initial price expectation
        self.total_surplus = 0  # Buyer's total surplus
        self.days_without_buying = 0  # Days without any purchase

    def adjust_price(self, deal):
        """ Adjusts the buyer's expected price based on whether a deal was made. """
        if deal:
            # If a deal is made, adjust the expected price closer to the deal price
            self.expected_price += .3 * (deal - self.expected_price)
        else:
            # If no deal was made, randomly adjust the expected price upwards
            noise = random.uniform(-.01, .01)
            noise += 1.05
            self.expected_price *= noise
            self.expected_price *= random.uniform(0.95, 1.05)
        # Ensure the expected price doesn't exceed the maximum price the buyer is willing to pay
        if self.expected_price > self.max_price:
            self.expected_price = self.max_price

    def __str__(self):
        """ String representation of the buyer's information. """
        return f"\nMax price:\t{self.max_price}\nExpected price:\t{self.expected_price:.2f}\nSurplus:\t{self.total_surplus:.2f}\n"


class Seller:
    """ Seller class representing the seller's behavior in the negotiation process. """
    
    def __init__(self, min_price, expected_price):
        """ Initializes the seller's attributes like minimum price, expected price, and surplus. """
        self.min_price = min_price  # Minimum acceptable price for the seller
        self.expected_price = expected_price  # The seller's initial price expectation
        self.total_surplus = 0  # Seller's total surplus
        self.sold_today = False  # Indicates whether the seller made a sale today
        self.days_without_sale = 0  # Days without any sale

    def adjust_price(self, deal):
        """ Adjusts the seller's expected price based on whether a deal was made. """
        if deal:
            # If a deal is made, adjust the expected price closer to the deal price
            self.expected_price += .3 * (deal - self.expected_price)
        else:
            # If no deal was made, randomly adjust the expected price downwards
            noise = random.uniform(-.01, .01)
            noise += .95
            self.expected_price *= noise
            self.expected_price *= random.uniform(0.95, 1.05)
        # Ensure the expected price doesn't drop below the minimum price
        if self.expected_price < self.min_price:
            self.expected_price = self.min_price

    def __str__(self):
        """ String representation of the seller's information. """
        return f"\nMin price:\t{self.min_price}\nExpected price:\t{self.expected_price:.2f}\nSurplus:\t{self.total_surplus:.2f}\n"


def trading_day(sellers, buyers, seller_surplus, buyer_surplus):
    """ Simulates a single trading day with the interaction between sellers and buyers. """
    
    transactions = []  # List to store successful transactions
    
    # Shuffle sellers and buyers to ensure randomness in each iteration
    sellers_shuffled = sellers[:]
    buyers_shuffled = buyers[:]
    random.shuffle(sellers_shuffled)
    random.shuffle(buyers_shuffled)
    
    # Set all sellers' "sold_today" status to False at the start of the day
    for s in sellers_shuffled:
        s.sold_today = False
    
    # Try to match buyers with sellers for deals
    for b in buyers_shuffled:
        made_deal = False
        
        # Try to negotiate with each seller for the current buyer
        for s in sellers_shuffled:
            if not s.sold_today:
                price = negotiate_price(s, b)
                
                if price is not None:
                    # Calculate the surplus for both seller and buyer based on the negotiated price
                    seller_surplus += price - s.min_price
                    buyer_surplus += b.max_price - price
                    
                    # Update the total surplus for the specific seller and buyer
                    s.total_surplus += price - s.min_price
                    b.total_surplus += b.max_price - price
                    
                    # Adjust the expected prices based on the deal
                    s.adjust_price(price)
                    b.adjust_price(price)
                    
                    # Record the transaction
                    transactions.append((s, b, price))
                    
                    s.sold_today = True
                    made_deal = True
                    break
            
        # If the buyer couldn't make a deal, adjust their price expectations downward
        if not made_deal:
            b.adjust_price(False) 
            b.days_without_buying += 1
        else:
            b.days_without_buying = 0
            
    # After trying all buyers, update the sellers who didn't sell anything
    for s in sellers:
        if not s.sold_today:
            s.adjust_price(False)
            s.days_without_sale += 1
        else:
            s.days_without_sale = 0    
            
    return transactions


# Variables to track total surplus across the whole simulation
seller_surplus = 0
buyer_surplus = 0

# Lists to store all buyers and sellers (it's good practice to keep the number of buyers and sellers at least a digit off, so that unsatisfied buyers and unsold sellers don't exactly merge on the graph)
all_buyers = [Buyer(random.triangular(20, 60, 50), random.triangular(5, 50, 30)) for _ in range(104)]

all_sellers = [Seller(random.triangular(10, 50, 20), random.triangular(5, 55, 30)) for _ in range(105)]


avg_prices = []
unsold_sellers = []
unsatisfied_buyers = []   
seller_surplus_by_day = []
buyer_surplus_by_day = []

# Simulate x days of trading
def simulation(x, inflation_rate = None, avg_prices=[], seller_surplus=[], buyer_surplus=[], unsold_sellers=[], unsatisfied_buyers=[], seller_surplus_by_day=[], buyer_surplus_by_day=[]):
    
    for i in range(x):
            
        if inflation_rate:
            apply_inflation(all_sellers, all_buyers, base_rate = inflation_rate)
        
        seller_surplus = 0
        buyer_surplus = 0
        
        transactions = trading_day(all_sellers, all_buyers, seller_surplus, buyer_surplus)
        
        day_seller_surplus = 0
        day_buyer_surplus = 0

        # Calculate the total surplus for the day
        for s, b, price in transactions:
            day_seller_surplus += price - s.min_price
            day_buyer_surplus += b.max_price - price

        # Append the daily surplus values to the lists
        seller_surplus_by_day.append(day_seller_surplus)
        buyer_surplus_by_day.append(day_buyer_surplus)

        if transactions:
            avg_price = sum(price for _, _, price in transactions) / len(transactions)
        else:
            avg_price = None
            
        avg_prices.append(avg_price)
        unsold_sellers.append(sum(1 for s in all_sellers if not s.sold_today))
        unsatisfied_buyers.append(sum(1 for b in all_buyers if b.days_without_buying))
        



# Plotting functions
def show_average_price(avg_prices_local):
    """ Plot the average price by day. """
    plt.plot(avg_prices_local)
    plt.title("Average price by day")
    plt.xlabel('Day')
    plt.ylabel('Price')
    plt.show()


def show_surplus(seller_surplus_by_day, buyer_surplus_by_day):
    """ Plot the total surplus for sellers and buyers by day. """
    plt.plot(seller_surplus_by_day, label="Seller Surplus", color='blue')
    plt.plot(buyer_surplus_by_day, label="Buyer Surplus", color='green')
    plt.title("Total Surplus by Day")
    plt.xlabel('Day')
    plt.ylabel('Total Surplus')
    plt.legend()
    plt.show()
    
    
def show_unsatisfied(unsold_sellers, unsatisfied_buyers):
    """ Plot the number of unsold sellers and unsatisfied buyers by day. """
    plt.plot(unsold_sellers, label="Unsold Sellers", color='red')
    plt.plot(unsatisfied_buyers, label="Unsatisfied Buyers", color='orange')
    plt.title("Unsold Sellers and Unsatisfied Buyers by Day")
    plt.xlabel('Day')
    plt.ylabel('Count')
    plt.legend()
    plt.show()


# Call the plotting functions to display the results
simulation(180, inflation_rate=.00006, avg_prices=avg_prices, seller_surplus=seller_surplus, buyer_surplus=buyer_surplus, unsold_sellers=unsold_sellers, unsatisfied_buyers=unsatisfied_buyers, seller_surplus_by_day=seller_surplus_by_day, buyer_surplus_by_day=buyer_surplus_by_day)
show_average_price(avg_prices)
show_surplus(seller_surplus_by_day, buyer_surplus_by_day)
show_unsatisfied(unsold_sellers, unsatisfied_buyers)