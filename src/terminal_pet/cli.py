"""CLI interface for terminal-pet."""

import sys
import time
import threading
import click
from rich.console import Console
from rich.live import Live

from .pet import Pet, PetState, PetType
from .display import (
    create_pet_panel,
    create_stats_panel,
    render_full_view,
    render_status,
)
from .tracker import GitTracker, poll_for_commits


console = Console()


@click.group(invoke_without_command=True)
@click.option("--type", "pet_type", type=click.Choice(["blob", "pixel", "botty", "octo", "foxy"]),
              help="Pet type (only for new pets)")
@click.option("--name", help="Pet name (only for new pets)")
@click.pass_context
def main(ctx, pet_type, name):
    """🐣 terminal-pet - A tamagotchi that feeds on your git commits."""
    if ctx.invoked_subcommand is None:
        # Default: show interactive view
        run_interactive(pet_type, name)


def run_interactive(pet_type: str = None, name: str = None):
    """Run the interactive pet view."""
    pet = Pet()
    
    # Set up new pet if needed
    if pet_type and pet.state.total_commits == 0:
        pet.state.pet_type = pet_type
    if name and pet.state.total_commits == 0:
        pet.state.name = name
    pet.save()
    
    # Set up git tracking
    def on_git_activity(activity: str):
        pet.on_activity(activity)
    
    tracker = GitTracker(on_git_activity)
    
    # Start backup polling in background
    poll_thread = threading.Thread(target=poll_for_commits, args=(pet,), daemon=True)
    
    console.clear()
    console.print("\n[bold cyan]🐣 terminal-pet[/bold cyan]")
    console.print("[dim]Press 'q' to quit, '?' for help[/dim]\n")
    
    try:
        tracker.start()
        poll_thread.start()
        
        with Live(create_pet_panel(pet), refresh_per_second=0.5, console=console) as live:
            while True:
                pet.apply_decay()
                live.update(create_pet_panel(pet))
                
                # Check for keyboard input (non-blocking)
                if sys.stdin in select_stdin():
                    key = sys.stdin.read(1).lower()
                    
                    if key == "q":
                        break
                    elif key == "f":
                        pet.on_activity("feed")
                        console.print("[green]🍕 Fed your pet![/green]")
                    elif key == "p":
                        pet.on_activity("play")
                        console.print("[green]🎮 Played with your pet![/green]")
                    elif key == "s":
                        pet.on_activity("sleep")
                        console.print("[green]😴 Pet is resting...[/green]")
                    elif key == "r":
                        if pet.is_dead:
                            pet.start_resurrection()
                            console.print("[yellow]👻 Resurrection started! Commit for 3 days to bring your pet back.[/yellow]")
                    elif key == "?":
                        console.print("""
[bold]Commands:[/bold]
  [cyan]f[/cyan] - Feed your pet
  [cyan]p[/cyan] - Play with your pet  
  [cyan]s[/cyan] - Put pet to sleep
  [cyan]r[/cyan] - Start resurrection (if dead)
  [cyan]q[/cyan] - Quit
                        """)
                
                time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        tracker.stop()
        pet.save()
        console.print("\n[dim]Your pet is still alive in the background. Come back soon! 👋[/dim]")


def select_stdin():
    """Non-blocking stdin check."""
    import select
    try:
        return select.select([sys.stdin], [], [], 0)[0]
    except Exception:
        return []


@main.command()
def status():
    """Show a quick status of your pet."""
    pet = Pet()
    render_status(pet, console)


@main.command()
def feed():
    """Feed your pet manually."""
    pet = Pet()
    if pet.is_dead and not pet.is_ghost:
        console.print("[red]Your pet is dead. Use 'terminal-pet resurrect' first.[/red]")
        return
    
    pet.on_activity("feed")
    console.print("[green]🍕 Fed your pet![/green]")
    render_status(pet, console)


@main.command()
def play():
    """Play with your pet."""
    pet = Pet()
    if pet.is_dead and not pet.is_ghost:
        console.print("[red]Your pet is dead. Use 'terminal-pet resurrect' first.[/red]")
        return
    
    pet.on_activity("play")
    console.print("[green]🎮 Played with your pet![/green]")
    render_status(pet, console)


@main.command()
def resurrect():
    """Start the resurrection process for a dead pet."""
    pet = Pet()
    
    if not pet.is_dead:
        console.print("[yellow]Your pet is alive! No resurrection needed.[/yellow]")
        return
    
    if pet.is_ghost:
        console.print(f"[yellow]👻 Resurrection in progress: {pet.state.resurrect_streak}/3 days[/yellow]")
        console.print("[dim]Keep committing daily to bring your pet back![/dim]")
        return
    
    pet.start_resurrection()
    console.print("[cyan]👻 Resurrection started![/cyan]")
    console.print("[dim]Commit code for 3 consecutive days to bring your pet back to life.[/dim]")
    render_status(pet, console)


@main.command()
def history():
    """Show pet activity history and stats."""
    pet = Pet()
    console.print(create_stats_panel(pet))


@main.command()
@click.option("--name", prompt="Pet name", help="Name for your new pet")
@click.option("--type", "pet_type", 
              type=click.Choice(["blob", "pixel", "botty", "octo", "foxy"]),
              prompt="Pet type",
              help="Type of pet")
def new(name: str, pet_type: str):
    """Create a new pet (warning: replaces existing pet!)."""
    if Pet.STATE_FILE.exists():
        if not click.confirm("This will replace your existing pet. Continue?"):
            return
    
    state = PetState(name=name, pet_type=pet_type)
    pet = Pet(state)
    pet.save()
    
    console.print(f"[green]🐣 Welcome {name} the {pet_type}![/green]")
    render_status(pet, console)


@main.command()
def reset():
    """Reset everything (delete your pet permanently)."""
    if not click.confirm("This will permanently delete your pet. Are you sure?", abort=True):
        return
    
    if Pet.STATE_FILE.exists():
        Pet.STATE_FILE.unlink()
    
    console.print("[yellow]Pet deleted. Run 'terminal-pet' to create a new one.[/yellow]")


if __name__ == "__main__":
    main()
