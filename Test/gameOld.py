from gamestate import GameState
from strategy import Strategy
from player import Player
from game_output import game_output
import random     


class GameOld:
    
    def __init__(self, players, start_money, max_rounds):
        self.players = players
        self.start_money = start_money
        self.max_rounds = max_rounds
        self.num_players = len(players)
          
        self.state = GameState.startState(self)
        self.board = self.state.board
        for i in range(len(players)):
            players[i].game = self
            players[i].index = i
            players[i].opponents = players[i+1:].copy() + players[:i].copy()

        game_output("** ==== Leodopoly: the Leeds landlords game ==== **")
        
    def play(self, display="verbose"):
        self.state.display_state()
          
        while self.max_rounds == 0 or self.state.round <= self.max_rounds:
            result = self.state.progress(display)
            if self.state.phase == "bankrupcy":
                    
                game_output( result, " lost all money and now declared BANKRUPT!" )
                break
                
        game_output("\nThe final state of play:")      
        self.state.display_state()
                
        if  self.state.phase == "bankrupcy":
            game_output("\n* The game ended in round {} due to bankrupcy).".format(self.state.round))
        else:
            game_output("\n* End of game (the full {} rounds have been played).".format(self.max_rounds))
        losing_amount = min([player.heuristic(self.state) for player in self.players])
        winning_amount = max([player.money(self.state) for player in self.players])
        winners = [player for player in self.players if player.money(self.state) == winning_amount]
        losers = [player for player in self.players if player.heuristic(self.state) == losing_amount]
        if len(winners) == 1:
            winner = winners[0]
            game_output( "* The winner is {} with M {}.".format(winner.name, winning_amount))

        else:
            winners_str = ", ".join([winner.name for winner in winners])
            game_output( "* The winners are {}, who have M {}.".format(winners_str,winning_amount))
        return (winners , losers)
        
    def check_for_quit(self):
        key = input( "Press <return> to continue, or enter 'q' to quit: ")  
        if key == "q" or key == "Q":
            return True
        return False
  

############# Players, number of games, start money, number of rounds, game output    