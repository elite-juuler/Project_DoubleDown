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

def card_value(card):
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

def displayValue(handValues,currHandSum):
    if 11 in handValues and currHandSum !=21:
        displayTotal = f"{currHandSum-10}/{currHandSum}"
    else: 
        displayTotal = currHandSum
    return displayTotal

def next_card(shoe,currHand,currValues,currHandSum):
    pulled_card = shoe.pop()
    currHand.append(pulled_card)
    cardValue = card_value(pulled_card)
    currValues.append(cardValue)
    currHandSum += cardValue
    # currHandSum = decrease_last_ace(currHand,currHandSum, 1 if cardValue == 11 else 0)
    if currHandSum > 21:
        currValues, currHandSum = simplify_aces(currValues,currHandSum)
    
    # values back to main program
    return currHand, currHandSum, currValues

def deal(deck,list_playerHands): # gives each player a card, then dealer a card 2x
    DealerHand = []
    DealerValues = []
    shoe = deck
    
    # each player first card
    for thisHand in list_playerHands:
        # PlayerHand = []
        # PlayerValues = []
        thisHand['cards'], thisHand['handTotal'], thisHand['handValues'] = next_card(shoe,thisHand['cards'], thisHand['handValues'],0)

    # dealer 1st card    
    DealerHand, dealerTotal, DealerValues = next_card(shoe,DealerHand,DealerValues,0)
        
    # each player second card
    for thisHand in list_playerHands:
        thisHand['cards'], thisHand['handTotal'], thisHand['handValues'] = next_card(shoe,thisHand['cards'], thisHand['handValues'],thisHand['handTotal'])
    
    # dealer 2nd card
    DealerHand, dealerTotal, DealerValues = next_card(shoe,DealerHand,DealerValues,dealerTotal)
    # print(list_playerHands)
    # for i in range(handsToDeal):
    #     list_playerHands = list_playerHands.append[
    #         {'index': handsToDeal.index(i),'hand': PlayerHand, 'handValues': PlayerValues, 'handTotal': playerHandTotal}
    #     ]
    return DealerHand, dealerTotal, DealerValues

def check_player_blackjack(currentPlayer): # checks if player has blackjack and adds to dictionary
    if card_value(currentPlayer['cards'][0]) + card_value(currentPlayer['cards'][1]) == 21:
        currentPlayer['hasBJ'] = True
        # return True
        return currentPlayer
    else:
        # return False
        currentPlayer['hasBJ'] = False
        return currentPlayer
    

# check_dealer_blackjack - handles dealer showing 10 and dealer showing Ace
def check_dealer_blackjack(DealerHand,dealerTotal):
    if card_value(DealerHand[0]) == 10:
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
    elif card_value(DealerHand[0]) == 11: 
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

def end_of_hand(dealerTotal,DealerHand,list_playerHands): # block that compares scores and announces result.
    print(">>>Hand is over!")
    time.sleep(1)
    print(f"Dealer: {dealerTotal} | {DealerHand}")
    for player in list_playerHands:
        if dealerTotal > 21 or (player['handTotal'] > dealerTotal and player['handTotal'] <=21):
            print(f"Player{player['index']+1}: {player['handTotal']} | WIN {player['cards']}")
        elif dealerTotal == player['handTotal']:
            print(f"Player{player['index']+1}: {player['handTotal']} | PUSH {player['cards']}")
        else:
            print(f"Player{player['index']+1}: {player['handTotal']} | LOSS {player['cards']}")
        time.sleep(1)
    # if dealer busts or player > dealer
    # if dealerTotal > 21 or (playerHandTotal > dealerTotal and playerHandTotal <= 21):
    #     print("You win!")
    # elif dealerTotal == playerHandTotal:
    #     print("Push!")
    # else:
    #     print("You lose, better luck next time!")
    # reset_hand() # not yet defined
    # playerHandTotal = 0

