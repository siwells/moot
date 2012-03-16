from dgdl import *

if __name__ == '__main__':
#    print "DGDL"
    
    turns = Turns(size=12)
    roles = RoleList()
    part = Participants()
    white = Player("white")
    white_cstore = Store("cstore", "set", "public", white)
    black = Player("black")
    black_cstore = Store("cstore", "set", "public", black)
    regulations = [ Regulation( str(count) ) for count in xrange(1,6) ]
    comp = Composition(turns, part, [black, white], [white_cstore, black_cstore], roles)
    moves = [Interaction("mv"+str(count), content = ["p","p","p","p"], opener="is it the case that") for count in xrange(1,6) ]
    
    game = Game("dgdl_simple", comp, regulations, moves)
 #   print game.fragment()
    
    
#    for mv in moves:
#        print mv.fragment()

    eff1 = Effect("update", "cstore", "black","p")
    print eff1.fragment()
    
    con1 = Condition("inspect", "in", "p", "cstore", "speaker")
    print con1.fragment()