import random
import time

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
    new_hand_sum = currHandSum + cardValue
    return currHand, new_hand_sum


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
    # print(f"Dealer: {DealerHand[1]} | {card_value(DealerHand[1])}")
    # print(f"PlayerHand: {PlayerHand} | {p1HandTotal}")
    return DealerHand, dealerHandTotal, PlayerHand,p1HandTotal

def dealer_check_hole_card(DealerHand,dealerHandTotal):
    print(f"Uh-oh, Dealer showing {card_value(DealerHand[1])}!")
    time.sleep(2.5)
    print("Checking hole card...")
    time.sleep(1)
    if dealerHandTotal == 21:
        print("Ouch! Dealer has Blackjack 😡")
        return "Home"
    else: 
        print("Whew, Dealer does not have Blackjack 😤")
        return "NotHome"

def offer_insurance(): # block that defines actions to take for players taking insurance
    # insurance offered here
    if input("Take insurance? Y/N: ") != "Y":
        return "N"
    else:
        return "Y"

def end_of_hand(): # block that defines actions to take based on final hand scores
    print(">>>Hand is over.")
    p1HandTotal = 0

def play_hand(deck,PlayerHand,p1HandTotal): # block of code that defines the playing of a hand
    while p1HandTotal <= 21:
        playerAction = input(f"Hand total: {p1HandTotal} - Hit or Stand? ")
        if playerAction == "Hit":
            PlayerHand, p1HandTotal = player_hit(deck,PlayerHand,p1HandTotal)
            print(f"PlayerHand: {PlayerHand}")
        else: # playerAction = STAND
            break
    if p1HandTotal > 21:
        print("BUST! You lose ☹")

def dealer_actions(): # block of code that defines what the dealer can do
    end_of_hand()

def player_hit(deck,PlayerHand,p1HandTotal):
    shoe = deck
    PlayerHand, p1HandTotal = next_card(shoe,PlayerHand,p1HandTotal)
    return PlayerHand, p1HandTotal
    
# Main Program

cardRanks = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
deck = create_deck(cardRanks)

# deal(deck) 
DealerHand, dealerHandTotal, PlayerHand, p1HandTotal = deal(deck)

print(f"Dealer: {DealerHand[1]} | {card_value(DealerHand[1])}") # dealer has a fair hand
print(f"PlayerHand: {PlayerHand} | {p1HandTotal}")

# Checking for Blackjack
# if Player dealt Blackjack
if p1HandTotal == 21: # if player's first two cards sum to 21:
    print("Blackjack!")
    time.sleep(1)
    if card_value(DealerHand[1]) == 10: # dealer shows 10, need to check for ace in hole
        if dealer_check_hole_card(DealerHand,dealerHandTotal) == "Home":
            # dealer and player have blackjack
            print("PUSH! At least it's not a loss...") 
    else: # Player has blackjack and dealer not showing a 10 
        print("YES! Player wins!")
        end_of_hand()

# p1 <> blackjack and dealer shows 10
elif card_value(DealerHand[1]) == 10:
    if dealer_check_hole_card(DealerHand,dealerHandTotal) == "Home":
        # dealer has blackjack
        end_of_hand() # not yet built out
    else:
        # neither player has blackjack
        play_hand(deck,PlayerHand,p1HandTotal)

# dealer showing Ace        
elif card_value(DealerHand[1]) == 11:
    insurance = offer_insurance()
    # no one takes insurance
    if insurance != "Y":
        if dealer_check_hole_card(DealerHand,dealerHandTotal) == "Home":
            #dealer has Ace-up blackjack
            end_of_hand()
        else: 
            # dealer does not have Ace-up blackjack
            play_hand(deck,PlayerHand,p1HandTotal)
    elif insurance != "Y": 
        print("[Insurance was taken]")
else: 
    play_hand(deck,PlayerHand,p1HandTotal)