def get_player_decision(player):        
        # first two cards
        if len(player['cards']) == 2:
            if str(player['cards'][0])[2:-3] == str(player['cards'][1])[2:3]:
                # player has pair, can split
                playerAction = input(f"Player{player['index']+1} hand total: {displayValue(player['handValues'], player['handTotal'])} - Hit/Stand/Double/Split? ").lower()
                if ('h') in playerAction: 
                    decision = "Hit"
                elif ('st') in playerAction:
                    decision = "Stand"
                elif ('do') in playerAction:
                    decision = "Double"
                elif ('sp') in playerAction:
                    decision = "Split"
                return decision
            else: # player does not have a pair, cannot split
                playerAction = input(f"Player{player['index']+1} hand total: {displayValue(player['handValues'], player['handTotal'])} - Hit/Stand/Double? ").lower()
                if ('h') in playerAction: 
                    decision = "Hit"
                elif ('st') in playerAction:
                    decision = "Stand"
                elif ('do') in playerAction:
                    decision = "Double"
                return decision
            
        else: # player has more than 2 cards, cannot split or double
            playerAction = input(f"Player{player['index']+1} hand total: {displayValue(player['handValues'], player['handTotal'])} - Hit/Stand? ").lower()
            if ('h') in playerAction: 
                decision = "Hit"
            elif ('st') in playerAction:
                decision = "Stand"
            return decision


def play_hand(deck,player): # block of code that defines the playing of a hand
    
    while player['handTotal'] <= 21:

        action = get_player_decision(player)
        if action == "Hit":
            deck, player = player_hit(deck,player)
            print(f"Player {player['index']+1}: {player['cards']} | {displayValue(player['handValues'],player['handTotal'])}")
            time.sleep(1)
        elif action == "Stand":
            player['handAlive'] = True
            return deck, player
        elif action == "Double":
            print("Doubley-Do! Good luck...")
            time.sleep(1)
            # deck, PlayerHand, currValues, playerHandTotal = player_hit(deck,PlayerHand,currValues,playerHandTotal)
            deck, player = player_hit(deck,player)
            print(f"Player {player['index']+1}: {player['cards']} | {displayValue(player['handValues'],player['handTotal'])}")
            time.sleep(1)
            if player['handTotal'] <= 21:
                player['handAlive'] = True
                return deck, player
            else: 
                player['handAlive'] = False
                return deck, player
        elif action == "Split":
            print("Splitting hands, good luck!")
            time.sleep(1)
            split_hand(deck,player)
            break
       
    if player['handTotal'] > 21:
        print("BUST!")
        player['handAlive'] = False
        return deck,player


# dealer hitting actions for Stand 17 rule variations
def dealer_action_s17(deck,DealerHand,currValues,dealerTotal):
    print("Flipping dealer's hole card...")
    time.sleep(1)
    print(f"Dealer hand: {DealerHand} | {displayValue(DealerValues,dealerTotal)}")
    while dealerTotal < 17:
        print(f"Dealer has {dealerTotal}, dealer hits...")
        time.sleep(1)
        DealerHand, dealerTotal, currValues = next_card(deck,DealerHand,currValues,dealerTotal)
        print(f"Dealer hand: {DealerHand} | {displayValue(currValues,dealerTotal)}")
        time.sleep(1)
    if dealerTotal >= 17 and dealerTotal <= 21:
        return deck, DealerHand, currValues, dealerTotal
    if dealerTotal > 21:
        print("Dealer BUSTS!")
        return deck, DealerHand, currValues, dealerTotal

# pulls card from shoe and appends it to player's hand
def player_hit(deck,player):
    shoe = deck
    player['cards'], player['handTotal'], player['handValues'] = next_card(shoe,player['cards'],player['handValues'],player['handTotal'])
    return deck, player
    

