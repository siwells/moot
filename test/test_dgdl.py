from dgdl import *
import unittest

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
        

if __name__ == '__main__':
    unittest.main()
