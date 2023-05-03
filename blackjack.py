# Features to think about adding:
# Make a betting pot
# Make multiplayer possible (with player names)

import random
import os

cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, "Ace", "Ace", "Ace", "Ace", "Jack", "Jack", "Jack", "Jack", "Queen", "Queen", "Queen", "Queen", "King", "King", "King", "King"]

def play_blackjack():
    os.system('clear')
    print("\nWelcome to Blackjack. Aces are both high and low.")
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
            return 0
        elif (hand_total > 21) and (11 in numeric_cards):
            numeric_cards.remove(11)
            numeric_cards.append(1)
            hand_total = sum(numeric_cards)
        return hand_total
    
    def display_score():
        print(f"\nPlayer's hand is {user_cards}. Computer has {len(computer_cards)} cards, one of which is a {computer_cards[0]}.")

    def play_again():
        answer = input("\nWould you like to play again? Y or N: ").lower()
        if answer == 'y':
            play_blackjack()
        elif answer == 'n':
            print("\nGoodbye\n")
            quit()
        else:
            print("\nInvalid input.")
            play_again()

    def check_for_blackjack():
        user_score = calculate_score(convert_face_cards(user_cards))
        computer_score = calculate_score(convert_face_cards(computer_cards))
        if user_score > 21 and computer_score > 21:
            print("\nYou and the computer both went over 21. Draw.")
            play_again()
        elif user_score > 21:
            print(f"\nYou went over 21. Computer had {computer_score}. You lose.")
            play_again()
        elif computer_score > 21:
            print(f"\nComputer went over 21. You had {user_score}. You win.")
            play_again()
        else:
            return False
    
    def compare_scores():
        user_score = calculate_score(convert_face_cards(user_cards))
        computer_score = calculate_score(convert_face_cards(computer_cards))
        if user_score < computer_score:
            print(f"\nYou had {user_score} while computer had {computer_score}. You lose.")
            play_again()
        elif user_score > computer_score:
            print(f"\nYou had {user_score} while computer had {computer_score}. You win.")
            play_again()
        elif user_score == computer_score:
            print(f"\nYou and the computer both ended with {user_score}. Draw.")
            play_again()
        
    user_cards = []
    computer_cards = []
    print("\nDealing cards...")
    for _ in range(0, 2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())
    display_score()
    check_for_blackjack()

    while check_for_blackjack() == False:
        hit_or_not = input("\nDo you want to draw another card? Y or N: ").lower()
        os.system('clear')
        if hit_or_not == 'y':
            new_card = deal_card()
            print(f"\nDealing you a new card...\n\nYour new card is: {new_card}")
            user_cards.append(new_card)
        elif hit_or_not == 'n':
            compare_scores()
        else:
            print("\nInvalid input.")
            continue
        if calculate_score(computer_cards) < 17:
            print("\nDealing computer a new card...")
            computer_cards.append(deal_card())
        display_score()
        check_for_blackjack()

play_blackjack()
