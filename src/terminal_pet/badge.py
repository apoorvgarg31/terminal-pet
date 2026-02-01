"""Badge generation for terminal-pet."""

from .pet import Pet, PetMood, EvolutionStage, EVOLUTION_EMOJI


# Mood emoji mapping (same as display.py)
MOOD_EMOJI = {
    PetMood.ECSTATIC: "\U0001F929",  # 🤩
    PetMood.HAPPY: "\U0001F60A",      # 😊
    PetMood.CONTENT: "\U0001F642",    # 🙂
    PetMood.NEUTRAL: "\U0001F610",    # 😐
    PetMood.SAD: "\U0001F622",        # 😢
    PetMood.HUNGRY: "\U0001F355",     # 🍕
    PetMood.TIRED: "\U0001F634",      # 😴
    PetMood.CRITICAL: "\U0001F630",   # 😰
    PetMood.DEAD: "\U0001F480",       # 💀
    PetMood.GHOST: "\U0001F47B",      # 👻
}

# Mood colors for badge
MOOD_COLORS = {
    PetMood.ECSTATIC: "#22c55e",  # green-500
    PetMood.HAPPY: "#4ade80",      # green-400
    PetMood.CONTENT: "#86efac",    # green-300
    PetMood.NEUTRAL: "#fbbf24",    # amber-400
    PetMood.SAD: "#f59e0b",        # amber-500
    PetMood.HUNGRY: "#ef4444",     # red-500
    PetMood.TIRED: "#8b5cf6",      # violet-500
    PetMood.CRITICAL: "#dc2626",   # red-600
    PetMood.DEAD: "#6b7280",       # gray-500
    PetMood.GHOST: "#a855f7",      # purple-500
}


def generate_text_badge(pet: Pet) -> str:
    """Generate a plain text badge."""
    pet.apply_decay()

    mood = pet.mood
    emoji = MOOD_EMOJI.get(mood, "")
    mood_text = mood.value.upper()

    name = pet.state.name
    pet_type = pet.state.pet_type.title()
    stage = pet.evolution_stage
    stage_emoji = EVOLUTION_EMOJI.get(stage, "")
    stage_text = stage.value.upper()

    hunger = round(pet.state.hunger)
    happiness = round(pet.state.happiness)
    energy = round(pet.state.energy)

    if pet.is_dead and not pet.is_ghost:
        return f"\U0001F480 {name} the {pet_type} | {mood_text} | {stage_text} {stage_emoji}"

    line1 = f"{stage_emoji} {name} the {pet_type} | {mood_text} {emoji} | {stage_text}"
    line2 = f"Hunger: {hunger}% | Happiness: {happiness}% | Energy: {energy}%"
    line3 = f"Commits: {pet.state.total_commits}"

    return f"{line1}\n{line2}\n{line3}"


def generate_markdown_badge(pet: Pet) -> str:
    """Generate a markdown badge with instructions."""
    pet.apply_decay()

    mood = pet.mood
    emoji = MOOD_EMOJI.get(mood, "")
    mood_text = mood.value.upper()

    name = pet.state.name
    pet_type = pet.state.pet_type.title()
    stage = pet.evolution_stage
    stage_emoji = EVOLUTION_EMOJI.get(stage, "")
    stage_text = stage.value.upper()

    hunger = round(pet.state.hunger)
    happiness = round(pet.state.happiness)
    energy = round(pet.state.energy)

    lines = [
        "<!-- terminal-pet badge -->",
        f"**{stage_emoji} {name} the {pet_type}** | {mood_text} {emoji} | Stage: {stage_text}",
        "",
        f"| Hunger | Happiness | Energy | Commits |",
        f"|:------:|:---------:|:------:|:-------:|",
        f"| {hunger}% | {happiness}% | {energy}% | {pet.state.total_commits} |",
        "",
        "---",
        "*Powered by [terminal-pet](https://github.com/yourusername/terminal-pet)*",
    ]

    if pet.is_dead and not pet.is_ghost:
        lines = [
            "<!-- terminal-pet badge -->",
            f"**\U0001F480 {name} the {pet_type}** | DECEASED | Stage: {stage_text} {stage_emoji}",
            "",
            "*Rest in peace*",
            "",
            "---",
            "*Powered by [terminal-pet](https://github.com/yourusername/terminal-pet)*",
        ]

    return "\n".join(lines)


