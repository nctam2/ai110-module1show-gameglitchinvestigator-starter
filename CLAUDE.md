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

## Known Bugs (all fixed)
The following bugs were discovered and fixed during development:

### Original 6 bugs (from starter code)
1. **Hints were reversed** — `check_guess` returned "Go HIGHER" when guess was too high. Fixed: corrected comparison logic.
2. **Type coercion on even attempts** — `secret` was cast to `str` on even attempts, breaking comparison. Fixed: removed type coercion.
3. **New game reset attempts to 0, not 1** — off-by-one on attempt count after new game. Fixed: resets to 0.
4. **Info bar hardcoded range 1-100** — ignored difficulty setting. Fixed: uses `low`/`high` variables.
5. **Score logic on "Too High"** — awarded +5 on even attempts for wrong guesses. Fixed: consistently deducts 5 for wrong guesses.
6. **`logic_utils.py` was a stub** — all functions raised `NotImplementedError`. Fixed: implemented all four functions.

### Additional bugs found during testing
7. **Score started at 0, went negative** — `st.session_state.score` initialized to 0; wrong guesses deducted 5, causing negative scores. Fixed: initial score is now 100.
8. **New Game button broken after game over** — new game handler did not reset `status`, `score`, or `history`, so the game stayed in "won"/"lost" state and `st.stop()` blocked play. Also hardcoded `randint(1, 100)` instead of using difficulty range. Fixed: resets all session state and uses `low, high`.
9. **Attempts off-by-one** — `attempts` initialized to 1 instead of 0, and incremented before processing the guess, so users got `attempt_limit - 1` guesses instead of `attempt_limit`. Fixed: initialize `attempts` to 0.
10. **Debug info showed stale state** — "Developer Debug Info" expander rendered before the submit handler, so it displayed pre-update values for attempts, score, and history. Fixed: moved debug expander to after the submit/new-game handler block.
11. **Game-over ambiguity** — on the last wrong guess, "Out of attempts!" was shown inline but the input remained interactive; submitting again showed a different generic "Game over" message. Fixed: on win/loss, `st.rerun()` immediately triggers the status check which shows a single informative message (including the secret and score) and calls `st.stop()`.
12. **Attempts-left counter stale after guess** — `st.info()` rendered before the submit handler, so it showed the pre-increment attempt count. Fixed: replaced with `st.empty()` placeholder filled after the handler runs.
13. **Difficulty change didn't reset game state** — changing difficulty after a win/loss kept the old `status`, `score`, `history`, etc., so balloons and win/loss messages reappeared on the new difficulty. Fixed: track difficulty in `st.session_state.difficulty` and reset all game state when it changes.
14. **Blank/invalid guesses consumed attempts** — `attempts` was incremented before `parse_guess` validated the input, so blank, empty, or non-numeric submissions counted as attempts and could drive the counter negative. Fixed: moved `attempts += 1` to after validation succeeds; invalid guesses no longer affect attempt count or history.

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
