# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
import unittest
from play import Player, Game

class RPGTests(unittest.TestCase):
    def test_separate_inventories(self):
        first, second = Player("A"), Player("B")
        first.inventory.append("Shield")
        self.assertNotIn("Shield", second.inventory)
    def test_multiple_level_ups(self):
        game = Game()
        game.player = Player("Tester", exp=195)
        from play import Enemy
        game.victory(Enemy("Dummy", 0, 0, 110, 0))
        self.assertEqual(game.player.level, 4)
        self.assertEqual(game.player.exp, 5)
    def test_health_cap(self):
        player = Player("Test")
        self.assertEqual(player.health, player.max_health)

if __name__ == "__main__":
    unittest.main()
