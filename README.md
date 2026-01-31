<p align="center">
  <img src="https://raw.githubusercontent.com/apoorvgarg31/terminal-pet/main/assets/banner.png" alt="terminal-pet banner" width="600">
</p>

<h1 align="center">🐣 terminal-pet</h1>

<p align="center">
  <strong>A tamagotchi that lives in your terminal and feeds on your git commits.</strong>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#pet-types">Pet Types</a> •
  <a href="#contributing">Contributing</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/github/stars/apoorvgarg31/terminal-pet?style=social" alt="GitHub Stars">
</p>

---

## What is this?

**terminal-pet** is a virtual pet that lives in your terminal. But here's the twist: **your coding activity keeps it alive.**

- 🍕 **Git commits** = Feeding your pet
- 🎮 **Running tests** = Playing with your pet  
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

```bash
pip install terminal-pet
```

Or install from source:

```bash
git clone https://github.com/apoorvgarg31/terminal-pet.git
cd terminal-pet
pip install -e .
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
| Run tests (`pytest`, `npm test`, etc.) | +15 happiness (playing!) |
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

## Customization

Create `~/.terminal-pet/config.yaml`:

```yaml
pet:
  name: "Sir Commits-a-Lot"
  type: "blob"
  
tracking:
  repos:
    - ~/projects/*
    - ~/work/*
  
notifications:
  enabled: true
  critical_only: false
  
theme: "retro"  # retro, modern, minimal, rainbow
```

## Stats & Streaks

terminal-pet tracks your coding streaks:

```
🔥 Current Streak: 12 days
📈 Longest Streak: 34 days
🏆 Total Commits Fed: 847
💀 Deaths: 2
🐣 Resurrections: 2
```

## Integrations

### GitHub Actions Badge

Add your pet's status to your GitHub profile:

```markdown
![terminal-pet](https://terminal-pet.dev/badge/YOUR_USERNAME)
```

### VS Code Extension (coming soon)

Your pet in the status bar!

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

<p align="center">
  Made with 💜 by <a href="https://github.com/apoorvgarg31">@apoorvgarg31</a>
</p>

<p align="center">
  <i>Don't let your pet die. Commit something.</i> 🐣
</p>
