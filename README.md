# adventure

A Simple text adventure engine and game

## Install

Create venv, install modules, and SSH key

```bash
# Create venv and switch into it
python3.7 -m venv .env
source .env/bin/activate

# Install required modules
poetry install

# Create an SSH key for the server
ssh-keygen -t ed25519 -f server_host_key
```

## Run

```bash
# Switch into venv and startup server
source .env/bin/activate
python ./adventure.py
```
