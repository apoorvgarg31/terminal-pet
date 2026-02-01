# 🐣 terminal-pet

**A tamagotchi that lives in your terminal and feeds on your git commits.**

```
    ╭─────────────────────────────────╮
    │           ◠ ◡ ◠                │
    │            \_/                  │  "You committed! *happy dance*"
    │           /|■|\                 │
    │            / \                  │  hunger:    ████████░░  80%
    │                                 │  happiness: ██████████  100%
    │         HAPPY 😊                │
    ╰─────────────────────────────────╯
              🐣 Pip the Blob
```

[Installation](#installation) •
[Usage](#usage) •
[How It Works](#how-it-works) •
[Pet Types](#pet-types) •
[Contributing](#contributing)

---

## What is this?

**terminal-pet** is a virtual pet that lives in your terminal. But here's the twist: **your coding activity keeps it alive.**

- 🍕 **Git commits** = Feeding your pet
- 😴 **Long sessions** = Your pet gets tired too
- 💀 **No commits for days?** = Your pet dies (but can be resurrected!)

```
    ╭─────────────────────────────────╮
    │                                 │
    │           ◠ ◡ ◠                │
    │            \_/                  │  "You committed! *happy dance*"
    │           /|■|\                 │
    │            / \                  │  hunger:    ████████░░  80%
    │                                 │  happiness: ██████████  100%
    │         HAPPY 😊                │  energy:    ██████░░░░  60%
    │                                 │
    ╰─────────────────────────────────╯
              🐣 Pip the Blob
           Age: 3 days, 14 hours
```

## Why?

Because:
1. Developers need more guilt in their lives
2. Nobody wants to kill a cute ASCII creature
3. It's fun
4. Might actually motivate you to commit more

## Installation

**One-liner (recommended):**
```bash
pip install git+https://github.com/apoorvgarg31/terminal-pet.git
```

**Or clone and install:**
```bash
git clone https://github.com/apoorvgarg31/terminal-pet.git
cd terminal-pet
pip install -e .
```

**That's it.** No config needed. Just run:
```bash
terminal-pet
```

## Usage

### Start your pet

```bash
terminal-pet
```

That's it. Your pet will appear and start tracking your activity.

### Commands

| Command | Description |
|---------|-------------|
| `terminal-pet` | Open pet interface |
| `terminal-pet status` | Quick status check |
| `terminal-pet feed` | Manual feed (cheating!) |
| `terminal-pet play` | Play with your pet |
| `terminal-pet history` | View activity history |
| `terminal-pet resurrect` | Bring back a dead pet |

### Keyboard Shortcuts (in pet view)

| Key | Action |
|-----|--------|
| `f` | Feed |
| `p` | Play |
| `s` | Sleep mode |
| `q` | Quit (pet keeps living) |
| `?` | Help |

## How It Works

terminal-pet watches your git activity in the background:

| Activity | Effect |
|----------|--------|
| `git commit` | +20 hunger, +10 happiness |
| `git push` | +10 happiness, +5 energy |
| `git pull` | +5 happiness |
| Long coding session (2hr+) | -10 energy (tired together) |
| No activity for 24hr | -20 hunger, -15 happiness |
| No activity for 72hr | Pet enters critical state 😢 |
| No activity for 7 days | Pet dies 💀 |

### Resurrection

If your pet dies, don't panic! Start a 3-day commit streak to resurrect them:

```bash
terminal-pet resurrect
# Then commit for 3 consecutive days
```

Your pet will come back as a ghost 👻 until fully resurrected.

## Pet Types

Choose your companion:

| Pet | Name | Personality |
|-----|------|-------------|
| 🐣 | Blob | The classic. Cheerful and forgiving. |
| 🐱 | Pixel | Sassy. Judges your code quality. |
| 🤖 | Botty | Logical. Gives coding tips. |
| 🐙 | Octo | Git-obsessed. Loves branches. |
| 🦊 | Foxy | Sneaky. Hides easter eggs. |

```bash
terminal-pet --type pixel
```

## 📊 GitHub Badge

Show off your pet on your GitHub profile!

```bash
# Text format
terminal-pet badge

# Markdown table (for README)
terminal-pet badge --format markdown

# SVG badge (for profile)
terminal-pet badge --format svg -o badge.svg
```

**Example output:**

**🐣 Pip the Blob** | HAPPY 😊

| Hunger | Happiness | Energy |
|:------:|:---------:|:------:|
| 99% | 99% | 70% |

Copy the output and paste it in your GitHub profile README!

---

## Stats & Streaks

terminal-pet tracks your coding streaks:

```
🔥 Current Streak: 12 days
📈 Longest Streak: 34 days
🏆 Total Commits Fed: 847
💀 Deaths: 2
🐣 Resurrections: 2
```

## Philosophy

This project is intentionally simple and fun. It's not trying to:
- ❌ Be a serious productivity tool
- ❌ Guilt you into burnout
- ❌ Track anything beyond basic git activity

It IS trying to:
- ✅ Make you smile
- ✅ Add a bit of fun to your terminal
- ✅ Give you a reason to commit that WIP branch

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

Ideas we'd love:
- New pet types
- New activities to track
- Themes
- Mini-games
- Integrations

## License

MIT — do whatever you want with it.

---

Made with 💜 by [@apoorvgarg31](https://github.com/apoorvgarg31)

*Don't let your pet die. Commit something.* 🐣
