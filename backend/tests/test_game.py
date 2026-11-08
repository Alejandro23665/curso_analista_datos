"""Pruebas de la motivación (XP, niveles, racha, logros), del repaso espaciado y de los ejercicios de lógica."""
import unittest
from datetime import date, timedelta

from app import game
from app import content

D = date(2026, 11, 2)


class XpTests(unittest.TestCase):
    def test_first_try_bonus_and_no_double_count(self):
        attempts = [(D, "a", True), (D, "a", True), (D, "b", False), (D, "b", True)]
        entries = game.xp_entries(attempts, [], [])
        doble = lambda ex: 2 if game.es_golpe_de_suerte(ex, D) else 1
        self.assertEqual([xp for _, xp, _ in entries], [15 * doble("a"), 10 * doble("b")])

    def test_golpe_de_suerte(self):
        self.assertEqual(game.es_golpe_de_suerte("x1", D), game.es_golpe_de_suerte("x1", D), "siempre igual para el mismo día")
        veces = sum(game.es_golpe_de_suerte("ej-%d" % i, D) for i in range(6000))
        self.assertTrue(800 < veces < 1200, "más o menos 1 de cada 6: %d" % veces)

    def test_theory_counts_once_per_topic(self):
        activities = [(D, "theory", "t1"), (D, "theory", "t1"), (D, "theory", "t2")]
        self.assertEqual(sum(xp for _, xp, _ in game.xp_entries([], activities, [])), 30)

    def test_events_and_skipped_break(self):
        events = [(D, "break_done"), (D, "break_skipped"), (D, "pomodoro"), (D, "review_ok"), (D, "challenge")]
        self.assertEqual(sum(xp for _, xp, _ in game.xp_entries([], [], events)), 20 + 8 + 25)

    def test_levels(self):
        self.assertEqual(game.level_info(0)["level"], 1)
        self.assertEqual(game.level_info(99)["level"], 1)
        self.assertEqual(game.level_info(100)["level"], 2)
        info = game.level_info(350)
        self.assertEqual((info["level"], info["into_level"], info["for_next"]), (3, 50, 300))


class StreakTests(unittest.TestCase):
    def days(self, *offsets):
        return {D - timedelta(days=o) for o in offsets}

    def test_today_not_done_does_not_break(self):
        self.assertEqual(game.streak_info(self.days(1, 2, 3), D)["current"], 3)

    def test_gap_without_freeze_breaks(self):
        self.assertEqual(game.streak_info(self.days(0, 2, 3), D)["current"], 1)

    def test_freeze_after_seven_days(self):
        active = self.days(*range(2, 9)) | {D}  # 7 días, un hueco ayer, hoy estudió
        info = game.streak_info(active, D)
        self.assertEqual(info["current"], 8)
        self.assertEqual(info["freezes"], 0)
        self.assertEqual(info["frozen_days"], [(D - timedelta(days=1)).isoformat()])

    def test_empty(self):
        self.assertEqual(game.streak_info(set(), D)["current"], 0)


class ReviewTests(unittest.TestCase):
    def test_new_attempt_comes_back_tomorrow(self):
        state = game.review_update(None, True, D)
        self.assertEqual((state["box"], state["due"]), (0, D + timedelta(days=1)))

    def test_correct_when_due_moves_up(self):
        state = game.review_update({"box": 0, "due": D, "lapses": 0, "reviews": 0}, True, D)
        self.assertEqual((state["box"], state["due"]), (1, D + timedelta(days=3)))

    def test_early_correct_changes_nothing(self):
        before = {"box": 2, "due": D + timedelta(days=4), "lapses": 0, "reviews": 1}
        self.assertEqual(game.review_update(before, True, D), before)

    def test_wrong_resets(self):
        state = game.review_update({"box": 3, "due": D, "lapses": 1, "reviews": 3}, False, D)
        self.assertEqual((state["box"], state["due"], state["lapses"]), (0, D + timedelta(days=1), 2))

    def test_daily_pick_is_stable(self):
        items = ["a", "b", "c", "d"]
        self.assertEqual(game.pick_daily(items, D), game.pick_daily(list(reversed(items)), D))
        self.assertIsNone(game.pick_daily([], D))


class AchievementTests(unittest.TestCase):
    def test_disciplined_days(self):
        events = [(D, "break_done")] * 4 + [(D - timedelta(days=1), "break_done")] * 4 + [(D - timedelta(days=1), "break_skipped")]
        self.assertEqual(game.disciplined_days(events), 1)

    def test_unlock(self):
        result = {a["key"]: a for a in game.achievements({"solved": 30})}
        self.assertTrue(result["ejercicios-25"]["unlocked"])
        self.assertFalse(result["ejercicios-100"]["unlocked"])
        self.assertEqual(result["ejercicios-100"]["value"], 30)


class NewExerciseKindTests(unittest.TestCase):
    def test_parsons(self):
        ex = {"id": "x", "kind": "parsons", "lines": ["a = 1", "b = 2", "print(a + b)"], "explanation": ""}
        blocks = content.public_exercise(ex)["blocks"]
        self.assertNotEqual([b["text"] for b in blocks], ex["lines"])
        self.assertNotIn("lines", content.public_exercise(ex))
        self.assertTrue(content.check_parsons(ex, [0, 1, 2])[0])
        correct, detail = content.check_parsons(ex, [1, 0, 2])
        self.assertFalse(correct)
        self.assertEqual(detail["first_wrong"], 0)
        self.assertFalse(content.check_parsons(ex, [0, 0, 2])[0])

    def test_predict(self):
        ex = {"id": "y", "kind": "predict", "answer": "1\n2", "explanation": "e"}
        self.assertTrue(content.check_predict(ex, "1  \r\n2\n")[0])
        self.assertFalse(content.check_predict(ex, "1 2")[0])
        self.assertNotIn("answer", content.public_exercise(ex))


if __name__ == "__main__":
    unittest.main()
