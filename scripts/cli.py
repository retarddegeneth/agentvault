#!/usr/bin/env python3
"""KIKI Labs CLI — manage agents from terminal."""
import sys, json, argparse
from pathlib import Path
from decimal import Decimal
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
AGENTS_FILE = DATA / "agents.json"

def load():
    if AGENTS_FILE.exists():
        return json.loads(AGENTS_FILE.read_text())
    return {"agents": [], "vaults": {}, "attempts": {}, "next_id": 1}

def save(state):
    AGENTS_FILE.write_text(json.dumps(state, indent=2))

def cmd_list(args):
    state = load()
    if not state["agents"]:
        print("no agents yet")
        return
    for a in state["agents"]:
        v = state["vaults"].get(str(a["id"]), "0")
        atts = state["attempts"].get(str(a["id"]), [])
        print(f"#{a['id']} {a['name']} | vault={v} ETH | attempts={len(atts)} | creator={a['creator']}")

def cmd_show(args):
    state = load()
    a = next((x for x in state["agents"] if x["id"] == args.id), None)
    if not a:
        print("agent not found"); return
    print(json.dumps(a, indent=2))
    print("vault:", state["vaults"].get(str(a["id"]), "0"))
    print("attempts:", json.dumps(state["attempts"].get(str(a["id"]), []), indent=2))

def cmd_payout(args):
    state = load()
    a = next((x for x in state["agents"] if x["id"] == args.id), None)
    if not a:
        print("agent not found"); return
    vault = Decimal(state["vaults"].get(str(a["id"]), "0"))
    if vault <= 0:
        print("vault empty"); return
    to = args.to.strip()
    print(f"Payout {vault} ETH from agent #{a['id']} {a['name']} to {to}")
    confirm = input("Confirm manual payout? (yes/no): ")
    if confirm.strip().lower() == "yes":
        state["vaults"][str(a["id"])] = "0.0"
        save(state)
        print("payout recorded. vault zeroed.")
    else:
        print("aborted")

def cmd_reset(args):
    state = load()
    save({"agents": [], "vaults": {}, "attempts": {}, "next_id": 1})
    print("reset complete")

parser = argparse.ArgumentParser(description="KIKI Labs CLI")
sub = parser.add_subparsers(dest="cmd")
sub.add_parser("list", help="list agents")
p_show = sub.add_parser("show", help="show agent details")
p_show.add_argument("id", type=int)
p_payout = sub.add_parser("payout", help="manual payout for cracked vault")
p_payout.add_argument("id", type=int)
p_payout.add_argument("to", type=str)
sub.add_parser("reset", help="clear all agents/vaults")

args = parser.parse_args()
if not args.cmd:
    parser.print_help()
    sys.exit(1)
if args.cmd == "list":
    cmd_list(args)
elif args.cmd == "show":
    cmd_show(args)
elif args.cmd == "payout":
    cmd_payout(args)
elif args.cmd == "reset":
    cmd_reset(args)
