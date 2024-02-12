from space import Space
from game_output import game_output

class Board:    
    def __init__( self ):
       self.go =  Space("Go Square",   0,  0)
       ## HOMS
       wh1 = Space("Hamra Street",  60, 20)
       wh2 = Space("Hadara Street",  50, 12)
       wh3 = Space("Hamidya Street",  30, 8)
       ## Damascus 
       hp1 = Space("Maza Road", 200, 60)
       hp2 = Space("Barza Road", 120, 40)
       hp3 = Space("Bab toma Road", 250, 80)
       ## Aleepo
       h1  = Space("Hamadanya Street", 300,  2)
       h2  = Space("North Lane",    100,   50)
       
       ## Latakia
       e1 = Space("Zeraa/University", 700, 150)
       e2 = Space("8 of March", 200, 60)
       
       
       self.spaces = [ 
               self.go,
               wh1, wh2, wh3,
               e1,
               hp1, hp2, hp3,
               e2,
               h1, h2
             ]
       
       set1 = [wh1, wh2, wh3]
       set2 = [hp1, hp2, hp3]
       set3 = [h1,  h2]
       set4 = [e1,e2]
       self.sets = [set1, set2, set3, set4]
       self.num_spaces = len(self.spaces)
       for propset in self.sets:
           for prop in propset:
               #game_output(prop.name)
               prop.neighbours = propset.copy()
               prop.neighbours.remove(prop)
    
def test_neighbours():
     board = Board()
     for space in board.spaces:
         game_output("{}: {}".format(space.name, ", ".join([s.name for s in space.neighbours])))   