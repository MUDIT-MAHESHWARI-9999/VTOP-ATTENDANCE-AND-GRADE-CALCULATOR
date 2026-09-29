import unittest
from src.calculator import AttendanceEngine, GradeEngine


class TestAttendanceEngine(unittest.TestCase):
    def test_safe_margin(self):
        res = AttendanceEngine.calculate_status(attended=32, total=40, target_pct=75.0)
        self.assertEqual(res["status"], "SAFE")
        self.assertEqual(res["margin"], 2)  # Can miss 2 classes (32/42 = 76.19%)

    def test_warning_margin(self):
        res = AttendanceEngine.calculate_status(attended=20, total=30, target_pct=75.0)
        self.assertEqual(res["status"], "WARNING")
        self.assertEqual(res["margin"], 10)  # Must attend 10 consecutive classes

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            AttendanceEngine.calculate_status(attended=10, total=0)


class TestGradeEngine(unittest.TestCase):
    def test_internal_calculation(self):
        score = GradeEngine.calculate_internal_score(cat1=40, cat2=40, da_quiz=25)
        # (40/50)*15 + (40/50)*15 + 25 = 12 + 12 + 25 = 49
        self.assertAlmostEqual(score, 49.0)

    def test_fat_requirements(self):
        reqs = GradeEngine.get_fat_requirements(internal_60=49.0)
        # S grade target 90 -> 41 needed weight -> (41/40)*100 = 102.5 -> Impossible (>100)
        self.assertEqual(reqs["S"]["status"], "Impossible")
        # A grade target 80 -> 31 needed weight -> (31/40)*100 = 77.5 -> 78
        self.assertEqual(reqs["A"]["fat_required"], 78)


if __name__ == "__main__":
    unittest.main()