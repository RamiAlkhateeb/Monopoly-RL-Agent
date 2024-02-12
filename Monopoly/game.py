from gamestate import GameState
from strategy import Strategy
from player import Player
from game_output import game_output
import random     
import matplotlib.pyplot as plt
import math 

class Game:
    
    def __init__(self  , players = None):
        if players is not None:
            self.players = players
        else:
            self.players = self.create_players()
        self.start_money = 500
        self.max_rounds = 10
        self.num_players = len(self.players)
        self.num_games = 5
        self.game_length = 16
        self.test_times = 10
        self.state = GameState.startState(self)
        self.board = self.state.board
        self.total_won_history = []
        for i in range(len(self.players)):
            self.players[i].game = self
            self.players[i].index = i
            self.players[i].opponents = self.players[i+1:].copy() + self.players[:i].copy()

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

    def test_game(self, test_players ):
        games_played = 0
        for player in test_players:
            player.games_won = 0 
            player.games_lost = 0

        while games_played < self.num_games:
            random.shuffle(test_players)
            game = Game( test_players)
            for player in test_players:
                player.total_games_played += 1
            (winners,losers) = game.play("no display")
            if len(winners) == 1: ## if there is a unique winner
                winners[0].games_won += 1
                winners[0].total_games_won += 1
                games_played += 1
            if len(losers) == 1: ## if there is a unique winner
                losers[0].games_lost += 1
        most_won = max([player.games_won for player in test_players])
        return [player for player in test_players if player.games_won == most_won]


    def plot_bar(self, players):
        plt.figure(figsize=(10, 6))
        plt.bar(list(players.keys()), list(players.values()))
        plt.title("players against each other")
        #ax.set_xlabel("X-axis")
        plt.ylabel("% of wins")
        plt.show()        


    def collaborative_player(self,players):
      
        first_phase = {}
        second_phase = [0,0,0,0,0,0,0,0]
        final_phase = []    

        for player in players:
            #won = player.total_games_won/player.total_games_played
            won = player.test_won
            #max_win = player.max_win_rate
            player_strategy_factors = player.strategy.strategy_factors()
            first_phase[player.name] = [won  * factor for factor in player_strategy_factors]

        for i in range(8): 
            for player in first_phase:
                currentPlayer = first_phase[player]
                second_phase[i] +=currentPlayer[i]
            final_phase.append(math.floor(second_phase[i] / self.test_times))

        return final_phase
    

    def min_regret_player(self, players, best_player):
        first_phase = {}   
        min_regret = 100000
        min_regret_player = players[0]

        for player in players:
            first_phase[player] = sum(player.strategy.strategy_factors())

        best_strategy_sum = sum(best_player.strategy.strategy_factors())

        for player in first_phase:
            if abs(best_strategy_sum - first_phase[player]) < min_regret:
                min_regret = abs(best_strategy_sum - first_phase[player]) 
                min_regret_player = player.strategy.strategy_factors()

        return min_regret_player
    

    def min_modified_regret_player(self, players):
    
        first_phase = {0:{} ,1:{},2:{},3:{},4:{},5:{},6:{},7:{} }
        second_phase = []

        for player in players:
            if player.total_games_played > 0:
                rate = player.total_games_won / player.total_games_played
                player_strategy_factors = player.strategy.strategy_factors()
                for i in range(8):
                    if player_strategy_factors[i] in first_phase[i]:
                        first_phase[i][player_strategy_factors[i]] += rate
                    else:
                        first_phase[i][player_strategy_factors[i]] = rate

        for factor_index in first_phase:
            Keymax = max(first_phase[factor_index], key= lambda x: first_phase[factor_index][x])
            second_phase.append(Keymax) 

        return second_phase


    def create_players(self):
        tight_strategy =  Strategy( 0,  1,  2,   10,   5,  500,  1000,   10000) #TIGHT BOUNDARY 
        greedy_strategy =  Strategy( 3, 0,  2,   50,  50,    0,  1200,   20000) #GREEDY BOUNDARY
        irrational_strategy =  Strategy( 0,   0,   0,    0,   0,   0,     0 ,   0    ) #IRRATIONAL BOUNDARY  
        random_strategy1 =  Strategy( 3,  0,  3,     10,  10,  100,   500,   10000) #RANDOM TESTER 1
        random_strategy2 =  Strategy( 2,  2,  3,   15,  15,  300,   500,   10000) #RANDOM TESTER 2
        random_strategy3 =  Strategy( 9,  0,    1,   20,  20,   0 ,   900,   20000) #RANDOM TESTER 3
        good_strategy =  Strategy( 3,  0,    0,   25, 25,   0 ,   1000,   20000) #good TESTER 4
        optimal_strategy =  Strategy( 3,  0,    1,   10,  10,   0 ,   900,   20000) #OPTIMAL STRATEGY

        tightPlayer = Player("Tight",  tight_strategy )
        irrationalPlayer   = Player("Irrational",   irrational_strategy )
        greedyPlayer   = Player("Greedy",   greedy_strategy )
        newbiePlayer1 = Player("Newbie1",   random_strategy1 )
        newbiePlayer2 = Player("Newbie2",   random_strategy2 )
        newbiePlayer3 = Player("Newbie3",   random_strategy3 )
        goodPlayer = Player("Good",   good_strategy )
        optimalPlayer = Player("Optimal",   optimal_strategy )

        players = [tightPlayer, irrationalPlayer , greedyPlayer , newbiePlayer1 , newbiePlayer2
               ,newbiePlayer3 , optimalPlayer , goodPlayer]
        
        return players
    


    def get_best_player(slef, best_players):
        if len(best_players) == 1:
            best_player = best_players[0]
        else:
            least_lost = min([player.games_lost for player in best_players])
            best_player = [player for player in best_players if player.games_lost == least_lost]
            best_player = best_player[0]
        return best_player


    def set_test_players(self, AI_Agent = None):
         if AI_Agent == None:
            return random.sample(self.players , 3)
         else:
            test_players = random.sample(self.players , 2)
            test_players.append(AI_Agent)
            return test_players


    def get_players_insights(self ,  num_episodes = None , AI_Agent = None ):
        if num_episodes == None:
            num_episodes = self.test_times
        for i in range(num_episodes):
            test_players = self.set_test_players(AI_Agent)
            best_players = self.test_game(test_players )
            best_player = self.get_best_player(best_players)

            best_player.set_max_win_rate(best_player.games_won/self.num_games)
            best_player.add_win_rate(best_player.games_won/self.num_games)
            best_player.test_won +=1
            players_percent = {}
            for player in test_players:
                players_percent[player.name] = (100 * player.games_won)/self.num_games

            #print("Test" , i+1 , "win rate:" ,players_percent , "and best player:" ,best_player )
        
        if AI_Agent != None:
            self.players.append(AI_Agent)
        player_total_won_policy = {}
        player_total_won = {}
        player_test_won = {}
        for player in self.players:
            if player.total_games_played > 0:
                win_rate = (player.total_games_won * 100)/(player.total_games_played)
                player_total_won[player.name] = win_rate
                player_total_won_policy[win_rate] = player.strategy.strategy_factors()
            player_test_won[player.name] = (player.test_won * 100)/( self.test_times)

        return (players_percent,player_total_won,player_test_won,player_total_won_policy)

    
    def get_best_strategies(self):
        players_insights = self.get_players_insights()
        best_player_name = self.players[0].name
        player_total_won = players_insights[1]
        player_test_won = players_insights[2]
        for player in self.players:
        
            if(player.name in player_total_won and player_total_won[player.name] > player_total_won[best_player_name]):
                best_player_name = player.name

        best_player = [player for player in self.players if player.name == best_player_name]
        print("players win rate in all games")
        self.plot_bar(player_total_won)
        print("players win rate in all tests")
        self.plot_bar(player_test_won)

        best_policy_collaborative = self.collaborative_player(self.players)
        best_policy_min_regret = self.min_regret_player(self.players, best_player[0])
        best_policy_min_modified_regret = self.min_modified_regret_player(self.players)

        print("collaborative_func strategy", best_policy_collaborative )
        print("min_regret_func strategy", best_policy_min_regret )
        print("min_modified_regret_func strategy", best_policy_min_modified_regret )

        print("Number of tests:" ,self.test_times , "number of games inside a test:" ,self.num_games )

        return [best_policy_collaborative , best_policy_min_regret , best_policy_min_modified_regret]


    def reset_players(self,players):
        for player in players:
            player.total_games_won = 0
            player.total_games_played = 0
            player.test_won = 0


    def get_key_by_value(self, my_dict, search_value):
        for key, value in my_dict.items():
            if value == search_value:
                return key
        return None

    def best_total_won_player(self,player_total_won):
        best_player_name = max(player_total_won, key=player_total_won.get)
        return [player for player in self.players if player.name == best_player_name]


    def evaluate_policy(self,best_policy, policy_name , num_episodes = None):
        print("Applying",policy_name,"policy:" , best_policy )
        AI_strategy =  Strategy(*best_policy) 
        if "RL" in policy_name:
            policy_name = "RL_Player"
        AI_Agent = Player(policy_name,   AI_strategy )
        self.players = self.create_players()
        #self.reset_players(self.players)
        
        players_insights= self.get_players_insights(num_episodes ,AI_Agent )

        if policy_name == "RL_Player":
            player_total_won = players_insights[1]
            self.total_won_history.append(player_total_won)

        return players_insights

    def get_final_result (self):
        RL_max_win_rate = self.total_won_history[0]["RL_Player"]
        final_win_rate = self.total_won_history[0]
        for win_rates in self.total_won_history:
            if win_rates["RL_Player"] > RL_max_win_rate:
                final_win_rate = win_rates
        
        self.visualize(final_win_rate, "RL_Player" )



    def visualize(self, player_total_won ,  agent_name = None , player_test_won = None ):
        print(agent_name , "player win rate in all games:",  player_total_won[agent_name] , "%")
        self.plot_bar(player_total_won)
        
        if player_test_won != None:
            print(agent_name , "player win rate in all test:",  player_test_won[agent_name] , "%")
            self.plot_bar(player_test_won)