import math


class AttendanceEngine:
    @staticmethod
    def calculate_status(attended: int, total: int, target_pct: float = 75.0) -> dict:
        if total <= 0:
            raise ValueError("Total classes must be greater than zero.")
        if attended < 0 or attended > total:
            raise ValueError("Attended classes must be between 0 and total classes.")

        current_pct = (attended / total) * 100

        if current_pct >= target_pct:
            bunks = math.floor((attended * 100 / target_pct) - total)
            return {
                "status": "SAFE",
                "current_pct": round(current_pct, 2),
                "margin": bunks,
                "message": f"You can safely miss {bunks} class(es)."
            }
        else:
            needed = math.ceil((target_pct * total - 100 * attended) / (100 - target_pct))
            return {
                "status": "WARNING",
                "current_pct": round(current_pct, 2),
                "margin": needed,
                "message": f"You need to attend {needed} consecutive class(es)."
            }


class GradeEngine:
    GRADE_TARGETS = {
        "S": 90,
        "A": 80,
        "B": 70,
        "C": 60,
        "D": 50
    }

    @staticmethod
    def calculate_internal_score(cat1: float, cat2: float, da_quiz: float) -> float:
        if not (0 <= cat1 <= 50 and 0 <= cat2 <= 50):
            raise ValueError("CAT marks must be between 0 and 50.")
        if not (0 <= da_quiz <= 30):
            raise ValueError("DA/Quiz score must be between 0 and 30.")

        cat1_weight = (cat1 / 50.0) * 15.0
        cat2_weight = (cat2 / 50.0) * 15.0
        return cat1_weight + cat2_weight + da_quiz

    @classmethod
    def get_fat_requirements(cls, internal_60: float) -> dict:
        results = {}
        for grade, target in cls.GRADE_TARGETS.items():
            needed_weight = target - internal_60
            fat_out_of_100 = (needed_weight / 40.0) * 100.0

            if fat_out_of_100 <= 0:
                results[grade] = {"fat_required": 0, "status": "Secured"}
            elif fat_out_of_100 > 100:
                results[grade] = {"fat_required": None, "status": "Impossible"}
            else:
                results[grade] = {"fat_required": math.ceil(fat_out_of_100), "status": "Achievable"}
        return results