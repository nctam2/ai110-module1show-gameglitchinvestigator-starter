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
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
