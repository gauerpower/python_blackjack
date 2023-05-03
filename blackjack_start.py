import blackjack_single_player
import blackjack_multiplayer

cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, "Ace", "Ace", "Ace", "Ace", "Jack", "Jack", "Jack", "Jack", "Queen", "Queen", "Queen", "Queen", "King", "King", "King", "King"]

def start_game():
    print("\nWelcome to Blackjack. Aces are both high and low.")
    n = int(input("Type '1' for single-player vs. computer, OR a number between 2-7 for multiplayer: "))
    if n == 1:
        blackjack_single_player.play_blackjack_single()
    elif n > 6:
        print("Can't have more than 6 players.")
    else:
        blackjack_multiplayer.play_blackjack_multi(n)