# split hands
def split_hand(deck,player):
    hand1 = []
    hand1Values = []
    hand1.append(playerHand[0])
    hand1Values.append(card_value(hand1[0]))
    hand1Sum = card_value(hand1[0])
    hand2 = []
    hand2Values = []
    hand2.append(playerHand[1])
    hand2Values.append(card_value(hand2[0]))
    hand2Sum = card_value(hand2[0])
    shoe = deck
    hand1,hand1Total,hand1Values = next_card(shoe,hand1,hand1Values,hand1Sum)
    hand2,hand2Total,hand2Values = next_card(shoe,hand2,hand2Values,hand2Sum)
    print(f"Player Hand1: {hand1} | {displayValue(hand1Values,hand1Total)}")
    print(f"Player Hand2: {hand2} | {displayValue(hand2Values,hand2Total)}")

    splitted_hands = [    
        {'hand': hand1, 'handValues': hand1Values, 'handTotal': hand1Total},
        {'hand': hand2, 'handValues': hand2Values, 'handTotal': hand2Total}
    ]

    for split in splitted_hands:
        shoe = shoe
        PlayerHand = split['hand']
        currValues = split['handValues']
        playerHandTotal = split['handTotal']
        play_hand(shoe,PlayerHand,currValues,playerHandTotal)
        

        # global "playerHandTotal" is not being updated, need way to exit loop of play_hand
        # ADD print functions for (hand1 result: score)
    
    # return activeHands,hand1,hand1Total,hand1Values,hand2,hand2Total,hand2Values
        # needs to return expected values for what is calling this



### Main Program ###

numberOfPlayers = int(input(f"How many players this hand? " ))
keys = ['index','cards','handValues','handTotal']
list_playerHands = []
for i in range(numberOfPlayers):
    playerHand = {}
    for key in keys:
        if key == 'index':
            playerHand[key] = i
        elif key == 'cards':
            playerHand[key] = []
        elif key == 'handValues':
            playerHand[key] = []
        elif key == 'handTotal':
            playerHand[key] = 0
    list_playerHands.append(playerHand)

cardRanks = [2,3,4,5,6,7,8,9,10,'J','Q','K','A'] # true deck
# cardRanks = [9,'6'] # test for Ace logic
deck = create_deck(cardRanks)

# deal cards to player and dealer
DealerHand, dealerTotal, DealerValues = deal(deck,list_playerHands)

print(f"Dealer: {DealerHand[0]} | {card_value(DealerHand[0])}") # dealer has a fair hand
for player in list_playerHands:
    print(f"Player {player['index']+1}: {player['cards']} | {displayValue(player['handValues'],player['handTotal'])}")

# check for player blackjacks
for player in list_playerHands:
    PlayerBJ = check_player_blackjack(player)
    
# check for dealer blackjack
DealerBJ = check_dealer_blackjack(DealerHand,dealerTotal)

### Procedures for when someone has Blackjack ###

# player has blackjack, dealer does not
for player in list_playerHands:
    if player['hasBJ'] == True and DealerBJ != True:
        # ADD code for the following
            list_playerHands.remove(player)
            # add winnings to player
        # end_of_hand(dealerTotal,playerHandTotal)

# player AND dealer have blackjack
    if player['hasBJ'] == True and DealerBJ == True:
        continue
        # ADD code for the following
            # result is a PUSH
        # end_of_hand(dealerTotal,playerHandTotal)

# player does NOT have blackjack, but dealer DOES
    if player['hasBJ'] != True and DealerBJ == True:
    # ADD code for the following
        # result is a loss for player
        # subtract wager from player
        end_of_hand(dealerTotal,player)
        

# neither player or dealer have blackjack
for player in list_playerHands:

    if player['hasBJ'] != True and DealerBJ != True:
        deck, player = play_hand(deck,player)

        # if playerhandAlive == True:
        #     deck,DealerHand,DealerValues,dealerTotal = dealer_action_s17(deck,DealerHand,DealerValues,dealerTotal)
        #     end_of_hand(dealerTotal,playerHandTotal)
        # else:
        #     end_of_hand(dealerTotal,playerHandTotal)

# see if dealer needs to hit (hands alive?)
if sum(1 for players in list_playerHands if players.get('handAlive') == True) > 0:
    deck,DealerHand,DealerValues,dealerTotal = dealer_action_s17(deck,DealerHand,DealerValues,dealerTotal)

end_of_hand(dealerTotal,DealerHand,list_playerHands)