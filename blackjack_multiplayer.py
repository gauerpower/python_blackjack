# Features to think about adding:
# Make a betting pot

#Playtest this to see if it works!

import random
import os

cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, "Ace", "Ace", "Ace", "Ace", "Jack", "Jack", "Jack", "Jack", "Queen", "Queen", "Queen", "Queen", "King", "King", "King", "King"]

def play_blackjack_multiplayer(num_of_players):
    players = []
    dealer = ""
    for i in range(0, num_of_players):
        player_name = input(f"Enter player {i + 1}'s name: ").title()
        player = {'name': player_name, 'hand': [], 'score': 0, 'dealer' : True if i == 0 else False}
        if player['dealer'] == True:
            dealer = player['name']
        players.append(player)

    os.system('clear')

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
            elif card == 'Ace':
                numeric_cards.remove(card)
                numeric_cards.append(11)
        return numeric_cards

    def calculate_score(card_list):
        numeric_cards = convert_face_cards(card_list)
        hand_total = sum(numeric_cards)
        if hand_total == 21:
            return 21
        elif (hand_total > 21) and (11 in numeric_cards):
            numeric_cards.remove(11)
            numeric_cards.append(1)
            hand_total = sum(numeric_cards)
        return hand_total
    
    def display_score():
        for p in players:
            if p['dealer'] == True:
                print(f"{p['name']} (dealer) has {len(p['hand'])} cards, one of which is {p['hand'][0]}.")
            else:
                print(f"{p['name']}'s hand is: {p['hand']}")

    def play_again():
        answer = input("\nWould you like to play again? Y or N: ").lower()
        if answer == 'y':
            play_blackjack_multiplayer()
        elif answer == 'n':
            print("\nGoodbye\n")
            quit()
        else:
            print("\nInvalid input.")
            play_again()

    def check_for_blackjack():
        for p in players:
            p['score'] = calculate_score(p['cards'])
            if p['score'] > 21:
                print(f"{p['name']} went over 21 and is out.")
                del p
        print(f"Remaining players: {[p['name'] for p in players].join(', ')}")
    
    def compare_scores():
        highest_score = 0
        highest_scorers = []
        for p in players:
            if p['score'] > highest_score:
                highest_score = p['score']
        for p in players:
            if p['score'] == highest_score:
                p.append(highest_scorers)
        if len(highest_scorers) == 1:
            print(f"{highest_scorers[0]['name']} won with a score of {highest_score}.")
        else:
            print(f"Draw between {[p['name'] for p in players].join(', ')} with a score of {highest_score}")
        play_again()
            
    print(f"\n{dealer} is the dealer.\nDealing cards...")
    display_score()

    while len(players) > 1 or any([p['stand'] for p in players] == False):
        for p in players:
            hit_or_not = input(f"{p['name']}, your hand is {p['hand']}.\nDo you want to draw another card? Y or N: ").lower()
            if hit_or_not == "n":
                new_card = deal_card()
                print(f"\nDealing you a new card...\n\nYour new card is: {new_card}")
                p['hand'].append(new_card)
                p['score'] = calculate_score(p['hand'])
                check_for_blackjack()
            if hit_or_not == "n":
                p['stand'] = True
        display_score()
    
    compare_scores()

play_blackjack_multiplayer()
