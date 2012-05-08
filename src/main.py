from dgdl import *

if __name__ == '__main__':
#    print "DGDL"
    """
    turns = Turns(size=12)
#    roles = RoleList()
    part = Participants()
    white = Player("white")
    white_cstore = Store("cstore", "set", "public", white)
    black = Player("black")
    black_cstore = Store("cstore", "set", "public", black)
    comp = Composition(turns, part, [black, white], [white_cstore, black_cstore])#, roles)
    
    
    regulations = [ Regulation( str(count) ) for count in xrange(1,6) ]
    
    
    moves = [Interaction("mv"+str(count), content = ["p","p","p","p"], opener="is it the case that") for count in xrange(1,6) ]
    
    game = Game("dgdl_simple", comp, regulations, moves)
#    print game.fragment()
    """
    
#    for mv in moves:
#        print mv.fragment()
    """
    print "###"

    eff1 = Effect("update", "cstore", "black","p")
    print eff1.fragment()
    
    con1 = Condition("inspect", "in", "p", "cstore", "speaker")
    print con1.fragment()
    
    rl2 = Rule(conditions=[con1], effects=[eff1])
    rl1 = Rule(effects=[eff1])
    print  rl1.fragment()
    
    rls1 = RuleExpr(rule_expr=[rl2, rl2])
    print rls1.fragment()    
    
    reg1 = Regulation("REG1", "movewise",rls1)
    print reg1.fragment()

    int1 = Interaction("ASSERT", ["p","q","r"], "It is the case that", rls1)
    print int1.fragment()
    """
    """
    system = System("TESTSYS")
    system.add_game(game)
    system.add_game(game)
#    system.print_system()
    """
    df = DescriptionFactory()
    desc = df.scaffold()
    print desc.description.fragment()