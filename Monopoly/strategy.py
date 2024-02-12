    
class Strategy:   
    def __init__(self, rm, opmm, oprm, bm, sm, reserve, reserve_penalty, ja):
        self.rent_mult = rm                # positive multiplier of total rent
        self.opponent_money_mult = opmm    # negative multiplier of total opponents' money
        self.opponent_rent_mult = oprm     # negative multiplier of total opponents' rent
        self.buy_margin = bm               # gain in heuristic required to buy property
        self.sell_margin = sm              # gain in heuristic required to sell property
        self.reserve = reserve                  # minimum reserve cash
        self.reserve_penalty = reserve_penalty  # negative applied if money lower than reserve 
        self.jeopardy_aversion = ja        # negative multiplier of jeopardy
          ## Jeopardy is calculated as the fraction of spaces owned by other plyers, whose
          ## rent is more than the players money.
        
    def strategy_factors(self):
        factors = [self.rent_mult 
                   ,self.opponent_money_mult
                   ,self.opponent_rent_mult 
                   ,self.buy_margin 
                   ,self.sell_margin 
                   ,self.reserve 
                   ,self.reserve_penalty 
                   ,self.jeopardy_aversion  ]
        return factors
            
    def heuristic(self, state, player):
        value = player.money(state) 
        value += player.total_rent(state) * player.strategy.rent_mult
        sum_of_opponents_money = sum( [opponent.money(state) for opponent in player.opponents] )
        value -= sum_of_opponents_money * self.opponent_money_mult
        sum_of_opponents_rent = sum( [opponent.total_rent(state) for opponent in player.opponents] )
        value -= sum_of_opponents_rent * self.opponent_rent_mult
          
        value -= player.jeopardy(state) * self.jeopardy_aversion
          
        if (player.money(state) < self.reserve):
              value -= self.reserve_penalty
          
        return value