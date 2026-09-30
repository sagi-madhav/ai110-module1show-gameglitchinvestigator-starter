# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first launched the app, the UI looked fine on the surface, but playing it quickly showed how glitchy it was. Right away, the debug info showed that attempts started at 1 before I even guessed, and the hints were completely backwards, telling me to guess higher when I was already too high. On even attempts, guessing numbers like 9 against 10 failed because strings and numbers were being compared as text instead of numerically. Clicking the new game button also failed to reset the status, which froze the game on a game-over screen until the page was reloaded.

---

## 2. How did you use AI as a teammate?

I used an AI assistant as an interactive pair programmer to help track down bugs, refactor code, and write unit tests. The AI was very helpful when explaining the Streamlit lifecycle, pointing out that "New Game" was not resetting all keys in `st.session_state`, which I verified by watching the debug panel during manual play. However, I rejected its initial suggestion to rewrite the starter tests when `check_guess` returned a tuple instead of a single string for the UI message. Instead of changing the original tests, I had the AI create a custom tuple that supports string equality, which I verified by running pytest with all starter tests passing.

---

## 3. Debugging and testing your fixes

I only considered a bug fixed when it passed an automated pytest case and also worked properly during manual play in the browser. Running `pytest -v` let me test 11 different scenarios in seconds, including a test that verified comparing '9' to 10 treats them as numbers so '9' doesn't falsely show up as greater than 10. The AI helped by suggesting edge-case tests I had not thought of right away, like handling input with extra spaces and catching invalid decimal entries. Combining automated unit tests with live browser testing gave me confidence that our fixes actually held up.

---

## 4. What did you learn about Streamlit and state?

I would tell a friend that Streamlit reruns your entire Python script from top to bottom every single time you interact with anything on the page, like clicking a button or typing. Because of this, normal variables get wiped out and re-initialized on every single click, which would make a game lose your score and secret number immediately. That is why `st.session_state` exists; it works like a persistent dictionary that remembers values across all those reruns. Using session state lets the app keep track of your attempts, guess history, and game progress until you deliberately reset them.

---

## 5. Looking ahead: your developer habits

A habit I definitely want to reuse is separating core business logic into its own utility module with unit tests before wiring it up to a UI. Next time I work with AI, I plan to be much more explicit upfront about expected function inputs and return types so we do not waste time reconciling mismatched formats. This project showed me that AI is great at speeding up brainstorming and writing tests, but it can easily introduce subtle bugs or suggest modifying test suites to take shortcuts. It really reinforced that you cannot blindly trust AI output without reviewing the logic and verifying it yourself.
