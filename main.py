import random
import time

def create_deck(cardRanks):
    suits = ['♣', '♦', '♥', '♠']
    ranks = cardRanks
    # creates a list of dictionaries with keys 'rank' and 'suit'. 
    deck = [[str(rank) + suit] for suit in suits for rank in ranks]
    random.shuffle(deck)
    # print(deck)
    return deck

def card_value(card,currHandSum):
    # print(f"Card is: {card}")
    card = str(card)[2:-3]
    if card in ['2','3','4','5','6','7','8','9']:
        return int(card)
    elif card in ['10','J','Q','K']:
        return 10
    else:  
        return 11

def simplify_aces(currValues,currHandSum):
    for value in currValues:
        while currHandSum > 21:
            if value == 11:
                newVal = value - 10
                currValues[currValues.index(value)] = newVal 
                currHandSum -=10
            else: 
                break
    # print(currValues)
    return currValues, currHandSum

### not needed thanks to simplify_aces()
# def decrease_last_ace(hand,total,num_aces):# if 11 would bust, ace is 1
#     while num_aces > 0:
#         if total > 21:
#             total -=10
#         num_aces -= 1
#     return total

### not in use thanks to simplify_aces()
# def num_aces(hand): 
#     num_aces = sum(1 for card in hand if str(card)[2:-3] == 'A')
#     return num_aces

def displayValue(hand,currHandSum):
    if 11 in hand and currHandSum !=21:
        displayTotal = f"{currHandSum-10}/{currHandSum}"
    else: 
        displayTotal = currHandSum
    return displayTotal

def next_card(shoe,currHand,currValues,currHandSum):
    pulled_card = shoe.pop()
    currHand.append(pulled_card)
    cardValue = card_value(pulled_card,currHandSum)
    currValues.append(cardValue)
    currHandSum += cardValue
    # currHandSum = decrease_last_ace(currHand,currHandSum, 1 if cardValue == 11 else 0)
    if currHandSum > 21:
        currValues, currHandSum = simplify_aces(currValues,currHandSum)
    
    # values back to main program
    return currHand, currHandSum, currValues

def deal(deck): # gives the player then dealer a card 2x
    PlayerHand = []
    PlayerValues = []
    DealerHand = []
    DealerValues = []
    shoe = deck
    PlayerHand, playerHandTotal, PlayerValues = next_card(shoe,PlayerHand,PlayerValues,0)
    DealerHand, dealerTotal, DealerValues = next_card(shoe,DealerHand,DealerValues,0)
    PlayerHand, playerHandTotal, PlayerValues = next_card(shoe,PlayerHand,PlayerValues,playerHandTotal)
    DealerHand, dealerTotal, DealerValues = next_card(shoe,DealerHand,DealerValues,dealerTotal)
    return DealerHand, dealerTotal, DealerValues, PlayerHand, playerHandTotal, PlayerValues

def check_player_blackjack(playerHandTotal):
    if card_value(PlayerHand[0],playerHandTotal) + card_value(PlayerHand[1],playerHandTotal) == 21:
        return True
    else:
        return False

# check_dealer_blackjack - handles dealer showing 10 and dealer showing Ace
def check_dealer_blackjack(DealerHand,dealerTotal):
    if card_value(DealerHand[0],dealerTotal) == 10:
        print("Uh-oh, Dealer showing a 10!")
        time.sleep(1)
        print("Checking hole card...")
        time.sleep(1)
        if dealerTotal == 21:
            print("Ouch! Dealer has Blackjack 😡")
            print(f"Dealer: {DealerHand} | {displayValue(DealerHand,dealerTotal)}")
            return True
        else:
            print("Dealer does not have Blackjack.")
            return False
    elif card_value(DealerHand[0],dealerTotal) == 11: 
        print("Dealer showing an Ace!")
        time.sleep(1)
        offer_insurance()# offer insurance here
        time.sleep(1)
        if dealerTotal == 21:
            print("Ouch! Dealer has Blackjack 😡")
            return True
        else:
            print("Dealer does not have Blackjack.")
            return False

def offer_insurance(): # block that defines actions to take for players taking insurance
    # insurance offered here
    if input("Take insurance? Y/N: ") != "Y":
        return "N"
    else:
        return "Y"

def end_of_hand(dealerTotal,playerHandTotal): # block that compares scores and announces result.
    print(">>>Hand is over!")
    time.sleep(1)
    print(f"Dealer: {dealerTotal} | {DealerHand}")
    print(f"Player: {playerHandTotal} | {PlayerHand}")
    time.sleep(1)
    # if dealer busts or player > dealer
    if dealerTotal > 21 or (playerHandTotal > dealerTotal and playerHandTotal <= 21):
        print("You win!")
    elif dealerTotal == playerHandTotal:
        print("Push!")
    else:
        print("You lose, better luck next time!")
    # reset_hand() # not yet defined
    # playerHandTotal = 0

