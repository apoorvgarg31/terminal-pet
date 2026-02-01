"""ASCII art and terminal display for the pet."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich import box

from .pet import Pet, PetMood, PetType, EvolutionStage, EVOLUTION_EMOJI


# ASCII art for different pet types and moods
PET_ART = {
    "blob": {
        PetMood.ECSTATIC: r"""
   \(^o^)/
    \_■_/
    /| |\
   / | | \
        """,
        PetMood.HAPPY: r"""
    ◠ ◡ ◠
     \_/
    /|■|\
     / \
        """,
        PetMood.CONTENT: r"""
    ◠ ‿ ◠
     \_/
    /|■|\
     / \
        """,
        PetMood.NEUTRAL: r"""
    ◠ _ ◠
     \_/
    /|■|\
     / \
        """,
        PetMood.SAD: r"""
    ◠ ︵ ◠
     \_/
    /|■|\
     / \
        """,
        PetMood.HUNGRY: r"""
    ◠ o ◠
     \○/
    /|■|\
     / \
        """,
        PetMood.TIRED: r"""
    - _ -
     \_/
    /|■|\
     / \
        """,
        PetMood.CRITICAL: r"""
    x _ x
     \_/
    /|■|\
     / \
        """,
        PetMood.DEAD: r"""
    x _ x
     \_/
    /|■|\   💀
     / \
        """,
        PetMood.GHOST: r"""
   ~◠ ◡ ◠~
    ~\_/~   👻
   ~/|■|\~
    ~~~~~
        """,
    },
    "pixel": {
        PetMood.ECSTATIC: r"""
    /\_/\  
   ( ^.^ ) ~♪
    > ^ <
        """,
        PetMood.HAPPY: r"""
    /\_/\  
   ( ^.^ )
    > ^ <
        """,
        PetMood.CONTENT: r"""
    /\_/\  
   ( -.- )
    > ^ <
        """,
        PetMood.NEUTRAL: r"""
    /\_/\  
   ( o.o )
    > ^ <
        """,
        PetMood.SAD: r"""
    /\_/\  
   ( ;.; )
    > ^ <
        """,
        PetMood.HUNGRY: r"""
    /\_/\  
   ( O.O ) !
    > ^ <
        """,
        PetMood.TIRED: r"""
    /\_/\  
   ( -.- ) zzz
    > ^ <
        """,
        PetMood.CRITICAL: r"""
    /\_/\  
   ( x.x )
    > ^ <
        """,
        PetMood.DEAD: r"""
    /\_/\  💀
   ( x.x )
    > ^ <
        """,
        PetMood.GHOST: r"""
   ~/\_/\~ 👻
   ( o.o )
   ~>~~~<~
        """,
    },
    "botty": {
        PetMood.ECSTATIC: r"""
    [^_^]
   -|===|-  ✓✓
    /   \
        """,
        PetMood.HAPPY: r"""
    [^_^]
   -|===|-
    /   \
        """,
        PetMood.CONTENT: r"""
    [=_=]
   -|===|-
    /   \
        """,
        PetMood.NEUTRAL: r"""
    [o_o]
   -|===|-
    /   \
        """,
        PetMood.SAD: r"""
    [T_T]
   -|===|-
    /   \
        """,
        PetMood.HUNGRY: r"""
    [O_O]
   -|===|-  ⚠
    /   \
        """,
        PetMood.TIRED: r"""
    [-_-]
   -|===|-  zzz
    /   \
        """,
        PetMood.CRITICAL: r"""
    [X_X]
   -|===|-  ⚠⚠
    /   \
        """,
        PetMood.DEAD: r"""
    [X_X]  💀
   -|===|-
    /   \
        """,
        PetMood.GHOST: r"""
   ~[o_o]~ 👻
   ~|===|~
   ~/   \~
        """,
    },
    "octo": {
        PetMood.ECSTATIC: r"""
     ,---.
    ( ^o^ )  🔀
   //|||||\\
        """,
        PetMood.HAPPY: r"""
     ,---.
    ( ^.^ )
   //|||||\\
        """,
        PetMood.CONTENT: r"""
     ,---.
    ( -.- )
   //|||||\\
        """,
        PetMood.NEUTRAL: r"""
     ,---.
    ( o.o )
   //|||||\\
        """,
        PetMood.SAD: r"""
     ,---.
    ( ;-; )
   //|||||\\
        """,
        PetMood.HUNGRY: r"""
     ,---.
    ( O.O )  !
   //|||||\\
        """,
        PetMood.TIRED: r"""
     ,---.
    ( -.- ) zzz
   //|||||\\
        """,
        PetMood.CRITICAL: r"""
     ,---.
    ( x.x )
   //|||||\\
        """,
        PetMood.DEAD: r"""
     ,---.   💀
    ( x.x )
   //|||||\\
        """,
        PetMood.GHOST: r"""
    ~,---,~ 👻
   ~( o.o )~
   ~//|||\\~
        """,
    },
    "foxy": {
        PetMood.ECSTATIC: r"""
    /\   /\
   (  ^w^  ) ~♥
    \\_v_//
        """,
        PetMood.HAPPY: r"""
    /\   /\
   (  ^w^  )
    \\_v_//
        """,
        PetMood.CONTENT: r"""
    /\   /\
   (  -w-  )
    \\_v_//
        """,
        PetMood.NEUTRAL: r"""
    /\   /\
   (  o.o  )
    \\_v_//
        """,
        PetMood.SAD: r"""
    /\   /\
   (  ;w;  )
    \\_v_//
        """,
        PetMood.HUNGRY: r"""
    /\   /\
   (  OwO  )  ?
    \\_v_//
        """,
        PetMood.TIRED: r"""
    /\   /\
   (  -.-  ) zzz
    \\_v_//
        """,
        PetMood.CRITICAL: r"""
    /\   /\
   (  x.x  )
    \\_v_//
        """,
        PetMood.DEAD: r"""
    /\   /\  💀
   (  x.x  )
    \\_v_//
        """,
        PetMood.GHOST: r"""
   ~/\~~~~/\~ 👻
   (  o.o  )
   ~\\_v_//~
        """,
    },
}

MOOD_EMOJI = {
    PetMood.ECSTATIC: "🤩",
    PetMood.HAPPY: "😊",
    PetMood.CONTENT: "🙂",
    PetMood.NEUTRAL: "😐",
    PetMood.SAD: "😢",
    PetMood.HUNGRY: "🍕",
    PetMood.TIRED: "😴",
    PetMood.CRITICAL: "😰",
    PetMood.DEAD: "💀",
    PetMood.GHOST: "👻",
}


def get_pet_art(pet: Pet) -> str:
    """Get ASCII art for a pet based on its type and mood."""
    pet_type = pet.state.pet_type
    mood = pet.mood
    
    if pet_type not in PET_ART:
        pet_type = "blob"
    
    art_dict = PET_ART[pet_type]
    return art_dict.get(mood, art_dict[PetMood.NEUTRAL])


def create_stat_bar(value: int, width: int = 10, filled: str = "█", empty: str = "░") -> str:
    """Create a visual stat bar."""
    filled_count = int(value / 100 * width)
    empty_count = width - filled_count
    return f"{filled * filled_count}{empty * empty_count}"


def create_pet_panel(pet: Pet) -> Panel:
    """Create a rich panel displaying the pet."""
    pet.apply_decay()

    mood = pet.mood
    art = get_pet_art(pet)
    message = pet.get_message()
    emoji = MOOD_EMOJI.get(mood, "")
    stage = pet.evolution_stage
    stage_emoji = pet.evolution_emoji

    # Build the display
    content = Text()
    content.append(art + "\n", style="cyan")
    content.append(f'"{message}"\n\n', style="italic yellow")

    # Stats
    if not pet.is_dead or pet.is_ghost:
        content.append(f"hunger:    {create_stat_bar(pet.state.hunger)}  {round(pet.state.hunger)}%\n",
                      style="green" if pet.state.hunger > 30 else "red")
        content.append(f"happiness: {create_stat_bar(pet.state.happiness)}  {round(pet.state.happiness)}%\n",
                      style="green" if pet.state.happiness > 30 else "red")
        content.append(f"energy:    {create_stat_bar(pet.state.energy)}  {round(pet.state.energy)}%\n",
                      style="green" if pet.state.energy > 30 else "red")

    content.append(f"\n{mood.value.upper()} {emoji}\n", style="bold")

    # Evolution stage info
    commits_to_next = pet.commits_to_next_evolution
    if commits_to_next is not None:
        content.append(f"Stage: {stage.value.upper()} {stage_emoji} ({commits_to_next} commits to evolve)\n", style="magenta")
    else:
        content.append(f"Stage: {stage.value.upper()} {stage_emoji} (MAX)\n", style="bold magenta")

    title = f"{stage_emoji} {pet.state.name} the {pet.state.pet_type.title()}"
    subtitle = f"Age: {pet.age_str} | Commits: {pet.state.total_commits}"

    if pet.is_dead and not pet.is_ghost:
        title = f"💀 {pet.state.name} (deceased)"
        subtitle = f"Lived for: {pet.age_str}"
    elif pet.is_ghost:
        title = f"👻 {pet.state.name} (ghost)"
        subtitle = f"Resurrection: {pet.state.resurrect_streak}/3 days"

    return Panel(
        content,
        title=title,
        subtitle=subtitle,
        border_style="cyan" if not pet.is_dead else "red",
        box=box.ROUNDED,
    )


def create_stats_panel(pet: Pet) -> Panel:
    """Create a panel showing pet statistics."""
    table = Table(show_header=False, box=None)
    table.add_column("Stat", style="cyan")
    table.add_column("Value", style="yellow")
    
    table.add_row("🔥 Current Streak", f"{pet.state.current_streak} days")
    table.add_row("📈 Longest Streak", f"{pet.state.longest_streak} days")
    table.add_row("🍕 Total Commits Fed", str(pet.state.total_commits))
    table.add_row("💀 Deaths", str(pet.state.total_deaths))
    table.add_row("🐣 Resurrections", str(pet.state.total_resurrections))
    
    return Panel(table, title="📊 Stats", border_style="blue", box=box.ROUNDED)


def create_help_panel() -> Panel:
    """Create a panel showing keyboard shortcuts."""
    help_text = """
