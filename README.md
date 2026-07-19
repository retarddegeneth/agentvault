# kimilabs

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
| `KIMILABS_LLM_BASE_URL` | OpenAI-compatible base URL |
| `KIMILABS_LLM_API_KEY` | API key |
| `KIMILABS_LLM_MODEL` | model id |
| `KIMILABS_TREASURY_ADDRESS` | official treasury wallet |
| `KIMILABS_TREASURY_PK` | treasury private key (server-side only) |
| `KIMILABS_RPC_URL` | RH chain RPC |
| `KIMILABS_CHAIN_ID` | chain ID (default 4663) |

## On-chain flow

- When `KIMILABS_TREASURY_ADDRESS` + `KIMILABS_RPC_URL` are set, every chat attempt requires a real `tx_hash` paying `attempt_fee` to the treasury.
- Backend verifies the tx on-chain before accepting the attempt.
- Cracked vaults auto-payout from treasury to the cracker's wallet on claim.
- If treasury is not configured, the app falls back to local JSON tracking.

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