def play_hand(deck,PlayerHand,currValues,playerHandTotal,canDouble): # block of code that defines the playing of a hand
    while playerHandTotal <= 21:

        # CAN Double
        if canDouble == True:
            playerAction = input(f"Hand total: {displayValue(currValues,playerHandTotal)} - Hit/Stand/Double? ").lower()
            if ('h') in playerAction: # playerAction == HIT
                canDouble = False
                deck, PlayerHand, currValues, playerHandTotal = player_hit(deck,PlayerHand,currValues,playerHandTotal)
                print(f"Player: {PlayerHand} | {displayValue(currValues,playerHandTotal)}")
                time.sleep(1)
            elif ('s') in playerAction: # playerAction == STAND
                handAlive = True
                return deck, PlayerHand, playerHandTotal,canDouble==False,handAlive
            elif ('do') in playerAction: # playerAction == DOUBLE
                print("Doubley-Do! Good luck...")
                deck, PlayerHand, currValues, playerHandTotal = player_hit(deck,PlayerHand,currValues,playerHandTotal)
                time.sleep(1)
                print(f"Player: {PlayerHand} | {displayValue(currValues,playerHandTotal)}")
                time.sleep(1)
                if playerHandTotal <= 21:
                    handAlive = True
                    return deck, PlayerHand, playerHandTotal, canDouble==False,handAlive
                else: 
                    handAlive = False
                    return deck, PlayerHand, playerHandTotal, canDouble==False,handAlive
                
        
        # CANNOT Double
        elif canDouble == False: 
            playerAction = input(f"Hand total: {displayValue(currValues,playerHandTotal)} - Hit/Stand? ").lower()
            if ('h') in playerAction: # playerAction == HIT
                deck, PlayerHand, currValues, playerHandTotal = player_hit(deck,PlayerHand,currValues,playerHandTotal)
                print(f"Player: {PlayerHand} | {displayValue(currValues,playerHandTotal)}")
                time.sleep(1)
            elif ('s') in playerAction: # playerAction == STAND
                handAlive = True
                return deck, PlayerHand, playerHandTotal, canDouble==False, handAlive
    if playerHandTotal > 21:
        print("BUST!")
        handAlive = False
        return deck, PlayerHand,playerHandTotal, canDouble==False, handAlive


# dealer hitting actions for Stand 17 rule variations
def dealer_action_s17(deck,DealerHand,currValues,dealerTotal):
    print("Flipping dealer's hole card...")
    time.sleep(1)
    print(f"Dealer hand: {DealerHand} | {displayValue(DealerValues,dealerTotal)}")
    while dealerTotal < 17:
        print(f"Dealer has {dealerTotal}, dealer hits...")
        time.sleep(1)
        deck, DealerHand, currValues, dealerTotal = player_hit(deck,DealerHand,currValues,dealerTotal)
        print(f"Dealer hand: {DealerHand} | {displayValue(currValues,dealerTotal)}")
        time.sleep(1)
    if dealerTotal >= 17 and dealerTotal <= 21:
        # print(deck)
        # print(DealerHand)
        # print(dealerTotal)
        return deck, DealerHand, currValues, dealerTotal
    if dealerTotal > 21:
        print("Dealer BUSTS!")
        return deck, DealerHand, currValues, dealerTotal

# pulls card from shoe and appends it to player's hand
def player_hit(deck,PlayerHand,currValues,playerHandTotal):
    shoe = deck
    PlayerHand, playerHandTotal, currValues = next_card(shoe,PlayerHand,currValues,playerHandTotal)
    return deck, PlayerHand, currValues, playerHandTotal
    



### Main Program ###

cardRanks = [2,3,4,5,6,7,8,9,10,'J','Q','K','A'] # true deck
# cardRanks = [9,'A'] # test for Ace logic
deck = create_deck(cardRanks)

# deal cards to player and dealer
DealerHand, dealerTotal, DealerValues, PlayerHand, playerHandTotal, PlayerValues = deal(deck)

print(f"Dealer: {DealerHand[0]} | {card_value(DealerHand[0],dealerTotal)}") # dealer has a fair hand
print(f"Player: {PlayerHand} | {displayValue(PlayerValues,playerHandTotal)}")

PlayerBJ = check_player_blackjack(playerHandTotal)
DealerBJ = check_dealer_blackjack(DealerHand,dealerTotal)
time.sleep(1)

### Procedures for when someone has Blackjack ###

# player has blackjack, dealer does not
if PlayerBJ == True and DealerBJ != True:
    end_of_hand(dealerTotal,playerHandTotal)

# player AND dealer have blackjack
if PlayerBJ == True and DealerBJ == True:
    end_of_hand(dealerTotal,playerHandTotal)

# player does NOT have blackjack, but dealer DOES
if PlayerBJ != True and DealerBJ == True:
    end_of_hand(dealerTotal,playerHandTotal)

# neither player or dealer have blackjack
if PlayerBJ != True and DealerBJ != True:
    canDouble = True
    deck, PlayerHand, playerHandTotal,canDouble, handAlive = play_hand(deck,PlayerHand,PlayerValues,playerHandTotal,canDouble)
    if handAlive == True:
        deck,DealerHand,DealerValues,dealerTotal = dealer_action_s17(deck,DealerHand,DealerValues,dealerTotal)
        end_of_hand(dealerTotal,playerHandTotal)
    else:
        end_of_hand(dealerTotal,playerHandTotal)