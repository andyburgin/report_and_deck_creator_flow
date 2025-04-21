# report_and_deck_creator_flow
This repo contains the report and slide deck builder using crewai

## Setup environment
```
docker run -ti -v ~/Documents/crewai-dev:/git --add-host=host.docker.internal:host-gateway --name crewai-dev python:3.11-bookworm bash
cd /git
git clone https://github.com/andyburgin/report_and_deck_creator_flow.git
cd report_and_deck_creator_flow
```

## Install dependencies
```
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv tool install crewai
uv add python-pptx
uv add exa_py
crewai install
```
Rename `.env.example` to `.env` and update with your api keys

## Install mermaid dependencies
```
apt-get update
apt-get install npm -y
npm install -g @mermaid-js/mermaid-cli
npx @puppeteer/browsers install chrome --install-deps
```
Note the version of chrome installed and update the `puppeteer-config.json` file with the executablePath, replacing the path and version with the details ouput from the last command above:
```
{
    "executablePath": "./chrome/linux-137.0.7135.0/chrome-linux64/chrome",
    "args": [
        "--no-sandbox"
    ]
}
```

## Running report and slide deck generation
Edit `src/report_and_deck_creator_flow/main.py` and update the `title`, `topic` and `goal`.
Run the flow by
```
crewai flow kickoff
```

## View resulting report and slide deck
The flow will create a markdown file and pptx.
