# python-openv

Installation:

```sh
pip install python-openv
```

Usage:

```python
from openv import load_openv

load_openv(project="my_project_name")
```

## Overview

This is a simple utility for loading project environment variables from 1password. It works more or less the same as [python-dotenv](https://github.com/theskumar/python-dotenv). It uses the [1password-client](https://github.com/wandera/1password-client) python package to access fields.

## Purpose

In theory, it's more secure, as someone with access to your computer can't go through your `.env` files, and you also don't risk accidentally including the `.env` file in version control.

## Requirements

1. In order to use this, you will need to install the [1Password CLI](https://developer.1password.com/docs/cli/get-started/) and turn on the desktop app integration.
2. You need to have a 1password vault named `.env`.
3. The title of each item in that vault must be unique within the vault.

## Example Workflow

Suppose you're developing a FastAPI app called `dad_joke_generator` that uses the OpenAI API to generate dad jokes. Assuming that you've added the API key to environment variables on whatever service we're deploying on (either directly, or through a service like Doppler or AWS Secrets Manager) - the question is how you reference the API key in your local development environment.

If we're using poetry for the app, we might add `python-openv` to the dev dependencies with:

```sh
poetry add python-openv --group dev
```

After creating a `.env` vault in 1password, you might add an item called `dad_joke_generator`, and add the following password field: `OPENAI_API_KEY`.

Then, your FastAPI app might look as follows (I didn't test this app so it might not work, it's just meant to illustrate usage).


```python
import os
import uvicorn
from openai import OpenAI
from fastapi import FastAPI

try:
    from openv import load_openv
    load_openv("dad_joke_generator")
except:
    pass

# The name of the field in the .env 1password vault.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

@app.get("/joke")
async def joke():
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Tell me a dad joke.",
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)

```

Note that you probably don't want to implement a production app like this, this is just to demonstrate idea. Of course, you can also use this to dynamically determine the host, port, whether the app reloads, uses debug mode, etc.

Also, in this case, when you deploy the app you would run:

```sh
poetry install --without dev
```

In whatever build script/configuration file you're using. This way `python-openv` won't be installed in your production environment, so the import will fail and the value you set in your production environment for that environment variable will be used instead.

