from board import Board
from game_output import game_output
import random


def resultOfTrade(state, seller, buyer, space, cost):
       newstate = state.clone()
       (newstate.properties[seller.index]).remove(space)
       (newstate.properties[buyer.index]).append(space)
       newstate.money[seller.index] += cost  
       newstate.money[buyer.index] -= cost  
       return newstate


def resultOfBuy(state, player, space, cost):
       newstate = state.clone()
       (newstate.properties[player.index]).append(space)
       newstate.money[player.index] -= cost
       return newstate
       



def auction(state, space, bid, players):
       player = players[0]
       if len(players) == 1:
          return (player, bid)
       if player.money(state) <= bid:
           game_output( player, "passes. (Not enough money to bid)")
           return auction(state, space, bid, players[1:])
       buy_result_state = resultOfBuy( state, player, space, bid)
       buy_value = player.heuristic(buy_result_state)
       op_buy_states = [ resultOfBuy( state, op, space, bid)
                             for op in player.opponents]
       op_buy_values = [player.heuristic(s) for s in op_buy_states]
       worst_op_buy_value = min( op_buy_values )
       if buy_value > worst_op_buy_value:
          rotate = players[1:].copy()
          rotate.append(player)
          game_output( "{} bids {}.".format(player, bid+10) )
          return auction( state, space, bid+10, rotate )
       else:
          game_output( player, "passes.")
          return auction(state, space, bid, players[1:])
  

### This function should return the highest offer in the range low--high (L-H) that a buyer
### of space can make to its owner and make a heuristic gain for at least the given margin

### (A) If a 0 payment does not make the gain margin gm then None is returned.
### (B) If the total money T available makes the margin this will be returned
### If neither (A) nor (B) hold then successively shrink the range by evaluating
### the gain at the midpoint.          
      
def highest_offer_giving_margin_gain(state, buyer, seller, space, margin):
         targetValue = buyer.heuristic(state) + margin
         result0 = resultOfTrade(state, seller, buyer, space, 0)
         result0value = buyer.heuristic(result0)
         if result0value < targetValue:
             return None
         allmoney = buyer.money(state)
         resultAll = resultOfTrade(state, seller, buyer, space, allmoney)
         resultAllvalue = buyer.heuristic(resultAll)
         if resultAllvalue >= targetValue:
            return allmoney 
         return highest_offer_in_range_meeting_target(state, buyer, seller, space, 
                                                          0, allmoney, targetValue)
         
def highest_offer_in_range_meeting_target(state, buyer, seller, space, low, high, targetValue):
         if low + 1 == high:
             return low
         mid = int( (low+high)/2 )
         resultMid = resultOfTrade(state, seller, buyer, space, mid)
         midValue = buyer.heuristic(resultMid)
         if midValue < targetValue:
             return highest_offer_in_range_meeting_target(state, buyer, seller, space, low, mid, targetValue)
         else:
             return highest_offer_in_range_meeting_target(state, buyer, seller, space, mid, high, targetValue)


