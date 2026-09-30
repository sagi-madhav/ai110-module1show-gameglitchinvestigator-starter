from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

# --- Starter Tests (Preserved) ---

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


# --- AI-Assisted Verification Tests Targeting Fixed Bugs ---

def test_hint_messages_direction():
    """Verify hints tell player to go LOWER when guess is too high, and HIGHER when too low."""
    outcome_high, msg_high = check_guess(60, 50)
    assert outcome_high == "Too High"
    assert "LOWER" in msg_high.upper()

    outcome_low, msg_low = check_guess(40, 50)
    assert outcome_low == "Too Low"
    assert "HIGHER" in msg_low.upper()


def test_check_guess_mixed_types_no_lexicographical_bug():
    """Verify comparing single-digit 9 to double-digit 10 works as numeric, not string."""
    # Lexicographically, '9' > '10', but numerically 9 < 10
    outcome, _ = check_guess(9, "10")
    assert outcome == "Too Low"

    outcome2, _ = check_guess("9", 10)
    assert outcome2 == "Too Low"


def test_parse_guess_valid_and_whitespace():
    """Verify integers and leading/trailing whitespace are parsed correctly."""
    ok, val, err = parse_guess("  42  ")
    assert ok is True
    assert val == 42
    assert err is None


def test_parse_guess_invalid_and_empty():
    """Verify invalid strings, empty input, and None return appropriate error flags."""
    ok, val, err = parse_guess("")
    assert ok is False
    assert val is None
    assert "Enter a guess" in err

    ok, val, err = parse_guess("hello")
    assert ok is False
    assert val is None
    assert "not a number" in err


def test_parse_guess_decimal_handling():
    """Verify decimal numbers are either cleanly converted if integer-equivalent or rejected."""
    ok_int_float, val_int_float, _ = parse_guess("5.0")
    assert ok_int_float is True
    assert val_int_float == 5

    ok_dec, val_dec, err_dec = parse_guess("5.7")
    assert ok_dec is False
    assert "whole integer" in err_dec


def test_get_range_for_difficulty():
    """Verify difficulty ranges scale properly with Hard having the widest range."""
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 200)


def test_update_score_no_even_attempt_bonus_glitch():
    """Verify wrong guesses do not spuriously award +5 points on even attempt numbers."""
    initial_score = 50
    # Attempt 2 is even; buggy code awarded +5 points for Too High
    score_after_high = update_score(initial_score, "Too High", attempt_number=2)
    assert score_after_high < initial_score
    assert score_after_high == 45

    # Attempt 4 is even; verify Too Low deducts points properly
    score_after_low = update_score(initial_score, "Too Low", attempt_number=4)
    assert score_after_low == 45


def test_update_score_win():
    """Verify winning guess awards scaled points based on attempts used."""
    score = update_score(0, "Win", attempt_number=1)
    assert score == 90

    # Minimum score threshold
    score_late = update_score(0, "Win", attempt_number=15)
    assert score_late == 10
