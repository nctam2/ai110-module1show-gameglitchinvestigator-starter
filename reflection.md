# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
Game looks pretty normal on first run. 

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  After losing, can't enter new game.
  Hints are random. Will give "Go Higher" or "Go Lower" randomly.
  New game resets attempts to 0
  Claude also found:
    -Hints are reversed
    -Type coercion on even attempts
    -Info bar always shows range 1-100
    -Score logic on "Too High" updates reward for wrong attempts

  
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used cursor as the IDE with Claude in the terminal.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - caught bugs like info bar always showing hard coded range, score logic rewarding, and all the bugs it caught seemed to be right
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - Failed to catch key bugs like the New Game button not working, and did bad suggestions like having score go to negative values

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - If all the tests ran smoothly, and a manual test of that specific bug worked successfully
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
    - Make sure blank guesses don't decrement count or update anything. Tested manually and through a pytest. Showed that my code can handle basic user input edge cases
- Did AI help you design or understand any tests? How?
  - The AI did help me design my tests, but it didn't really seem to understand everything that needed to be tested, especially from a visual standpoint. It sped up the test making, but didn't always nail down what needed to be tested unless I gave it specific instructions.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  - On even attempts, the secret was converted to a string, so check_guess compared an int guess to a str which should never be equal in python. So even guesses would always fail. In addition to this, hints were reversed. This made it seem like the secret number kept changing, and why the hints seemed incorrect.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - In streamlit, every time you interact, to make the UI seem like it changed, it reruns the entire python script to reload any changes made to the state. The issue is that a normal variable set to a random int, will be reset in this case, which is not what we want for things that should be persistent throughout the duration of the game, like the secret number. To fix this, we use st.session_state to make sure this random number stays persistent for the game.
- What change did you make that finally gave the game a stable secret number?
  - Remove the weird type coercion on even attempts. And made sure that st.session_state.secret was set to the value, instead of making secret a local value that would get reset on each rerun.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  One habit I want to reuse it to plan, and make sure to always have it make thorough tests(But I think I could have a testing agent to make sure my tests are more thorough with edge cases). While I've been able to experiment a little bit with agents, I definitely want to utilize them more.
- What is one thing you would do differently next time you work with AI on a coding task?
  - Make smaller commits to describe changes, instead of one large commit where I can't describe most of the work I did in one message
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - AI generated code usually works fine, but even with multiple passes, it often can't find all the bugs, especially those that are seen on the user side. I realized that it takes lots of passes over the same code that I just went over to really get something that is bug free. To make sure these changes stay, thorough testing is super super important, especially to check for edge cases. And I realized that manual testing is still super important. Can't just say, fix all the bugs and write tests to check functionalities. In reality, I need to spend a lot of time manually testing features and interactions.
