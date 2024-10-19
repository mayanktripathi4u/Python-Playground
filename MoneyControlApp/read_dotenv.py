import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

print(os.getenv("FALSK_SECRET_KEY"))
print(os.getenv("FLASK_COMBINED"))


# Anothet way to get into a dict format.
config = dotenv_values(".env")
print(config)
print(config['FALSK_SECRET_KEY'])
print(config['FLASK_COMBINED'])

# Get all Environment Variables.
print(os.environ)

"""
We can also have two env files.. as below.
.env.shared  --> this will have values which could be shared.
.env.secret  --> only sceret keys to store and will not be shared.

config = {
    **dotenv_values(".env.shared"),
    **dotenv_values(".env.secret"),
    **os.environ
}
print(config)
"""