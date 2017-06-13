import unittest
import RoyalFamily
import copy

skipTestGame = True


class MyTestCase(unittest.TestCase):

    def test_Rules_calculateWeight(self):
        s = RoyalFamily.State([1, 2, 3, 4], [1])
        r = RoyalFamily.Rules()
        t = s.getTuples(s.getGround())
        self.assertEqual(r.calculateWeight(t[0]), 1)
        t[0].append(0)
        with self.assertRaises(AssertionError):
            r.calculateWeight(t[0])

    def test_Rules_checkPossibleMove(self):
        r = RoyalFamily.Rules()
        t1 = [RoyalFamily.Chest]
        t2 = [0]
        self.assertTrue(r.checkPossibleMove(t1, t2))
        t1.append(RoyalFamily.Queen)
        self.assertFalse(r.checkPossibleMove(t1, t2))
        t2.append(RoyalFamily.King)
        self.assertTrue(r.checkPossibleMove(t2, t1))

    def test_State_Constructor(self):
        with self.assertRaises(TypeError):
            t = RoyalFamily.State()
        s = RoyalFamily.State([1, 2, 3], [2])
        sc = copy.deepcopy(s)
        self.assertEqual(s.getTower(), sc.getTower())
        self.assertEqual(s.getGround(), sc.getGround())

    def test_State_getTuples(self):
        testData = [[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
        s = RoyalFamily.State([1, 2, 3, 4], [1])
        self.assertEqual(s.getTuples(s.getTower()), testData)
        self.assertEqual(s.getTuples(s.getGround()), [[0, 1]])

    def test_State_getF(self):
        s = RoyalFamily.State([0, 10, 20], [0, 10])
        self.assertEqual(3, s.getF())

    @unittest.skip
    def test_rules_Move(self):
        basket1 = [[]]
        basket2 = [[]]
        rules = RoyalFamily.Rules()

        basket1[0].append(RoyalFamily.Chest)
        basket2[0].append(0)
        self.assertTrue(rules.checkPossibleMove(basket1[0], basket2[0]))

        basket1[0].append(RoyalFamily.Queen)
        self.assertFalse(rules.checkPossibleMove(basket1[0], basket2[0]))

        basket2[0].append(RoyalFamily.King)
        self.assertFalse(rules.checkPossibleMove(basket1[0], basket2[0]))

    def test_State_ExpandState(self):
        state = RoyalFamily.State([RoyalFamily.Queen, RoyalFamily.Prince, RoyalFamily.Chest], [RoyalFamily.King])
        t = state.expandState()

    def test_Game_Constructor(self):
        with self.assertRaises(TypeError):
            t = RoyalFamily.Game(None)
        t = RoyalFamily.Game()

    def test_Game_checkFinalState(self):
        g = RoyalFamily.Game()
        s1 = RoyalFamily.State([10], [])
        s2 = RoyalFamily.State([90, 50, 40], [30])
        self.assertFalse(g.checkFinalState(s1))
        self.assertFalse(g.checkFinalState(s2))
        s3 = RoyalFamily.State([], [RoyalFamily.King, RoyalFamily.Queen, RoyalFamily.Prince, RoyalFamily.Chest])
        self.assertTrue(g.checkFinalState(s3))

    def test_Game_parseWeight(self):
        g = RoyalFamily.Game()
        self.assertListEqual([], g.parseWeight([0, 5, 10, 20, RoyalFamily.King+10]))
        self.assertListEqual(['Prince', 'Queen'], g.parseWeight([0, 40, 10, 20, RoyalFamily.King + 10, 50]))

    def test_Game_victory(self):
        s = RoyalFamily.State([10, 50], [])
        sp = RoyalFamily.State([10], [50])
        s.setPrevious(sp)
        g = RoyalFamily.Game()
        g.victory(s)

    def test_Game_checkStateInList(self):
        g = RoyalFamily.Game()
        s1 = RoyalFamily.State([90, 50, 40], [30])
        l = [s1]
        self.assertFalse(g.checkStateInList(s1, []))
        self.assertTrue(g.checkStateInList(s1, l))

    @unittest.skipIf(skipTestGame, 'Game testing not yet')
    def test_Game_searchDepth(self):
        g = RoyalFamily.Game()
        g.searchDepth()

    @unittest.skipIf(skipTestGame, 'Game testing not yet')
    def test_INf(self):
        g = RoyalFamily.Game()
        g.searchInformed()

    @unittest.skipIf(skipTestGame, 'Game testing not yet')
    def test_Width(self):
        g = RoyalFamily.Game()
        g.searchWidth()


if __name__ == '__main__':
    unittest.main()
