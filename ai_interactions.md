# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Refactor the guessing game architecture by decoupling game logic from the UI: migrate core mathematical and validation functions from `app.py` into `logic_utils.py`, fix identified game bugs (inverted hints, string comparison sabotage, session state resets), update `app.py` to import and consume the refactored module, and create automated verification tests in `tests/test_game_logic.py`.

**What did the agent do?**

1. Created a dedicated Python virtual environment (`.venv`) and installed all project dependencies (`streamlit`, `pytest`, `altair`).
2. Implemented `logic_utils.py` containing `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score`.
3. Created a custom `GuessResult(tuple)` class to maintain dual compatibility between `app.py`'s unpacking syntax (`outcome, message = check_guess(...)`) and `test_game_logic.py`'s string assertion (`check_guess(...) == "Win"`).
4. Refactored `app.py` to import functions from `logic_utils.py`, removed the sabotage code (`secret = str(...)` on even turns), and fixed the session state reset logic in the "New Game" button.
5. Added automated pytest test cases in `tests/test_game_logic.py` covering edge cases.
6. Configured `pytest.ini` with `pythonpath = .` to ensure seamless test discovery.

**What did you have to verify or fix manually?**

1. Verified that the starter tests (`assert result == "Win"`) in `tests/test_game_logic.py` did not fail when `check_guess` returned rich tuple outcomes. Rather than allowing the agent to break starter tests or change the UI contract, we used human-in-the-loop oversight to ensure `GuessResult` satisfied both interfaces.
2. Verified in the live Streamlit UI that changing the difficulty setting in the sidebar dynamically re-rolled the secret number within the new range rather than leaving a stale number from the previous difficulty.
3. Verified that invalid inputs (e.g. non-numeric characters) did not deplete the player's attempt counter.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|---|---|---|---|---|
| String vs Int Comparison (`'9'` vs `10`) | "Generate a pytest case to ensure check_guess compares numbers numerically even if one input is passed as a string" | `test_check_guess_mixed_types_no_lexicographical_bug` checking `check_guess(9, "10") == "Too Low"` | Yes | In Python, `'9' > '10'` is True alphabetically. Testing numeric normalization prevents insidious comparison bugs. |
| Inverted Hint Feedback | "Write a test verifying the hint message warns the user to guess lower when guess > secret and higher when guess < secret" | `test_hint_messages_direction` inspecting `"LOWER" in msg_high` and `"HIGHER" in msg_low` | Yes | Ensures the human player receives actionable, correct guidance rather than inverted hints. |
| Decimal Input Validation | "Write a test checking how parse_guess handles decimals like 5.0 versus 5.7" | `test_parse_guess_decimal_handling` ensuring integer floats parse but non-integers are rejected | Yes | Prevents silent truncation and forces explicit integer guessing. |
| Score Bonus on Even Attempts | "Write a test ensuring incorrect guesses do not receive bonus points on even attempt counts" | `test_update_score_no_even_attempt_bonus_glitch` checking `update_score(50, "Too High", 2) == 45` | Yes | Verifies that faulty even-attempt point rewards from the buggy starter code are eliminated. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Review logic_utils.py and app.py for PEP 8 compliance, clean docstrings, clear variable naming, and appropriate type annotations. Ensure comments clearly document bug fixes and logic crime scenes (# FIXME and # FIX).
```

**Linting output before:**

```
- Missing docstrings in refactored functions.
- Redundant logic implementations duplicated across both app.py and logic_utils.py.
- Unhandled Exception catch in parse_guess masking unexpected runtime errors.
- Inconsistent variable naming between secret_number, secret, and g.
```

**Changes applied:**

- Added structured PEP 257 docstrings to all functions in `logic_utils.py` defining parameters and return types.
- Replaced broad `except Exception:` with specific `except ValueError:` in `parse_guess`.
- Unified variable names and added explicit `# FIXME:` and `# FIX:` annotations detailing the human-AI debugging collaboration.
- Extracted constants and consolidated game configuration into modular functions.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

"How should we resolve the discrepancy where `app.py` expects `outcome, message = check_guess(guess, secret)` while `tests/test_game_logic.py` asserts `assert check_guess(50, 50) == 'Win'` without modifying the starter test file?"

| | Model A (Claude 3.7 Sonnet) | Model B (Gemini 2.5 Flash) |
|---|---|---|
| **Model name** | Claude 3.7 Sonnet | Gemini 2.5 Flash |
| **Response summary** | Suggested creating a `GuessResult` class subclassing `tuple` with a custom `__eq__` method that matches string comparisons against index 0 while preserving tuple unpacking. | Suggested changing `check_guess` to return a plain string and creating an auxiliary helper `get_hint_message(outcome)` in `logic_utils.py` to be called separately in `app.py`. |
| **More Pythonic?** | Yes. Leverages Python's object model and tuple subclassing to maintain 100% backwards compatibility with zero breaking changes to existing callers or tests. | Moderately. While separating message generation is clean, it required changing the signature and call sites across `app.py`. |
| **Clearer explanation?** | Yes, included exact code demonstrations showing why `isinstance(other, str)` allows transparent string equality alongside tuple unpacking. | Good, but overlooked the constraint to minimize modifications across existing UI code. |

**Which did you prefer and why?**

I preferred Model A's approach. In real-world legacy codebases and course assignments with automated starter tests, breaking existing test assertions or refactoring multiple external call sites introduces regression risks. Subclassing `tuple` with a custom `__eq__` elegantly met both contracts simultaneously.
