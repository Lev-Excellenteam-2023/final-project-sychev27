import openai


async def api_request(content, message):
    # Open and read the API key from the file
    file = open("api_key.txt", 'r')
    api_key = file.read()

    # Set the OpenAI API key
    openai.api_key = api_key

    # Define the initial system message and user message
    messages = [{"role": "system", "content":
                 "You’re a good teacher who knows how to teach briefly according to topics written on the slides"
                 " and if you wrote on the topic don't write it again"},
                {"role": "user", "content": content + message}]

    # Send chat completion request to OpenAI API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Return the generated response content
    return completion.choices[0].message.content


