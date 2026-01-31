# Contributing to terminal-pet 🐣

Thanks for wanting to contribute! Here's how you can help.

## Ideas We'd Love

- **New pet types** — Design ASCII art for new pets
- **New activities to track** — What else could feed/play with the pet?
- **Themes** — Color schemes, ASCII styles
- **Mini-games** — Simple terminal games to play with your pet
- **Integrations** — VS Code extension, shell prompt integration, etc.

## Getting Started

1. Fork the repo
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/terminal-pet.git
   cd terminal-pet
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run the tests:
   ```bash
   pytest
   ```

## Making Changes

1. Create a branch:
   ```bash
   git checkout -b my-feature
   ```

2. Make your changes

3. Format your code:
   ```bash
   black src/
   ruff check src/ --fix
   ```

4. Test your changes:
   ```bash
   pytest
   terminal-pet status  # Manual testing
   ```

5. Commit and push:
   ```bash
   git add .
   git commit -m "Add my feature"
   git push origin my-feature
   ```

6. Open a Pull Request!

## Code Style

- We use [Black](https://github.com/psf/black) for formatting
- We use [Ruff](https://github.com/astral-sh/ruff) for linting
- Keep it simple and fun — this is a toy project!

## Adding a New Pet Type

1. Add ASCII art to `src/terminal_pet/display.py` in the `PET_ART` dictionary
2. Add the type to `PetType` enum in `src/terminal_pet/pet.py`
3. Add to CLI choices in `src/terminal_pet/cli.py`
4. Update README with the new pet

Example ASCII art format:
```python
"newpet": {
    PetMood.HAPPY: r"""
    Your ASCII
      art here
    """,
    # ... other moods
}
```

## Questions?

Open an issue! We're friendly. 🐣
