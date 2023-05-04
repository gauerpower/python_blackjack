# Features to think about adding:
# Make a betting pot

#Playtest this to see if it works!

import random
import os

cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, "Ace", "Ace", "Ace", "Ace", "Jack", "Jack", "Jack", "Jack", "Queen", "Queen", "Queen", "Queen", "King", "King", "King", "King"]

def set_starting_cash():
    try:
        starting_cash = float(input("\nWhat is the buy-in amount? $"))
    except:
        print('Invalid input. Please enter a number.')
        set_starting_cash()
    return starting_cash

def create_players(num_of_players):
    start_money = set_starting_cash()
    players = []
    for i in range(0, num_of_players):
        player_name = input(f"Enter player {i + 1}'s name: ").title()
        player = {'name': player_name, 'cash': start_money,'hand': [], 'score': 0, 'stand': False, 'bust': False}
        players.append(player)
    return players

def play_blackjack_multi(players):
    os.system('clear')

    dealer = random.choice(players)['name']

    def set_bets():
        print(f"\n{dealer} is the dealer.")
        bet_amount = float(input(f"\n{dealer}, how much do you want to bet? $"))
        while bet_amount > min([p['cash'] for p in players if p['cash'] > 0]):
            print(f"Can't bet more than players have. Lowest amount is {min([p['cash']] for p in players)}")
            bet_amount = float(input(f"\n{dealer}, how much do you want to bet?"))
        return bet_amount

    def deal_card():
        chosen_card = random.choice(cards)
        cards.remove(chosen_card)
        return chosen_card
    
    def convert_face_cards(card_list):
        numeric_cards = card_list[:]
        for card in numeric_cards:
            if card in ['Jack', 'Queen', 'King']:
                numeric_cards.remove(card)
                numeric_cards.append(10)
            if card == 'Ace':
                numeric_cards.remove(card)
                numeric_cards.append(11)
        return numeric_cards

    def calculate_score(card_list):
        numeric_cards = convert_face_cards(card_list)
        hand_total = sum(numeric_cards)
        if (hand_total > 21) and (11 in numeric_cards):
            numeric_cards.remove(11)
            numeric_cards.append(1)
            hand_total = sum(numeric_cards)
        return hand_total
    
    def display_score():
        for p in players:
            if p['name'] == dealer:
                print(f"\n{p['name']} (dealer) has {len(p['hand'])} cards, one of which is {p['hand'][0]}.")
            elif len(p['hand']) > 0 :
                print(f"\n{p['name']}'s hand is: {p['hand']}")

    def play_again():
        answer = input("\nWould you like to play again? Y or N: ").lower()
        if answer == 'y':
            for p in players:
                p['stand'] = False
                p['bust'] = False
                p['hand'] = []
                p['score'] = 0
            play_blackjack_multi(players)
        elif answer == 'n':
            print("\nGoodbye\n")
            quit()
        else:
            print("\nInvalid input.")
            play_again()

    def check_for_blackjack(player):
        player['score'] = calculate_score(convert_face_cards(player['hand']))
        if player['score'] > 21:
            print(f"{player['name']} went over 21 and is out.")
            player['bust'] = True
            player['stand'] = True
        print(f'Remaining players: {", ".join([p["name"] for p in players if (p["bust"] == False and p["stand"] == False)])}')
    
    def compare_scores():
        if all([p['stand'] for p in players]) == True:
            print('\nAll players stand.')
        highest_score = 0
        highest_scorers = []
        for p in players:
            if p['score'] > highest_score and p['bust'] == False and len(p['hand']) > 0:
                highest_score = p['score']
        for p in players:
            if p['score'] == highest_score:
                highest_scorers.append(p['name'])
        if len(highest_scorers) == 1:
            print(f"\n{highest_scorers[0]} won with a score of {highest_score} and takes ${total}.")
            for p in players:
                if p['name'] in highest_scorers:
                    p['cash'] += total
        else:
            print(f"\nDraw between {', '.join(highest_scorers)} with a score of {highest_score}.\nThey split the pot for a total of ${total / len(highest_scorers)} each.")
            for p in players:
                if p['name'] in highest_scorers:
                    p['cash'] += total / len(highest_scorers)
        for p in players:
            if p['cash'] == 0:
                print(f"\n{p['name']} ran out of money and is out of the game.")
                players.remove(p)
        play_again()
    
    for p in players:
        print(f"\n{p['name']} has a total of ${p['cash']}")

    bet = set_bets()
    total = 0

    for p in players:
        if p['name'] == dealer:
            p['cash'] -= bet
            total += bet
            for i in range(2):
                p['hand'].append(deal_card())
            continue
        agree_to_bet = input(f"{p['name']}, do you agree to bet {bet}? Y or N: ").lower()
        while agree_to_bet not in ['y', 'n']:
            agree_to_bet = input('Invalid input. Please enter Y or N: ').lower()
        if agree_to_bet == 'n':
            print(f"{p['name']} sits out this round.")
            p['stand'] = True
            p['score'] = -1
        if agree_to_bet == 'y':
            p['cash'] -= bet
            total += bet
            for i in range(2):
                p['hand'].append(deal_card())
    
    print(f"\nDealing cards...")

    while (any([p['stand'] for p in players]) == False) and (any([p['bust'] for p in players]) == False):
        display_score()
        for p in players:
            if p['bust'] == False and len(p['hand']) > 0:
                hit_or_not = input(f"\n{p['name']}, your hand is {p['hand']}. Do you want to draw another card? Y or N: ").lower()
                if hit_or_not not in ['y', 'n']:
                    hit_or_not = input("Invalid input. Please enter Y or N: ")
                if hit_or_not == "y":
                    new_card = deal_card()
                    print(f"\nDealing {p['name']} a new card...\n\nYour new card is: {new_card}")
                    p['hand'].append(new_card)
                    p['score'] = calculate_score(convert_face_cards(p['hand']))
                    check_for_blackjack(p)
                if hit_or_not == "n":
                    p['stand'] = True
    
    compare_scores()
