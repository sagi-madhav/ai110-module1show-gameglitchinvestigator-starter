# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When first launching the application, the Streamlit interface appeared visually intact, but attempting to play revealed that the game was fundamentally broken. Opening the "Developer Debug Info" expander revealed that `attempts` was initialized to 1 before any guess was made, immediately stealing an attempt from the player. As soon as guesses were entered, the hints actively lied by telling the player to "Go HIGHER!" when their guess was already too high, and on even attempt numbers, type coercion sabotage converted the secret into a string, breaking comparisons. Furthermore, after winning or losing, clicking "New Game" left `status` unchanged, causing `st.stop()` to permanently freeze the app in an unplayable game-over state.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|---|---|---|---|
| Guess `60` when Secret is `50` (Attempt 1) | Game indicates "Too High" and displays hint "📉 Go LOWER!" with point penalty. | Game displayed "📈 Go HIGHER!", misleading the player to make higher guesses. | Streamlit warning displayed: `📈 Go HIGHER!` |
| Guess `9` when Secret is `10` (Attempt 2, even attempt) | Game indicates "Too Low" and prompts the user to guess higher (9 < 10). | Secret was cast to str `"10"`, triggering a `TypeError` on `guess > secret`, which fell back to lexicographical comparison `"9" > "10"`, falsely reporting "Too High". | Handled internally by `except TypeError: g = str(guess)` producing reversed comparison. |
| Click "New Game 🔁" after winning or running out of attempts | Game resets `status = 'playing'`, clears guess history, resets attempts and score, and picks a new secret. | `new_game` only reset `attempts = 0` and generated a number, leaving `status = 'won'` or `'lost'`. The app hit `st.stop()` and froze. | Streamlit alert: `"You already won. Start a new game to play again."` (game halted). |
| Run `pytest` on starter project | Test suite imports logic functions and verifies game rules. | All tests crashed with `NotImplementedError` because starter code left stubbed functions in `logic_utils.py` while duplicating buggy code in `app.py`. | `FAILED tests/test_game_logic.py::test_winning_guess - NotImplementedError: Refactor this function...` |

---

## 2. How did you use AI as a teammate?

During this investigation, I used an AI coding assistant (Gemini 3.8 Flash / Claude Code agent) as an interactive pair programmer to diagnose issues, refactor code, and generate unit tests. One suggestion the AI made that was completely correct was diagnosing the Streamlit lifecycle: it explained why `attempts` and `status` were persisting stale values on "New Game" and suggested re-initializing all keys in `st.session_state` (`status="playing"`, `attempts=0`, `history=[]`, `score=0`) upon restart. I verified this recommendation by inspecting the Developer Debug Info expander during live manual gameplay, confirming that clicking "New Game" cleanly reset all state.

Conversely, one suggestion I did not accept as written occurred during test reconciliation: the AI suggested rewriting all existing starter tests in `tests/test_game_logic.py` because `check_guess` in `app.py` returned a 2-tuple `(outcome, message)` whereas `tests/test_game_logic.py` asserted `assert result == "Win"`. Modifying the starter test set or degrading the UI message contract would have been a lazy hallucination workaround that defeated the purpose of human-in-the-loop verification. Instead, I prompted the AI to design a lightweight `GuessResult(tuple)` subclass that simultaneously behaves as a 2-tuple for UI unpacking and supports direct string equality (`result == "Win"`). I verified this approach by running `pytest`, ensuring 100% test suite compatibility without changing a single line of the original starter tests.

---

## 3. Debugging and testing your fixes

To decide whether a bug was truly fixed, I established a strict two-stage verification standard: an automated unit test in pytest had to pass in isolation, followed by live verification in the Streamlit web application. For automated testing, I executed `pytest -v`, which ran 11 test cases covering starter requirements, hint inversion, mixed string/int type coercion, decimal parsing, and score calculations. The test `test_check_guess_mixed_types_no_lexicographical_bug` proved critical: it verified that passing `"9"` against `10` or vice versa is evaluated numerically (9 < 10) rather than lexicographically (`'9' > '10'`). The AI assisted significantly in designing the test set by identifying tricky edge cases, such as whitespace trimming in `parse_guess(" 42 ")` and preventing wrongful point bonuses on even attempt numbers in `update_score`.

---

## 4. What did you learn about Streamlit and state?

Streamlit operates on a unique reactive execution model where the entire Python script runs from line 1 to the end every time a user interacts with a widget (such as clicking a button or pressing Enter). To someone new to the framework, this means standard local Python variables lose their values and get recreated on every click, making game continuity impossible. `st.session_state` solves this by acting like a persistent dictionary that survives across reruns, holding game-critical data such as the secret number, score, and attempts until explicitly reset.

---

## 5. Looking ahead: your developer habits

One habit from this project that I will carry into every future project is separating business logic from user interface code into dedicated utility modules (`logic_utils.py` vs `app.py`) accompanied by automated pytest suites. This architectural separation makes logic testable in milliseconds without having to repeatedly click through a browser UI. Next time I collaborate with an AI assistant, I will provide stricter schema definitions and explicit input/output contracts in my initial prompts to avoid AI over-engineering or hallucinated return signatures. Ultimately, this project reinforced that AI pair programmers are rapid prototyping accelerators, but human-in-the-loop critical judgment is mandatory to detect subtle bugs, preserve test set integrity, and deliver robust software.
