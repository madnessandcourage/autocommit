import os
from openai import OpenAI


def get_key():
    key = os.getenv("AUTOCOMMIT_OPENAPI_KEY")
    if key is None:
        raise ValueError(
            "OpenAI API key not found. Please, set the AUTOCOMMIT_OPENAPI_KEY environment variable.")
    return key


class Chat():
    def __init__(self,  engine="gpt-3.5-turbo", description="You're helpful and friendly assistant"):
        self.client = OpenAI(
            api_key=get_key()
        )
        self.chat_messages = [
            {
                "role": "system",
                "content": description,
            }
        ]
        self.engine = engine

    def send(self, message):
        self.chat_messages.append({
            "role": "user",
            "content": message,
        })
        completion = self.client.chat.completions.create(
            messages=self.chat_messages,
            model=self.engine,
        )
        self.chat_messages.append({
            "role": "system",
            "content": completion.choices[0].message.content,
        })
        return completion.choices[0].message.content


# c = Chat(key)
# print(c.send("Hello, who are you?"))
