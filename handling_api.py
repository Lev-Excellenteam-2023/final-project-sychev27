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