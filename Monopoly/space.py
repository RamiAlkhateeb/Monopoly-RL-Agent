from game_output import game_output

class Space:
    def __init__(self, name, cost, base_rent):
        self.name = name
        self.cost = cost
        self.base_rent = base_rent
        self.neighbours = []
        
    def __string__(self):
        return self.name
    
    def owner( self, state):
        for player in state.players:
            if self in player.properties(state):
                return player
        return None
    
    def occupants( self, state):
        return [ player for player in state.players 
                             if state.spaces[player.index] == self]
        
    def display(self, state):
        self.owner(state)
        if self.owner(state) != None:
            ownerstr = self.owner(state).name
        else:
            ownerstr = ""
        if self.set_owned(state):
            doublestr = "*"
        else:
            doublestr = " "

        occupantstr = ", ".join([str(x) for x in self.occupants(state)]) 
        game_output("| {:<18} | {:>4} | {:>4}{} | {:<5} | {:>4}".format(self.name, self.cost, self.rent(state), doublestr, ownerstr , occupantstr), end = "")
        
        #game_output("{}".format(occupantstr))
        
    def add_player(self, p):
        self.occupants.append(p)
        
    def remove_player(self, p):
        self.occupants.remove(p)
        
    def set_owned(self, state):
        owner = self.owner(state)
        if owner == None:
            return False
        for p in self.neighbours:
              if p.owner(state) != owner:
                  return False
        return True
        
    def rent(self, state):
        if self.set_owned(state):
            return self.base_rent * 2
        else:
            return self.base_rent
