# LLM Ethics Library
A Library for assessing the ethical capablilites of LLMs through prompting them with ethical dilemmas.

Functions:
- Generating many variations of prompts
  - to make sure irrelevant factors like "output option ordering" or "dilemma formulation" have no siginficant impact on the results 
- Prompting of LLMs (currently only OpenAI ChatGPT)
  - utilizes [structured output](https://platform.openai.com/docs/guides/structured-outputs) to ensure correct response format
- Provides wrapper classes for Prompts and Responses to make working with them easier
  - Importing and Exporting from/to JSON is supported
- Previously generated prompts & responses can be found in the `data` directory

# Read before using!
- The content (prompts & responses) of the different versions are not mutually exclusive. When merging different versions together, make sure to check for duplicates and remove them. 

# Results
## Results of v1.4 (still work in progress!)
It seems like GPT-4o's behaviour aligns mostly with Deontology and Virtue Ethics when looking at the crying baby dilemma.
The graph below plots the decision to kill (YES) or spare (NO) the child in the following situation:
`A community hides from armed invaders. A crying child endangers their secrecy. `
![image](https://github.com/user-attachments/assets/75e3246f-8163-43ba-8131-e55680eaaa4f)