[cyan]f[/] - Feed your pet
[cyan]p[/] - Play with your pet
[cyan]s[/] - Put pet to sleep
[cyan]r[/] - Start resurrection (if dead)
[cyan]q[/] - Quit (pet keeps living)
[cyan]?[/] - Show this help
    """
    return Panel(help_text.strip(), title="⌨️ Controls", border_style="green", box=box.ROUNDED)


def render_full_view(pet: Pet, console: Console):
    """Render the full pet view."""
    layout = Layout()
    
    layout.split_column(
        Layout(name="pet", ratio=2),
        Layout(name="bottom", ratio=1),
    )
    
    layout["bottom"].split_row(
        Layout(name="stats"),
        Layout(name="help"),
    )
    
    layout["pet"].update(create_pet_panel(pet))
    layout["stats"].update(create_stats_panel(pet))
    layout["help"].update(create_help_panel())
    
    console.print(layout)


def render_status(pet: Pet, console: Console):
    """Render a quick status view."""
    pet.apply_decay()
    console.print(create_pet_panel(pet))


def render_evolution_notification(stage: EvolutionStage, console: Console):
    """Render an evolution achievement notification."""
    stage_emoji = EVOLUTION_EMOJI.get(stage, "")
    stage_name = stage.value.upper()

    messages = {
        EvolutionStage.EGG: "Your pet has hatched... wait, it's still an egg!",
        EvolutionStage.BABY: "Your egg has hatched! Welcome to the world, little one!",
        EvolutionStage.TEEN: "Your pet is growing up! It's now a teenager!",
        EvolutionStage.ADULT: "Your pet has reached adulthood! So proud!",
        EvolutionStage.ELDER: "Your pet has achieved ELDER status! A true legend!",
    }

    message = messages.get(stage, f"Your pet evolved to {stage_name}!")

    content = Text()
    content.append("\n")
    content.append("  ★ EVOLUTION! ★  \n", style="bold yellow")
    content.append("\n")
    content.append(f"    {stage_emoji} {stage_name} {stage_emoji}\n", style="bold magenta")
    content.append("\n")
    content.append(f"    {message}\n", style="italic cyan")
    content.append("\n")

    panel = Panel(
        content,
        title="🎉 Achievement Unlocked!",
        border_style="yellow",
        box=box.DOUBLE,
    )
    console.print(panel)
