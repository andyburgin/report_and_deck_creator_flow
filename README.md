# report_and_deck_creator_flow
This repo contains the report nd slide deck builder using crewai

## Setup environment
```
docker run -ti -v ~/Documents/creai-dev:/git --add-host=host.docker.internal:host-gateway --name crewai-dev python:3.11-bookworm bash
cd /git
git clone https://github.com/andyburgin/report_and_deck_creator_flow.git
cd report_and_deck_creator_flow
```

## Install dependencies
```
uv tool install crewai
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
```{
    "executablePath": "./chrome/linux-137.0.7135.0/chrome-linux64/chrome",
    "args": [
        "--no-sandbox"
    ]
}
```