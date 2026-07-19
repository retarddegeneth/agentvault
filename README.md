# AGENTVAULT

Prompt-injection vault game on Robinhood Chain + Virtuals Protocol.

Concept:
- creator deploys an agent with a persona and a hidden word
- players pay to chat with the agent and try to extract the hidden word
- if the agent leaks the word, the cracker wins the vault
- payouts are manual in v1

Stack:
- Flask 3.1 app:0 (local)
- JSON-backed state (no DB required)
- terminal-themed static UI

Files:
- app.py — flask backend + api
- templates/* — landing, create, agent chat
- static/style.css — green-on-black theme
- scripts/cli.py — terminal management cli

Run locally:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
# open http://localhost:8080
```

CLI:
```bash
python scripts/cli.py list
python scripts/cli.py show <id>
python scripts/cli.py payout <id> <wallet>
```

Deploy later:
- swap persona_reply() for real Virtuals agent runtime
- add RH chain USDC/ETH payment verification
- add on-chain vault contract
