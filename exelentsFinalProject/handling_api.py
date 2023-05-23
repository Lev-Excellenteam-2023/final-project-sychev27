import os
import openai
openai.api_key = "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"

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "Tell the world about the ChatGPT API in the style of a pirate."}
  ]
)


print(completion.choices[0].message.content)