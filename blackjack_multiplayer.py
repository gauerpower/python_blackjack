import random
import os

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
        player = {'name': player_name, 'cash': start_money,'hand': [], 'score': 0, 'stand': False, 'bust': False, 'playing_this_round' : False}
        players.append(player)
    return players

def play_blackjack_multi(players):
    cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, "Ace", "Ace", "Ace", "Ace", "Jack", "Jack", "Jack", "Jack", "Queen", "Queen", "Queen", "Queen", "King", "King", "King", "King"]

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
    
    def display_score(l):
        for p in l:
            if p['playing_this_round']:
                print(f"\n{p['name']}'s hand is: {p['hand']}")

    def play_again(l):
        players_copy = l[:]
        answer = input("\nWould you like to play again? Y or N: ").lower()
        if answer == 'y':
            for p in players_copy:
                p['hand'] = []
                p['score'] = 0
                p['playing_this_round'] = False
                if round(float(p['cash']), 2) <= 0.0:
                    players_copy.remove(p)
                else:
                    p['stand'] = False
                    p['bust'] = False
            play_blackjack_multi(players_copy)
        elif answer == 'n':
            print("\nFinal score was:")
            for p in players_copy:
                print(f"{p['name']}: {p['cash']}")
            quit()
        else:
            print("\nInvalid input.")
            play_again(l)

    def check_for_blackjack(player):
        player['score'] = calculate_score(convert_face_cards(player['hand']))
        if player['score'] > 21:
            print(f"{player['name']} went over 21 and is out.")
            player['bust'] = True
            player['stand'] = True
            player['score'] = -1
        return player
    
    def compare_scores(l):
        players_copy = l[:]
        highest_score = 0
        highest_scorers = []
        for p in players_copy:
            p['score'] = calculate_score(convert_face_cards(p['hand']))
            if p['score'] > highest_score and p['bust'] == False and p['playing_this_round'] == True:
                highest_score = p['score']
        for p in players_copy:
            if p['score'] == highest_score:
                highest_scorers.append(p['name'])
        if len(highest_scorers) == 0:
            print("Nobody won this round. Pot split equally.")
            for p in players_copy:
                if p['playing_this_round']:
                    p['cash'] += bet
        if len(highest_scorers) == 1:
            print(f"\n{highest_scorers[0]} won with a score of {highest_score} and takes ${total}.")
            for p in players_copy:
                if p['name'] in highest_scorers:
                    p['cash'] += total
        else:
            print(f"\nDraw between {', '.join(highest_scorers)} with a score of {highest_score}.\nThey split the pot for a total of ${total / len(highest_scorers)} each.")
            for p in players_copy:
                if p['name'] in highest_scorers:
                    p['cash'] += total / len(highest_scorers)
        for p in players_copy:
            if p['cash'] <= 0.0:
                print(f"\n{p['name']} ran out of money and is out of the game.")
                players_copy.remove(p)
        if len(players_copy) < 2:
            print(f"\nGame over. {players_copy[0]['name']} won with a total of ${players_copy[0]['cash']}.")
            quit()
        else:
            play_again(players_copy)

    def set_bets(l):
        total = 0
        players_copy = l[:]
        print(f"\n{dealer} is the dealer.")
        bet_amount = 0
        while len([p for p in players_copy if len(p['hand']) >= 2]) < 2:
            bet_amount = float(input(f"\n{dealer}, how much do you want to bet? $"))
            while bet_amount > min([p['cash'] for p in players_copy if p['cash'] > 0]):
                print(f"\nCan't bet more than players have. Lowest amount is {min([p['cash']] for p in players_copy)}")
                bet_amount = float(input(f"\n{dealer}, how much do you want to bet?"))
            for p in players_copy:
                if p['name'] == dealer:
                    p['playing_this_round'] = True
                    continue
                agree_to_bet = input(f"{p['name']}, do you agree to bet {bet_amount}? Y or N: ").lower()
                while agree_to_bet not in ['y', 'n']:
                    agree_to_bet = input('Invalid input. Please enter Y or N: ').lower()
                if agree_to_bet == 'y':
                    p['playing_this_round'] = True
                elif agree_to_bet == 'n':
                    print(f"\n{p['name']} sits out this round.")
                    p['playing_this_round'] = False
            if len([p for p in players_copy if p['playing_this_round']]) >= 2:
                for p in players_copy:
                    if p['playing_this_round']:
                        for i in range(2):
                            p['hand'].append(deal_card())
                        p['cash'] -= bet_amount
                        total += bet_amount
                break
            else:
                print("\nCan't start the game if no one agrees to the bet.")
                for p in players_copy:
                    if p['name'] != dealer:
                        p['playing_this_round'] = False
                        p['stand'] = False
                        p['score'] = 0
        return [bet_amount, total, players_copy]

    dealer = random.choice(players)['name']
    for p in players:
        print(f"\n{p['name']} has a total of ${p['cash']}")

    [bet, total, players] = set_bets(players)

    for p in players:
        if p['playing_this_round']:
            print(f"{p['name']} is in.")
    print(f"Total pot is ${total}.")
    print(f"\nDealing cards...")

    while (all([p['stand'] for p in players if p['playing_this_round']]) == False) and len([p['bust'] for p in players if (p['playing_this_round'] == True and p['bust'] == False)]) > 1:
        display_score(players)
        for p in players:
            if len([p for p in players if (p['bust'] == False and p['playing_this_round'] == True)]) < 2:
                break
            if p['stand']:
                break
            if p['playing_this_round'] == True and p['bust'] == False:
                    hit_or_not = input(f"\n{p['name']}, your hand is {p['hand']}. Do you want to draw another card? Y or N: ").lower()
                    if hit_or_not not in ['y', 'n']:
                        hit_or_not = input("Invalid input. Please enter Y or N: ")
                    if hit_or_not == "y":
                        new_card = deal_card()
                        print(f"\nDealing {p['name']} a new card...\n\n{p['name']}'s new card is: {new_card}")
                        p['hand'].append(new_card)
                        p['score'] = calculate_score(convert_face_cards(p['hand']))
                        p = check_for_blackjack(p)
                    if hit_or_not == "n":
                        print(f"{p['name']} stands.")
                        p['stand'] = True
    
    compare_scores(players)