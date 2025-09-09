2. Install dependencies
Install OpenAI SDK using pip (Requires: Python >=3.8):

pip install openai
3. Run a basic code sample
This sample demonstrates a basic call to the chat completion API. It is leveraging the GitHub AI model inference endpoint and your GitHub token. The call is synchronous.

import os
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-5"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
    model=model
)

print(response.choices[0].message.content)
4. Going beyond rate limits
You're using GitHub Models for free with rate limits.
To remove limits and scale your app, enable paid usage. You'll be billed per token used. Learn more about billing.
Using Azure Metered Billing? Go through our bring your own key (BYOK) setup to add your billing info and start using paid model usage through Azure.