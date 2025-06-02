import random     

def apply_inflation(sellers, buyers, base_rate=0.000055, noise_range=0.0005):
    for s in sellers:
        noise = random.uniform(-noise_range, noise_range)
        inflation_factor = 1 + base_rate + noise
        s.min_price *= inflation_factor
        s.expected_price *= inflation_factor
    
    for b in buyers:
        noise = random.uniform(-noise_range, noise_range)
        inflation_factor = 1 + base_rate + noise
        b.max_price *= inflation_factor
        b.expected_price *= inflation_factor



def negotiate_price(seller, buyer):
    """ Negotiates a price based on both the seller's and the buyer's expected prices. """
    
    seller_compliance = .9  # Seller's willingness to accept a lower price
    buyer_compliance = 1.1  # Buyer's willingness to pay a higher price
    
    # Start with the average of both parties' expected prices
    start_price = (seller.expected_price + buyer.expected_price) / 2
    # Introduce random noise to simulate negotiation variability
    noise = random.uniform(-.05, .05)
    price = start_price * (1 + noise)
    
    # Check if the negotiated price is acceptable to both parties
    if (price >= seller.min_price and price >= seller.expected_price * seller_compliance) and \
       (buyer.max_price >= price and price <= buyer.expected_price * buyer_compliance):
        return price
    else:
        return None