def _create_stat_bar_svg(value: int, x: int, y: int, width: int = 60) -> str:
    """Create an SVG stat bar."""
    filled_width = int(value / 100 * width)

    # Background bar (gray)
    bg = f'<rect x="{x}" y="{y}" width="{width}" height="8" rx="4" fill="#374151"/>'

    # Filled bar (gradient based on value)
    if value >= 70:
        fill_color = "#22c55e"  # green
    elif value >= 30:
        fill_color = "#fbbf24"  # amber
    else:
        fill_color = "#ef4444"  # red

    filled = f'<rect x="{x}" y="{y}" width="{filled_width}" height="8" rx="4" fill="{fill_color}"/>'

    return bg + filled


def generate_svg_badge(pet: Pet) -> str:
    """Generate a self-contained SVG badge."""
    pet.apply_decay()

    mood = pet.mood
    emoji = MOOD_EMOJI.get(mood, "")
    mood_text = mood.value.upper()
    mood_color = MOOD_COLORS.get(mood, "#6b7280")

    name = pet.state.name
    pet_type = pet.state.pet_type.title()
    stage = pet.evolution_stage
    stage_emoji = EVOLUTION_EMOJI.get(stage, "")
    stage_text = stage.value.upper()

    hunger = round(pet.state.hunger)
    happiness = round(pet.state.happiness)
    energy = round(pet.state.energy)
    total_commits = pet.state.total_commits

    # Badge dimensions
    width = 300
    height = 115

    if pet.is_dead and not pet.is_ghost:
        # Dead pet - simplified badge
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="70" viewBox="0 0 {width} 70">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1f2937"/>
      <stop offset="100%" style="stop-color:#111827"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="70" rx="8" fill="url(#bg)"/>
  <rect x="1" y="1" width="{width-2}" height="68" rx="7" fill="none" stroke="#6b7280" stroke-width="1"/>
  <text x="20" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="14" fill="#f9fafb">
    <tspan>\U0001F480 {name} the {pet_type}</tspan>
  </text>
  <text x="20" y="46" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="#9ca3af">DECEASED</text>
  <text x="20" y="62" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#9ca3af">Stage: {stage_text} {stage_emoji} | Commits: {total_commits}</text>
</svg>'''
        return svg

    # Generate stat bars
    hunger_bar = _create_stat_bar_svg(hunger, 75, 42)
    happiness_bar = _create_stat_bar_svg(happiness, 75, 58)
    energy_bar = _create_stat_bar_svg(energy, 75, 74)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1f2937"/>
      <stop offset="100%" style="stop-color:#111827"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" rx="8" fill="url(#bg)"/>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" rx="7" fill="none" stroke="{mood_color}" stroke-width="1"/>

  <!-- Header -->
  <text x="15" y="24" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#f9fafb">
    <tspan>{stage_emoji} {name} the {pet_type}</tspan>
  </text>

  <!-- Mood badge -->
  <rect x="210" y="10" width="70" height="20" rx="10" fill="{mood_color}"/>
  <text x="245" y="24" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#ffffff" text-anchor="middle">{mood_text}</text>

  <!-- Stats labels -->
  <text x="15" y="50" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#9ca3af">Hunger</text>
  <text x="15" y="66" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#9ca3af">Happy</text>
  <text x="15" y="82" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#9ca3af">Energy</text>

  <!-- Stat bars -->
  {hunger_bar}
  {happiness_bar}
  {energy_bar}

  <!-- Stat values -->
  <text x="145" y="50" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#d1d5db">{hunger}%</text>
  <text x="145" y="66" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#d1d5db">{happiness}%</text>
  <text x="145" y="82" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#d1d5db">{energy}%</text>

  <!-- Mood emoji -->
  <text x="260" y="75" font-family="system-ui, -apple-system, sans-serif" font-size="24">{emoji}</text>

  <!-- Evolution stage footer -->
  <text x="15" y="103" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#a78bfa">Stage: {stage_text} | Commits: {total_commits}</text>
</svg>'''

    return svg


def generate_badge(pet: Pet, format: str = "text") -> str:
    """Generate a badge in the specified format.

    Args:
        pet: The Pet instance
        format: One of "text", "markdown", or "svg"

    Returns:
        The badge content as a string
    """
    if format == "svg":
        return generate_svg_badge(pet)
    elif format == "markdown":
        return generate_markdown_badge(pet)
    else:
        return generate_text_badge(pet)
