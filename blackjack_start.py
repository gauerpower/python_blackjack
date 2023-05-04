import blackjack_single_player
import blackjack_multiplayer

def start_game():
    print("\nWelcome to Blackjack. Aces are both high and low.")
    n = int(input("\nType '1' for single-player vs. computer, OR a number between 2-6 for multiplayer: "))
    if n == 1:
        blackjack_single_player.play_blackjack_single()
    elif n > 6:
        print("\nCan't have more than 6 players.")
        start_game()
    else:
        p = blackjack_multiplayer.create_players(n)
        blackjack_multiplayer.play_blackjack_multi(p)

start_game()