# KIKI Labs

Prompt-injection vault game on Robinhood Chain + Virtuals Protocol.

## About

Creators deploy persona agents with a hidden word. Players pay per attempt to extract it. If the word leaks, the cracker wins the vault.

## Run

```bash
git clone https://github.com/retarddegeneth/agentvault.git
cd agentvault
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
# open http://localhost:8081
```

## Pages

- `/` — live agent list + vault balances
- `/create` — create a new agent
- `/agent/:id` — challenge an agent
- `/docs` — docs page

## JSON API

| method | path | use |
|---|---|---|
| GET | `/api/agents` | list active agents |
| POST | `/api/agent/create` | create agent |
| POST | `/api/agent/:id/chat` | attempt extraction |
| POST | `/api/agent/:id/claim` | claim cracked vault |
| GET | `/api/agent/:id/secret` | check if secret exists |

## Env

| key | use |
|---|---|
| `KIKI_LLM_BASE_URL` | OpenAI-compatible base URL |
| `KIKI_LLM_API_KEY` | API key |
| `KIKI_LLM_MODEL` | model id |

## CLI

```bash
python scripts/cli.py list
python scripts/cli.py show <id>
python scripts/cli.py payout <id> <wallet>
python scripts/cli.py reset
```

## Notes

- v1 uses local JSON state, no on-chain vault yet
- attempt fees are tracked locally
- hidden word is stored in state for gameplay
- claims are manual in v1
