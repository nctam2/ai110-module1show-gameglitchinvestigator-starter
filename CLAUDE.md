# Game Glitch Investigator - Project Instructions

## Project Overview
This is a deliberately broken Streamlit number-guessing game. The goal is to find and fix intentional bugs, then refactor logic into `logic_utils.py` so tests pass.

## Key Files
- `app.py` — Streamlit UI + all game logic (buggy)
- `logic_utils.py` — refactoring target; all functions currently raise `NotImplementedError`
- `tests/test_game_logic.py` — pytest tests that import from `logic_utils`, not `app.py`
- `reflection.md` — student reflection doc (do not modify unless asked)

## Running the Project
```bash
python -m streamlit run app.py   # run the app
pytest                           # run tests
```

## Known Bugs to Investigate (do not fix unless asked)
1. **Hints are reversed** — `check_guess` in `app.py` returns "Go HIGHER" when guess is too high, should say "Go LOWER" (and vice versa). The comparison logic is inverted.
2. **Type coercion on even attempts** — on even-numbered attempts, `secret` is cast to `str` before comparison in `check_guess`, which breaks numeric comparison and makes hints unreliable.
3. **New game resets attempts to 0, not 1** — `app.py:135` sets `st.session_state.attempts = 0`, but the game starts at 1, so attempt count is off by one after a new game.
4. **Info bar always shows range 1-100** — `app.py:110` hardcodes "1 and 100" regardless of selected difficulty.
5. **Score logic on "Too High"** — `update_score` awards +5 points on even attempts for a wrong guess, which is likely unintentional.
6. **`logic_utils.py` is a stub** — all four functions raise `NotImplementedError`; tests will fail until they are implemented.

## Refactoring Goal
Move these four functions from `app.py` into `logic_utils.py` with correct logic:
- `get_range_for_difficulty(difficulty)`
- `parse_guess(raw)`
- `check_guess(guess, secret)` — tests expect only the outcome string, not a tuple
- `update_score(current_score, outcome, attempt_number)`

Note: `test_game_logic.py` expects `check_guess` to return just the outcome string (e.g., `"Win"`), not the `(outcome, message)` tuple that `app.py` currently uses.

## Architecture Diagram
- `architecture.md` — auto-generated Mermaid diagram. Do not edit manually.
- `analyze_arch.py` — script that reads all source files and calls the Claude API to regenerate the diagram.

Whenever a function is added, removed, or moved between files, run:
```bash
python analyze_arch.py
```

## Debugging Approach
- Use the "Developer Debug Info" expander in the running app to inspect secret, attempts, score, and history
- Run `pytest -v` to see which specific assertions fail
- Fix `logic_utils.py` independently of `app.py` — the tests only import from `logic_utils`
