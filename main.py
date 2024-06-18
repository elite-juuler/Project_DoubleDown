import random

def Clubs(Deck):
    ClubList = []
    for x in Deck:
        x = str(x) + '♣'
        ClubList.append(x)
    return ClubList

def Diamonds(Deck):
    DiamondsList = []
    for x in Deck:
        x = str(x) + '♦'
        DiamondsList.append(x)
    return DiamondsList

def Hearts(Deck):
    HeartsList = []
    for x in Deck:
        x = str(x) + '♥'
        HeartsList.append(x)
    return HeartsList

def Spades(Deck):
    SpadesList = []
    for x in Deck:
        x = str(x) + '♠'
        SpadesList.append(x)
    return SpadesList

def create_deck(cardRanks):
    suits = ['♣', '♦', '♥', '♠']
    ranks = cardRanks
    # creates a list of dictionaries with keys 'rank' and 'suit'. 
    deck = [[str(rank) + suit] for suit in suits for rank in ranks]
    random.shuffle(deck)
    # print(deck)
    return deck

def card_value(card):
    # print(f"Card is: {card}")
    card = str(card)[2:-3]
    if card in ['2','3','4','5','6','7','8','9']:
        return int(card)
    elif card in ['10','J','Q','K']:
        return 10
    else: # Ace
        return 11

def next_card(shoe,currHand,currHandSum):
    pulled_card = shoe.pop()
    currHand.append(pulled_card)
    cardValue = card_value(pulled_card)
    return currHand, currHandSum + cardValue


def deal(deck): # gives the player then dealer a card 2x
    PlayerHand = []
    DealerHand = []
    shoe = deck
    PlayerHand, p1HandTotal = next_card(shoe,PlayerHand,0)
    DealerHand, dealerHandTotal = next_card(shoe,DealerHand,0)
    PlayerHand, p1HandTotal = next_card(shoe,PlayerHand,p1HandTotal)
    DealerHand, dealerHandTotal = next_card(shoe,DealerHand,dealerHandTotal)
    # p1HandTotal = card_value(PlayerHand) 
    # DealerHand.append(next_card(shoe))
    # dealerHandTotal = card_value(DealerHand)
    # print(f"DealerHand: {DealerHand} | Dealer total: {dealerHandTotal}")
    print(f"Dealer: {DealerHand[1]} | {card_value(DealerHand[1])}")
    print(f"PlayerHand: {PlayerHand} | {p1HandTotal}")
    return DealerHand, dealerHandTotal, PlayerHand,p1HandTotal

def player_hit(deck,PlayerHand,p1HandTotal):
    shoe = deck
    next_card(shoe,PlayerHand,p1HandTotal)
    return PlayerHand, p1HandTotal
    


# Main Program

cardRanks = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
deck = create_deck(cardRanks)

# deal(deck) 
DealerHand, dealerHandTotal, PlayerHand, p1HandTotal = deal(deck)

# give player another card from deck

print(f"PlayerHand: {PlayerHand} | {p1HandTotal}") # not tested yet
print("the end")

