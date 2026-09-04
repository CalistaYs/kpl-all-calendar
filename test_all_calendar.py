import datetime as dt
import unittest

from ics_generator import build_calendar
from match_parser import is_legal_final_score, parse_matches
from validator import max_plausible_score, validate_matches


def raw_match(scheduleid, home, away, *, state=1, home_score=0, away_score=0):
    return {
        "scheduleid": scheduleid,
        "_season_id": "KPL2026S2",
        "match_time": "2026-07-03 20:00:00",
        "hname": home,
        "gname": away,
        "host_score": home_score,
        "guest_score": away_score,
        "match_state": state,
        "season": "2026年KPL夏季赛",
        "stage_name": "常规赛第一轮",
        "bo_total": 5,
        "region": "成都",
    }


class AllMatchesCalendarTest(unittest.TestCase):
    def test_even_bo_score_rules(self):
        self.assertEqual(2, max_plausible_score(2))
        self.assertTrue(is_legal_final_score(0, 2, 2))
        self.assertFalse(is_legal_final_score(1, 0, 2))

    def test_official_tbd_placeholder_is_allowed(self):
        raw = [raw_match("KPL2026S2M4", "待定", "待定")]
        matches, _ = parse_matches(raw, warn=lambda _: None)
        ok, errors, warnings = validate_matches(matches)
        self.assertTrue(ok, errors)
        self.assertTrue(warnings)

    def test_real_same_team_is_rejected(self):
        raw = [raw_match("KPL2026S2M5", "北京WB", "北京WB")]
        matches, _ = parse_matches(raw, warn=lambda _: None)
        ok, errors, _ = validate_matches(matches)
        self.assertFalse(ok)
        self.assertTrue(errors)

    def test_parser_keeps_matches_without_ag(self):
        raw = [raw_match("KPL2026S2M1", "重庆狼队", "北京WB")]
        matches, skipped = parse_matches(raw, warn=lambda _: None)
        self.assertEqual(0, skipped)
        self.assertEqual(1, len(matches))
        self.assertEqual("重庆狼队", matches[0]["home"])

    def test_calendar_uses_both_team_names(self):
        raw = [raw_match("KPL2026S2M2", "重庆狼队", "北京WB")]
        matches, _ = parse_matches(raw, warn=lambda _: None)
        text = build_calendar(
            matches,
            dtstamp=dt.datetime(2026, 7, 1, tzinfo=dt.timezone.utc),
        )
        self.assertIn("X-WR-CALNAME:KPL 全赛程日历", text)
        self.assertIn("SUMMARY:狼队 VS WB", text)
        self.assertIn("对阵：重庆狼队 vs 北京WB", text)

    def test_finished_score_stays_home_away_order(self):
        raw = [
            raw_match(
                "KPL2026S2M3", "重庆狼队", "北京WB",
                state=4, home_score=3, away_score=1,
            )
        ]
        matches, _ = parse_matches(raw, warn=lambda _: None)
        uid = "kpl-kpl2026s2m3@calistays.github"
        text = build_calendar(
            matches,
            existing_final_states={uid: {"score": (3, 1), "final": False}},
        )
        self.assertIn("最终比分：狼队 3 : 1 WB", text)
        self.assertIn("X-MATCH-FINAL-SCORE:YES", text)


if __name__ == "__main__":
    unittest.main()
