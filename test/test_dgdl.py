from dgdl import *
import unittest

class TestGameFunctions(unittest.TestCase):
    def setUp(self):
        self.turns = Turns(size=12)
        self.roles = RoleList()
        self.part = Participants()
        self.white = Player("white")
        self.white_cstore = Store("cstore", "set", "public", self.white)
        self.black = Player("black")
        self.black_cstore = Store("cstore", "set", "public", self.black)

        self.rules = [ Rule(str(count)) for count in xrange(1,6) ]

        self.comp = Composition(self.turns, self.part, [self.black, self.white], [self.white_cstore, self.black_cstore], self.roles)
        self.game = Game("dgdl_simple", self.comp, self.rules)

    def test_fragment(self):
        out = self.game.fragment()
        self.assertEqual(out, "dgdl_simple{{turns, magnitude:12, ordering:strict}, {turns, magnitude:12, ordering:strict}, {players, min:2, max:undefined}, {player, id:black}, {player, id:white}, {store, id:cstore, owner:{white}, structure:set, visibility:public}, {store, id:cstore, owner:{black}, structure:set, visibility:public}, {{RULE1}, {RULE2}, {RULE3}, {RULE4}, {RULE5}}}")

class TestRoleListFunctions(unittest.TestCase):
    def setUp(self):
        self.rl1 = RoleList()
        self.rl2 = RoleList("speaker")
        self.rl3 = RoleList("speaker", "listener")

    def test_fragment(self):
        out = self.rl1.fragment()
        self.assertEqual(out, "{roles, {}}")

        out = self.rl2.fragment()
        self.assertEqual(out, "{roles, {speaker}}")

        out = self.rl3.fragment()
        self.assertEqual(out, "{roles, {speaker, listener}}")

class TestRuleFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def test_fragment(self):
        pass

class TestTurnFunctions(unittest.TestCase):
    def setUp(self):
        self.t1 = Turns()
        self.t2 = Turns(size="multiple")
        self.t3 = Turns(ordering="liberal")


    def test_fragment(self):
        out = self.t1.fragment()
        self.assertEqual(out, "{turns, magnitude:single, ordering:strict}")

        out = self.t2.fragment()
        self.assertEqual(out, "{turns, magnitude:multiple, ordering:strict}")

        out = self.t3.fragment()
        self.assertEqual(out, "{turns, magnitude:single, ordering:liberal}")        

if __name__ == '__main__':
    unittest.main()