class GameState:
   def __init__(self):
        pass
              
   @staticmethod  
   def startState( game ):
        gs = GameState()
        gs.game = game
        gs.board = Board()
        gs.players = game.players.copy()
        
        gs.positions = [0 for p in gs.players]
        gs.spaces = [gs.board.spaces[p] for p in gs.positions ]
        gs.money = [game.start_money for p in gs.players]
        gs.properties = [ [] for p in gs.players ]
       
        
        gs.round = 1
        gs.current_player_num = 0
        gs.phase = "turn start"
        gs.display = "verbose"
        return gs
        
   def clone( self ):
       newstate = GameState()
       
       newstate.game = self.game
       newstate.board = self.board
       newstate.players = self.players
       
       newstate.positions  = [x for x in self.positions]
       newstate.spaces     = [x for x in self.spaces]
       newstate.money      = self.money.copy()
       newstate.properties = [x.copy() for x in self.properties]
       
       newstate.round              = self.round 
       newstate.current_player_num = self.current_player_num
       newstate.phase              = self.phase
       newstate.display            = self.display
       return newstate
       
       
   ## Calcuate heursitic gain from player going from current state to newstate.
   ## Will be negative if heuristic value goes down.
   def gainFromStateChange( self, player, newstate):
       return player.heuristic(newstate) - player.heuristic(self)
       
   def occupants(self, space):
       occ_list = []
       for i in range(self.game.num_players):
           if self.spaces[i] == space:
               occ_list.append(self.players[i])
       return occ_list
            
   def display_state(self):
       game_output("-----------------------------------------------")
       game_output("| LOCATION           | COST | RENT  | OWNER   | OCCUPANTS" )
       game_output("|---------------------------------------------|" )
       for space in self.board.spaces:
            space.display(self)
       game_output("----------------------------------------------") 

       game_output("-----------------------------------------------")
       game_output("| NAME           | BALANCE | PROPERTIES  | TOTAL_RENT   | HEURISTIC" )
       game_output("|-------------------------------------------------------|" )
       for player in self.players:
            player.display(self)
    
   def display_phase(self):
       game_output("Round: {},  Player: {},  Phase: {} ({})".format(self.round,
                                                         self.current_player().name,
                                                         self.phase,
                                                         self.phase))   
       
   def current_player(self):
       return self.players[self.current_player_num]
   
   def progress(self, display="verbose"):
       player = self.current_player()
       game_output("Phase:", self.phase)
       #game_output("Phase:", self.phase)

       
       if self.phase == "round start":
          self.display_state()
          game_output( "Round", self.round)
          self.phase = "turn start"
          return
       
       if self.phase == "turn start":
          game_output( player, "to go.")
          if player.properties(self):
              self.phase = "opportunity to sell"
              return
          else:
              self.phase = "roll and move"
              return
      
       if self.phase == "opportunity to sell":
          game_output( player, "has the following properties for sale:")
          props_for_sale = player.properties(self)
          game_output( ", ".join([prop.name for prop in props_for_sale]))
          for prop in props_for_sale:
              offers = [(op, highest_offer_giving_margin_gain(self, op, player, prop, op.strategy.buy_margin))
                        for op in player.opponents]
              offers = [offer for offer in offers if offer[1] and offer[1] > 0]
              if offers == []:
                  game_output("No offers were made to buy {}.".format(prop.name))
    
              for op, offer in offers:
                  game_output( "*** {} offers M {} for {}.".format(op.name, offer, prop.name))
                  
              offer_result_states =  [ (op, offer, 
                                       resultOfTrade(self, player, op, prop, offer)) 
                                       for (op, offer) in offers ]
              offer_result_state_vals = [ (op, offer, result_state, 
                                           player.heuristic(result_state)) 
                                           for (op, offer, result_state) in offer_result_states] 
              
              acceptable_offer_result_state_vals = [ x for x in offer_result_state_vals if x[3] >= player.strategy.sell_margin]

              if acceptable_offer_result_state_vals == []:
                  if len(offers) > 1:
                     game_output(player, "does not accept any of these offers.")
                  else:
                     game_output(player, "does not accept any of this offer.")
                  continue
              
              if len(acceptable_offer_result_state_vals) > 1:
                 acceptable_offer_result_state_vals.sort(key=lambda x: x[3])  
              accepted_offer =  acceptable_offer_result_state_vals[-1]
              buyer = accepted_offer[0]
              amount = accepted_offer[1]
              game_output( "DEAL: {} agrees to sell {} to {} for M {}.".format(player.name, prop.name, buyer.name, amount ))
              
              
              #resultAllvalue = buyer.heuristic(resultAll)
              
          self.phase = "roll and move"
          return
       
       if self.phase == "roll and move":
          player = self.current_player()
          dice_num = random.randint(1,6)
          game_output( player.name, "rolls", str(dice_num)+"!" )
          self.positions[player.index] = (self.positions[player.index] + dice_num)%self.board.num_spaces
          new_space = self.board.spaces[self.positions[player.index]]
          self.spaces[player.index] =  new_space
        
          game_output( player.name, "moves to", new_space.name + "." )

          if new_space.cost == 0:
             game_output("This place cannot be bought.")
             self.phase = "end of turn"
             return
          if new_space.owner(self): ## someone already owns the space
             game_output("This property is owned by {}.".format(new_space.owner(self).name))
             if new_space.owner(self) == player:
                game_output("{} enjoys visiting {}.".format(player.name, new_space.name))
             else:    
                game_output( "{} must pay M {} to {}.".format(player, new_space.rent(self), new_space.owner(self).name) )
                player_money = self.money[player.index] 
                if player_money < new_space.rent(self): ## Player is knocked out!
                   #game_output("!!", player, "cannot pay and is knocked out of the game !!")
                   self.money[new_space.owner(self).index] += player_money
                   game_output( "{} gets M {} (all {}'s remaining money).".format(new_space.owner(self).name, player_money, player.name))
                   self.money[player.index] = 0
                   self.phase = "bankrupcy"
                   return player
                else:    
                   self.money[player.index] -= new_space.rent(self)
                   self.money[new_space.owner(self).index] += new_space.rent(self)
             self.phase = "end of turn"
             return
          else: ## the space is available to buy
             game_output("This property is for sale for {} M  Lira.".format(new_space.cost))
             if player.money(self) < player.space(self).cost:
                game_output( player.name, "cannot afford", player.space(self).name + "." )
                self.phase = "auction"
                return
             else:
                self.phase = "opportunity to buy" 
                return
       
       ### -------------- BUY PHASE            
       if self.phase == "opportunity to buy":   # buying phase
           player = self.current_player()
           space = player.space(self)

           buy_result_state = resultOfBuy( self, player, space, space.cost)
           buy_value = player.heuristic(buy_result_state)
           
           op_buy_states = [ resultOfBuy( self, op, space, space.cost)
                             for op in player.opponents]
           op_buy_values = [player.heuristic(s) for s in op_buy_states]
           worst_op_buy_value = min( op_buy_values ) 
           
           #game_output(player, "evaluates current state as:", player.heuristic(self) )
           #game_output(player, "evaluates the result of buying as:", result_value )
          
           #gain = self.gainFromStateChange( player, buy_result_state )
           #game_output("Heuristic gain from buying:", gain)
           
           ## if player.money(self) < space.cost + player.strategy.reserve: 
           #if gain < 0:
           if True or buy_value < worst_op_buy_value:
              game_output( player.name, "declines to buy", space.name + "." )
              self.phase = "auction"
              return
      
                    
       if self.phase == "auction":
           auction_space = self.spaces[player.index]
           start_index = player.index + 1
           game_output( auction_space.name, "is up for auction.")
           bid_order_players = self.players[start_index:].copy() + self.players[0:start_index].copy()
           winner, bid = auction( self, auction_space, 0, bid_order_players)
           game_output( "{} buys {} for {}.".format(winner, auction_space.name, bid)) 
           (self.properties[winner.index]).append(auction_space)
           self.money[winner.index] -=  bid
           self.phase = "end of turn"
           return
          
       if self.phase == "end of turn":
             if display == "verbose":
                self.display_state()
             self.current_player_num += 1
             self.phase = "turn start"
             if self.current_player_num == len(self.players):
                 self.current_player_num = 0
                 self.round += 1
                 self.phase = "round start"