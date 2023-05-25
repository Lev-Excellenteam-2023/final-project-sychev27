import openai


async def api_request(content, message):
    openai.api_key = "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"

    messages = [{"role": "system", "content":
                 "You’re a good teacher who knows how to teach briefly according to topics written on the slides"
                 " and if you  wrote on the topic don't write ot it again"}]

    messages.append({"role": "user", "content": content + message})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return completion.choices[0].message.content


#print(completion.choices[0].message.content)