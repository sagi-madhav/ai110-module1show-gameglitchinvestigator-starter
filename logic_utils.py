class GuessResult(tuple):
    """
    A tuple subclass (outcome, message) that also compares directly to the outcome string.
    This satisfies both:
      - outcome, message = check_guess(guess, secret)
      - assert check_guess(guess, secret) == "Too High"
    """
    def __new__(cls, outcome: str, message: str):
        return super().__new__(cls, (outcome, message))

    @property
    def outcome(self) -> str:
        return self[0]

    @property
    def message(self) -> str:
        return self[1]

    def __eq__(self, other):
        if isinstance(other, str):
            return self[0] == other
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIXME: Logic breaks here - starter code set Hard range (1-50) smaller than Normal (1-100)
    # FIX: Refactored logic into logic_utils.py with proper ranges (Easy: 1-20, Normal: 1-100, Hard: 1-200)
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIXME: Logic breaks here - starter code silently truncated float guesses without feedback
    # FIX: Refactored validation into logic_utils.py with robust whitespace and type checks
    if raw is None:
        return False, None, "Enter a guess."

    raw_clean = str(raw).strip()
    if raw_clean == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw_clean:
            float_val = float(raw_clean)
            if float_val.is_integer():
                return True, int(float_val), None
            return False, None, "Please enter a whole integer, not a decimal."

        value = int(raw_clean)
        return True, value, None
    except ValueError:
        return False, None, "That is not a number."


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIXME: Logic breaks here - starter code had inverted hints (Go HIGHER when guess > secret)
    # and failed with TypeError / lexicographic comparison on mixed str/int types.
    # FIX: Refactored into logic_utils.py using GuessResult, normalized to int, fixed hints to point in correct direction.
    try:
        g = int(guess)
        s = int(secret)
    except (ValueError, TypeError):
        g = guess
        s = secret

    if g == s:
        return GuessResult("Win", "🎉 Correct!")
    elif g > s:
        return GuessResult("Too High", "📉 Go LOWER!")
    else:
        return GuessResult("Too Low", "📈 Go HIGHER!")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIXME: Logic breaks here - starter code awarded +5 points for wrong guesses on even attempt numbers
    # FIX: Refactored into logic_utils.py: awards points for win (scaled by attempts) and deducts points for wrong guesses.
    if outcome == "Win":
        points = max(10, 100 - 10 * attempt_number)
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return max(0, current_score - 5)

    return current_score
