# Give Your Assistant a Memory

A Telegram bot that transforms a stateless AI chatbot into a **persistent, personalized AI agent** using a four-tier memory architecture. Built with Python, OpenAI, and python-telegram-bot.

---

## Architecture

The bot maintains context across sessions using four memory layers:

| Tier | Storage | Lifetime |
|------|---------|----------|
| Session Memory | In-process Python dict | Single conversation |
| Daily Notes | Markdown files in `workspace/daily_notes/` | Per day |
| Core Memory | `SOUL.md` + `USER.md` | Permanent |
| Long-term Storage | SQLite (`workspace/memory.db`) | Permanent |

On every message, the bot: loads core memory → retrieves recent DB history → appends session context → calls OpenAI → saves the reply to daily notes and SQLite.

---

## Project Structure

```
Give-Your-Assistant-a-memory/
├── bot.py               # Main Telegram bot with memory logic
├── SOUL.md              # Assistant personality and communication style
├── USER.md              # User profile (name, goals, preferences)
├── memory_config.json   # Memory tier and guardrail configuration
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore
└── LICENSE
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/JaswantOnGit/Give-Your-Assistant-a-memory.git
cd Give-Your-Assistant-a-memory
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in:

- `TELEGRAM_BOT_TOKEN` — from [@BotFather](https://t.me/BotFather) on Telegram
- `OPENAI_API_KEY` — from [platform.openai.com](https://platform.openai.com)
- `TELEGRAM_USER_ID` — your numeric Telegram ID (find it via [@userinfobot](https://t.me/userinfobot))

### 5. Personalise the core memory files

Edit **`SOUL.md`** to define your assistant's personality, tone, and rules.

Edit **`USER.md`** to describe yourself — your name, goals, preferences, and background.

### 6. Run the bot

```bash
python bot.py
```

Open Telegram and send your bot a message. The assistant will respond with full memory context loaded.

---

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Wake the bot and confirm memory is loaded |
| `/reset` | Clear session memory (long-term memory is preserved) |

---

## Memory Files

### SOUL.md — Assistant Identity

Defines the assistant's name, personality traits, tone, and behavior rules. Loaded into the system prompt on every startup.

### USER.md — User Profile

Describes the user's background, goals, and preferences so the assistant can personalise every response from the first message.

### Daily Notes

Auto-generated in `workspace/daily_notes/YYYY-MM-DD.md`. Each conversation turn is timestamped and appended, giving the assistant a running log of past sessions.

### memory_config.json

Controls which memory tiers are active and sets security guardrails (Telegram user allowlist).

---

## Security

- Hard guardrail: the bot rejects any message from a Telegram user ID not listed in `TELEGRAM_USER_ID`
- Soft guardrails: personality and behavioral boundaries defined in `SOUL.md`
- All secrets are loaded from `.env` and never committed to source control

---

## Author

**Jaswant Singh** — PMP Certified Technical Project Manager  
Calgary, Alberta, Canada  
[jaswants022@gmail.com](mailto:jaswants022@gmail.com)

---

## License

MIT — see [LICENSE](LICENSE) for details.
