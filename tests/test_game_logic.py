from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


# ── check_guess ──────────────────────────────────────────────────────

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_check_guess_off_by_one_high():
    assert check_guess(51, 50) == "Too High"

def test_check_guess_off_by_one_low():
    assert check_guess(49, 50) == "Too Low"

def test_check_guess_boundary_low():
    assert check_guess(1, 1) == "Win"

def test_check_guess_boundary_high():
    assert check_guess(100, 100) == "Win"

def test_check_guess_returns_string_not_tuple():
    result = check_guess(50, 50)
    assert isinstance(result, str)


# ── get_range_for_difficulty ─────────────────────────────────────────

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_unknown_difficulty_defaults_to_normal():
    assert get_range_for_difficulty("Unknown") == (1, 100)

def test_empty_difficulty_defaults_to_normal():
    assert get_range_for_difficulty("") == (1, 100)


# ── parse_guess ──────────────────────────────────────────────────────

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_float_string_truncates():
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None

def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."

def test_parse_negative_number():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None

def test_parse_zero():
    ok, value, err = parse_guess("0")
    assert ok is True
    assert value == 0
    assert err is None

def test_parse_whitespace_only():
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


# ── update_score ─────────────────────────────────────────────────────

def test_score_win_first_attempt():
    # 100 - 10*(1+1) = 80
    assert update_score(0, "Win", 1) == 80

def test_score_win_late_attempt():
    # 100 - 10*(8+1) = 10; minimum is 10
    assert update_score(0, "Win", 8) == 10

def test_score_win_very_late_floors_at_10():
    # 100 - 10*(20+1) = -110, floored to 10
    assert update_score(0, "Win", 20) == 10

def test_score_too_high_subtracts():
    assert update_score(50, "Too High", 1) == 45

def test_score_too_high_even_attempt_still_subtracts():
    # Bug 5 fix: even attempts should NOT award +5
    assert update_score(50, "Too High", 2) == 45

def test_score_too_low_subtracts():
    assert update_score(50, "Too Low", 1) == 45

def test_score_unknown_outcome_unchanged():
    assert update_score(50, "Something Else", 1) == 50

def test_score_accumulates_across_rounds():
    score = 0
    score = update_score(score, "Too Low", 1)   # -5 → -5
    score = update_score(score, "Too High", 2)   # -5 → -10
    score = update_score(score, "Win", 3)         # 100 - 40 = 60 → 50
    assert score == 50


# ── Tests for off-by-one fix (attempts now start at 0) ──────────────

def test_score_win_zeroth_attempt():
    # With 0-based attempts: 100 - 10*(0+1) = 90
    assert update_score(0, "Win", 0) == 90

def test_score_from_100_wrong_guess_stays_positive():
    # Starting score of 100, wrong guess deducts 5
    assert update_score(100, "Too Low", 0) == 95

def test_score_from_100_win_first_attempt():
    # Starting at 100, win on attempt 0: 100 + (100 - 10) = 190
    assert update_score(100, "Win", 0) == 190

def test_check_guess_all_outcomes_are_strings():
    # Regression guard: all outcomes must be plain strings, not tuples
    for result in [check_guess(50, 50), check_guess(60, 50), check_guess(40, 50)]:
        assert isinstance(result, str)

def test_score_full_game_from_100():
    # Simulate a full game starting from score 100 with 0-based attempts
    score = 100
    score = update_score(score, "Too Low", 0)    # 100 - 5 = 95
    score = update_score(score, "Too High", 1)   # 95 - 5 = 90
    score = update_score(score, "Win", 2)         # 90 + (100 - 30) = 160
    assert score == 160


# ── Tests for invalid guesses not counting as attempts ───────────────

def test_parse_blank_rejects():
    # Blank input should be rejected so it never reaches attempt logic
    ok, value, err = parse_guess("")
    assert ok is False

def test_parse_none_rejects():
    ok, value, err = parse_guess(None)
    assert ok is False

def test_parse_non_numeric_rejects():
    ok, value, err = parse_guess("hello")
    assert ok is False

def test_parse_valid_allows():
    # Only valid parses should proceed to increment attempts
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
