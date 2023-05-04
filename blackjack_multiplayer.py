# Features to think about adding:
# Make a betting pot

#Playtest this to see if it works!

import random
import os

cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, "Ace", "Ace", "Ace", "Ace", "Jack", "Jack", "Jack", "Jack", "Queen", "Queen", "Queen", "Queen", "King", "King", "King", "King"]

def create_players(num_of_players):
    players = []
    for i in range(0, num_of_players):
        player_name = input(f"Enter player {i + 1}'s name: ").title()
        player = {'name': player_name, 'hand': [], 'score': 0, 'stand': False, 'bust': False}
        players.append(player)
    return players

def play_blackjack_multi(players):
    os.system('clear')

    dealer = random.choice(players)['name']

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
        print(numeric_cards)
        hand_total = sum(numeric_cards)
        if (hand_total > 21) and (11 in numeric_cards):
            numeric_cards.remove(11)
            numeric_cards.append(1)
            hand_total = sum(numeric_cards)
        return hand_total
    
    def display_score():
        for p in players:
            if p['bust'] == True:
                print(f"{p['name']} is out.")
            else:
                if p['name'] == dealer:
                    print(f"\n{p['name']} (dealer) has {len(p['hand'])} cards, one of which is {p['hand'][0]}.")
                else:
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

    def check_for_blackjack():
        for p in players:
            p['score'] = calculate_score(convert_face_cards(p['hand']))
            if p['score'] > 21:
                print(f"{p['name']} went over 21 and is out.")
                p['bust'] = True
                p['stand'] = True
        print(f'Remaining players: {", ".join([p["name"] for p in players if p["bust"] == False])}')
    
    def compare_scores():
        if all([p['stand'] for p in players]) == True:
            print('\nAll players stand.')
        highest_score = 0
        highest_scorers = []
        for p in players:
            if p['score'] > highest_score and p['bust'] == False:
                highest_score = p['score']
        for p in players:
            if p['score'] == highest_score:
                highest_scorers.append(p['name'])
        if len(highest_scorers) == 1:
            print(f"\n{highest_scorers[0]} won with a score of {highest_score}.")
        else:
            print(f"\nDraw between {', '.join(highest_scorers)} with a score of {highest_score}")
        play_again()
    
    for p in players:
        for i in range(2):
            p['hand'].append(deal_card())
    print(f"\n{dealer} is the dealer. Dealing cards...")
    display_score()

    while (any([p['stand'] for p in players]) == False) and (any([p['bust'] for p in players]) == False):
        for p in players:
            if p['bust'] == False and p['stand'] == False:
                hit_or_not = input(f"\n{p['name']}, your hand is {p['hand']}. Do you want to draw another card? Y or N: ").lower()
            if hit_or_not == "y":
                new_card = deal_card()
                print(f"\nDealing {p['name']} a new card...\n\nYour new card is: {new_card}")
                p['hand'].append(new_card)
                p['score'] = calculate_score(convert_face_cards(p['hand']))
                check_for_blackjack()
            if hit_or_not == "n":
                p['stand'] = True
        os.system('clear')
        display_score()
    
    compare_scores()
