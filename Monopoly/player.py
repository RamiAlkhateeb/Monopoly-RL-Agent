from game_output import game_output

def pounds(number):
    return "M " + str(number)

class Player:
      def __init__(self, name, strategy):
             self.name = name
             self.strategy = strategy
             self.game = None
             self.games_won = 0
             self.games_lost = 0
             self.total_games_won = 0
             self.total_games_played = 0
             self.test_won = 0
             self.max_win_rate = 0
             self.win_rates = []
             self.index = None
             
      
      def display(self, state):
          game_output( "| {:<14} | {:>6} | {:>11} | {:>12}| ({})".format( self.name+":", 
                                                   pounds(self.money(state)),
                                                   len(self.properties(state)),
                                                   pounds(self.total_rent(state)),
                                                   int(self.heuristic(state))
                                                 ) )
    
      def money(self,state):
          return state.money[self.index]
          
      def position(self,state):
          return state.positions[self.index]
          
      def space(self,state):
          return state.spaces[self.index]
        
      def set_max_win_rate(self , new_win_rate):
        if new_win_rate > self.max_win_rate:
            self.max_win_rate = new_win_rate
            
      def add_win_rate(self , new_win_rate):
        self.win_rates.append(new_win_rate)
            
          
      def properties(self,state):
          #game_output("*state.properties", state.properties)
          return state.properties[self.index]
    
      def heuristic(self, state):
          return self.strategy.heuristic(state, self)
    
                    
      def __str__(self):
          return self.name
      
      def __repr__(self):
          return self.name 
          
      def owns(self, space):
          return space in self.properties  
        
      def total_rent(self, state):
          return sum( [prop.rent(state) for prop in self.properties(state) ] )
      
      ## The jeopardy of a player in a given state is the fraction of spaces on
      ## the board, which if the player landed on they would lose (because rent
      ## higher than their total money).
      def jeopardy(self, state):
          deadly = 0
          for space in self.game.board.spaces:
              if ( space.owner(state) != self
                   and
                   space.rent(state) > self.money(state)
                 ):
                 deadly += 1
          return deadly / len(self.game.board.spaces) 
      