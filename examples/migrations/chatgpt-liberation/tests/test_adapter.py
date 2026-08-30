"""Tests for ChatGPT liberation adapter — 10 tests, deterministic."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from adapter.mapper import classify, map_chatgpt
from adapter.parser import extract_messages, load_chatgpt_export


def test_load_zip():
    exp = load_chatgpt_export(ROOT / "sample-data" / "chatgpt-export.zip")
    assert len(exp["conversations"]) == 38
    assert len(exp["memories"]) == 5

def test_load_dir():
    exp = load_chatgpt_export(ROOT / "sample-data")
    assert len(exp["conversations"]) == 38

def test_extract_messages_user_only_count():
    exp = load_chatgpt_export(ROOT / "sample-data")
    msgs = extract_messages(exp["conversations"])
    # 106 total (both roles), 53 user approx
    user_msgs = [m for m in msgs if m["role"] == "user"]
    assert len(user_msgs) >= 40

def test_classify_preference():
    assert classify("I love coffee, usually 2 cups") == "preference"

def test_classify_instruction():
    assert classify("Remember: I'm vegetarian, no meat") == "instruction" or classify("Instruction: always include risks") == "instruction"

def test_classify_goal():
    assert classify("My main goal is to ship Project Atlas by Aug 30") == "goal"

def test_classify_observation_prefix():
    assert classify("Observation: dense retrieval fails on our 4PB") == "observation"

def test_map_count():
    exp = load_chatgpt_export(ROOT / "sample-data")
    rows = map_chatgpt(exp)
    assert len(rows) == 43
    # no assistant observations beyond user
    assert all(r["source"] == "chatgpt" for r in rows)

def test_map_covers_all_types():
    exp = load_chatgpt_export(ROOT / "sample-data")
    rows = map_chatgpt(exp)
    types = {r["type"] for r in rows}
    assert len(types) == 13

def test_evolving_preference_tag():
    exp = load_chatgpt_export(ROOT / "sample-data")
    rows = map_chatgpt(exp)
    tagged = [r for r in rows if "contradiction-resolved" in r["tags"]]
    assert len(tagged) >= 1
    assert any("coffee" in r["content"].lower() and "tea" in r["content"].lower() for r in tagged)
