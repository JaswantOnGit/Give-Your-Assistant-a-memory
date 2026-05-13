"""
bot.py - Persistent Memory Telegram Assistant
==============================================
A Telegram bot powered by OpenAI that maintains layered memory across sessions:
  - Session memory   : in-context message history
  - Daily notes      : auto-saved markdown files per day
  - Core memory      : SOUL.md (personality) + USER.md (user profile)
  - Long-term storage: SQLite database for conversation history

Usage:
    python bot.py

Environment variables required (see .env.example):
    TELEGRAM_BOT_TOKEN  - Your Telegram bot token from @BotFather
    OPENAI_API_KEY      - Your OpenAI API key
    TELEGRAM_USER_ID    - Your Telegram numeric user ID (for security guardrail)
"""

import os
import json
import sqlite3
import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import openai

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALLOWED_USER_ID = int(os.getenv("TELEGRAM_USER_ID", "0"))

openai.api_key = OPENAI_API_KEY

WORKSPACE_DIR = Path("./workspace")
DAILY_NOTES_DIR = WORKSPACE_DIR / "daily_notes"
DB_PATH = WORKSPACE_DIR / "memory.db"
SOUL_PATH = Path("SOUL.md")
USER_PATH = Path("USER.md")
CONFIG_PATH = Path("memory_config.json")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# In-memory session history: {chat_id: [{"role": ..., "content": ...}, ...]}
session_memory: dict[int, list[dict]] = {}

# ---------------------------------------------------------------------------
# Setup helpers
# ---------------------------------------------------------------------------

def ensure_workspace() -> None:
    """Create workspace directories if they don't exist."""
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    DAILY_NOTES_DIR.mkdir(parents=True, exist_ok=True)


def init_db() -> None:
    """Initialise the SQLite long-term memory database."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT    NOT NULL,
                role      TEXT    NOT NULL,
                content   TEXT    NOT NULL
            )
            """
        )
        conn.commit()


def load_core_memory() -> str:
    """Load SOUL.md and USER.md into a combined system prompt string."""
    soul = SOUL_PATH.read_text(encoding="utf-8") if SOUL_PATH.exists() else ""
    user = USER_PATH.read_text(encoding="utf-8") if USER_PATH.exists() else ""
    return f"# Assistant Soul\n{soul}\n\n# User Profile\n{user}"


def load_memory_config() -> dict:
    """Load memory_config.json."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# ---------------------------------------------------------------------------
# Memory helpers
# ---------------------------------------------------------------------------

def get_daily_note_path() -> Path:
    return DAILY_NOTES_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.md"


def append_to_daily_note(role: str, content: str) -> None:
    """Append a message to today's daily note file."""
    note_path = get_daily_note_path()
    timestamp = datetime.now().strftime("%H:%M")
    with open(note_path, "a", encoding="utf-8") as f:
        if not note_path.exists() or note_path.stat().st_size == 0:
            f.write(f"# Daily Note - {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"**[{timestamp}] {role.capitalize()}:** {content}\n\n")


def save_to_db(role: str, content: str) -> None:
    """Persist a message to the SQLite long-term store."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO conversations (timestamp, role, content) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), role, content),
        )
        conn.commit()


def load_recent_history(limit: int = 20) -> list[dict]:
    """Retrieve the most recent N messages from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [{"role": r, "content": c} for r, c in reversed(rows)]

# ---------------------------------------------------------------------------
# Security guardrail
# ---------------------------------------------------------------------------

def is_authorised(user_id: int) -> bool:
    """Return True only if the user is on the allowlist."""
    if ALLOWED_USER_ID == 0:
        logger.warning("TELEGRAM_USER_ID not set - running without access control!")
        return True
    return user_id == ALLOWED_USER_ID

# ---------------------------------------------------------------------------
# OpenAI call
# ---------------------------------------------------------------------------

def chat_with_memory(chat_id: int, user_message: str) -> str:
    """
    Build a full prompt from core memory + recent DB history + session history,
    send to OpenAI, and return the assistant reply.
    """
    system_prompt = load_core_memory()

    # Build message list: system -> recent long-term -> session -> current user msg
    messages = [{"role": "system", "content": system_prompt}]
    messages += load_recent_history()
    messages += session_memory.get(chat_id, [])
    messages.append({"role": "user", "content": user_message})

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )
    reply = response.choices[0].message.content.strip()
    return reply

# ---------------------------------------------------------------------------
# Telegram handlers
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    if not is_authorised(update.effective_user.id):
        logger.warning("Unauthorised /start from user %s", update.effective_user.id)
        await update.message.reply_text("Access denied.")
        return
    await update.message.reply_text(
        "Hey Jay! I'm back online and my memory is loaded. What are we working on today?"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /reset command - clears session memory only."""
    if not is_authorised(update.effective_user.id):
        await update.message.reply_text("Access denied.")
        return
    chat_id = update.effective_chat.id
    session_memory.pop(chat_id, None)
    await update.message.reply_text("Session memory cleared. Long-term memory is still intact.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if not is_authorised(user_id):
        logger.warning("Unauthorised message from user %s", user_id)
        await update.message.reply_text("Access denied.")
        return

    user_text = update.message.text

    # Save user turn
    append_to_daily_note("user", user_text)
    save_to_db("user", user_text)
    session_memory.setdefault(chat_id, []).append({"role": "user", "content": user_text})

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    # Get reply
    reply = chat_with_memory(chat_id, user_text)

    # Save assistant turn
    append_to_daily_note("assistant", reply)
    save_to_db("assistant", reply)
    session_memory[chat_id].append({"role": "assistant", "content": reply})

    await update.message.reply_text(reply)

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    ensure_workspace()
    init_db()

    config = load_memory_config()
    logger.info("Memory config loaded: %s tiers active", len(config.get("memory_tiers", {})))
    logger.info("Core memory loaded from SOUL.md and USER.md")
    logger.info("Starting bot...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
