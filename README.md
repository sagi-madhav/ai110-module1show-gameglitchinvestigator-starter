# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `streamlit run app.py`
3. Run test suite: `pytest`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.**
   - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

### Purpose of the Game
The game is an interactive number guessing challenge built in Streamlit. Players choose a difficulty setting (Easy: 1–20, Normal: 1–100, Hard: 1–200) and try to guess a randomly chosen secret number within a limited number of attempts. With each guess, the game gives feedback on whether the guess is too high or too low, adjusts the player's score, and provides hints.

### Bugs Identified
1. **Inverted Hint Directions:** When a guess was greater than the secret number, the game displayed `"📈 Go HIGHER!"`, and when a guess was lower, it displayed `"📉 Go LOWER!"`.
2. **Alternating String Conversion Sabotage:** On even attempt numbers, the secret was cast to a string (`secret = str(st.session_state.secret)`), which raised a `TypeError` when compared to an int and defaulted to lexicographical comparison (e.g., `'9' > '10'`).
3. **Attempt Counter Off-by-One:** Session state initialized `attempts = 1` before any guess was made, depriving players of their first attempt.
4. **Permanent Soft-Lock on New Game:** Clicking "New Game 🔁" did not reset `st.session_state.status = "playing"`. If the player won or lost, the script hit `st.stop()` upon rerun and remained permanently stuck.
5. **Hardcoded Difficulty and Inverted Ranges:** Hard mode was configured with a smaller range (1–50) than Normal (1–100), and the UI banner hardcoded "between 1 and 100" rather than reflecting the selected difficulty range.
6. **Erratic Scoring Logic:** In `update_score()`, players were awarded `+5` points for wrong guesses on even attempt numbers.
7. **Architectural Coupling & Missing Logic Module:** All logic lived directly in `app.py`, while `logic_utils.py` had empty stubs raising `NotImplementedError`, causing all automated tests to fail.

### Fixes Applied
1. **Refactored Core Logic into `logic_utils.py`:** Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` into `logic_utils.py` and imported them into `app.py`.
2. **Fixed Inverted Hints & Type Safety:** Updated `check_guess` to point players in the correct direction (`"Too High" -> "📉 Go LOWER!"`, `"Too Low" -> "📈 Go HIGHER!"`). Implemented clean integer type normalization to eliminate `TypeError` crashes and alphabetical comparison bugs.
3. **Engineered `GuessResult`:** Built a transparent `GuessResult(tuple)` class that unpacks as `(outcome, message)` in `app.py` and compares directly to string constants (`result == "Win"`) in tests, preserving backwards compatibility with existing starter tests.
4. **Repaired Streamlit State Management:** Initialized `attempts = 0`, reset all state variables (`status`, `attempts`, `score`, `history`, `secret`) when "New Game" is clicked, and automatically re-rolled the secret number if difficulty changed.
5. **Corrected Scoring & Difficulty Ranges:** Set Hard range to 1–200, ensured only valid guesses consume attempts, and removed spurious point rewards for incorrect guesses.
6. **Comprehensive Automated Verification:** Added 8 new unit tests covering edge cases (whitespace, decimals, mixed types, difficulty scaling, scoring).

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. **Launch App & Select Difficulty:** Open the app with `streamlit run app.py`. In the sidebar, select a difficulty (e.g. Normal: 1–100 with 8 attempts).
2. **Review Initial State:** Observe that the UI accurately displays "Guess a number between 1 and 100. Attempts left: 8" and the attempts counter in "Developer Debug Info" starts cleanly at 0.
3. **Submit a Guess:** Enter a number (e.g., `50`) into the text box and click "Submit Guess 🚀".
4. **Follow Accurate Hints:** If 50 is too high, the app warns `📉 Go LOWER!` and decrements attempts left to 7. Enter a lower guess (e.g. `25`).
5. **Win & Reset:** Enter the matching secret number. Confetti balloons appear, your final score is displayed, and clicking "New Game 🔁" cleanly resets the board for a fresh round.

## 🧪 Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.12.4, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\Code\CodePath\ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
plugins: anyio-4.15.1
collected 11 items

tests\test_game_logic.py ...........                                     [100%]

============================= 11 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
