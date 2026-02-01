"""Pet class and state management."""

import json
import threading
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional
import random


class PetType(Enum):
    """Available pet types."""
    BLOB = "blob"
    PIXEL = "pixel"
    BOTTY = "botty"
    OCTO = "octo"
    FOXY = "foxy"


class PetMood(Enum):
    """Pet mood states."""
    ECSTATIC = "ecstatic"
    HAPPY = "happy"
    CONTENT = "content"
    NEUTRAL = "neutral"
    SAD = "sad"
    HUNGRY = "hungry"
    TIRED = "tired"
    CRITICAL = "critical"
    DEAD = "dead"
    GHOST = "ghost"


class EvolutionStage(Enum):
    """Pet evolution stages based on total commits fed."""
    EGG = "egg"        # 0-9 commits
    BABY = "baby"      # 10-49 commits
    TEEN = "teen"      # 50-199 commits
    ADULT = "adult"    # 200-499 commits
    ELDER = "elder"    # 500+ commits


# Evolution stage thresholds (commits needed to reach each stage)
EVOLUTION_THRESHOLDS = {
    EvolutionStage.EGG: 0,
    EvolutionStage.BABY: 10,
    EvolutionStage.TEEN: 50,
    EvolutionStage.ADULT: 200,
    EvolutionStage.ELDER: 500,
}

# Evolution stage emojis
EVOLUTION_EMOJI = {
    EvolutionStage.EGG: "🥚",
    EvolutionStage.BABY: "🐣",
    EvolutionStage.TEEN: "🐥",
    EvolutionStage.ADULT: "🐤",
    EvolutionStage.ELDER: "👑",
}


@dataclass
class PetState:
    """Represents the current state of a pet."""
    name: str = "Pip"
    pet_type: str = "blob"

    # Stats (0-100)
    hunger: int = 80
    happiness: int = 80
    energy: int = 80

    # Lifecycle
    born_at: float = field(default_factory=time.time)
    last_fed: float = field(default_factory=time.time)
    last_played: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    last_decay_applied: float = field(default_factory=time.time)
    died_at: Optional[float] = None
    resurrect_streak: int = 0
    
    # Stats
    total_commits: int = 0
    total_deaths: int = 0
    total_resurrections: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    last_commit_date: Optional[str] = None
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "PetState":
        return cls(**data)


class Pet:
    """A terminal pet that feeds on git commits."""

    STATE_FILE = Path.home() / ".terminal-pet" / "state.json"

    # Decay rates (per hour) - tuned for ~7 day survival from full stats
    # 100 hunger / 0.6 per hour = ~166 hours = ~7 days
    HUNGER_DECAY = 0.6
    HAPPINESS_DECAY = 0.4
    ENERGY_DECAY = 0.2

    # Thread lock for state access
    _lock = threading.Lock()
    
    # Activity effects
    EFFECTS = {
        "commit": {"hunger": 20, "happiness": 10, "energy": 5},
        "push": {"hunger": 5, "happiness": 15, "energy": 5},
        "pull": {"hunger": 0, "happiness": 5, "energy": 0},
        "test": {"hunger": 0, "happiness": 20, "energy": -5},
        "feed": {"hunger": 30, "happiness": 5, "energy": 0},
        "play": {"hunger": -5, "happiness": 25, "energy": -10},
        "sleep": {"hunger": -5, "happiness": 5, "energy": 30},
    }
    
    def __init__(self, state: Optional[PetState] = None):
        self.state = state or self._load_state() or PetState()
        self._ensure_state_dir()
    
    def _ensure_state_dir(self):
        """Ensure the state directory exists."""
        self.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_state(self) -> Optional[PetState]:
        """Load pet state from file."""
        if self.STATE_FILE.exists():
            try:
                with open(self.STATE_FILE) as f:
                    data = json.load(f)
                return PetState.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                return None
        return None
    
    def save(self):
        """Save pet state to file."""
        self._ensure_state_dir()
        with self._lock:
            with open(self.STATE_FILE, "w") as f:
                json.dump(self.state.to_dict(), f, indent=2)
    
    def apply_decay(self):
        """Apply time-based stat decay."""
        if self.is_dead:
            return

        with self._lock:
            now = time.time()
            hours_since_decay = (now - self.state.last_decay_applied) / 3600

            # Apply decay based on time since last decay was applied
            self.state.hunger = max(0, self.state.hunger - hours_since_decay * self.HUNGER_DECAY)
            self.state.happiness = max(0, self.state.happiness - hours_since_decay * self.HAPPINESS_DECAY)
            self.state.energy = max(0, self.state.energy - hours_since_decay * self.ENERGY_DECAY)

            # Update last decay time
            self.state.last_decay_applied = now

            # Check for death - pet dies when hunger reaches 0
            if self.state.hunger <= 0:
                self._die()
    
    def _die(self):
        """Pet dies from neglect."""
        if not self.is_dead:
            self.state.died_at = time.time()
            self.state.total_deaths += 1
            self.state.current_streak = 0
    
    @property
    def is_dead(self) -> bool:
        """Check if pet is dead."""
        return self.state.died_at is not None
    
    @property
    def is_ghost(self) -> bool:
        """Check if pet is in ghost resurrection mode."""
        return self.is_dead and self.state.resurrect_streak > 0
    
    @property
    def mood(self) -> PetMood:
        """Determine current mood based on stats."""
        if self.is_dead:
            if self.is_ghost:
                return PetMood.GHOST
            return PetMood.DEAD
        
        avg = (self.state.hunger + self.state.happiness + self.state.energy) / 3
        
        if avg >= 90:
            return PetMood.ECSTATIC
        elif avg >= 70:
            return PetMood.HAPPY
        elif avg >= 50:
            return PetMood.CONTENT
        elif avg >= 30:
            return PetMood.NEUTRAL
        elif self.state.hunger < 20:
            return PetMood.HUNGRY
        elif self.state.energy < 20:
            return PetMood.TIRED
        elif avg < 20:
            return PetMood.CRITICAL
        else:
            return PetMood.SAD
    
    @property
    def age(self) -> timedelta:
        """Get pet's age."""
        end_time = self.state.died_at or time.time()
        return timedelta(seconds=end_time - self.state.born_at)

    @property
    def evolution_stage(self) -> EvolutionStage:
        """Determine evolution stage based on total commits."""
        commits = self.state.total_commits
        if commits >= EVOLUTION_THRESHOLDS[EvolutionStage.ELDER]:
            return EvolutionStage.ELDER
        elif commits >= EVOLUTION_THRESHOLDS[EvolutionStage.ADULT]:
            return EvolutionStage.ADULT
        elif commits >= EVOLUTION_THRESHOLDS[EvolutionStage.TEEN]:
            return EvolutionStage.TEEN
        elif commits >= EVOLUTION_THRESHOLDS[EvolutionStage.BABY]:
            return EvolutionStage.BABY
        else:
            return EvolutionStage.EGG

    @property
    def evolution_emoji(self) -> str:
        """Get the emoji for current evolution stage."""
        return EVOLUTION_EMOJI.get(self.evolution_stage, "🥚")

    @property
    def commits_to_next_evolution(self) -> Optional[int]:
        """Get the number of commits needed to reach the next evolution stage."""
        stage = self.evolution_stage
        if stage == EvolutionStage.ELDER:
            return None  # Already at max stage

        # Get next stage threshold
        stages = list(EvolutionStage)
        current_index = stages.index(stage)
        next_stage = stages[current_index + 1]
        return EVOLUTION_THRESHOLDS[next_stage] - self.state.total_commits
    
    @property
    def age_str(self) -> str:
        """Get pet's age as a human-readable string."""
        age = self.age
        days = age.days
        hours = age.seconds // 3600
        
        if days > 0:
            return f"{days} day{'s' if days != 1 else ''}, {hours} hour{'s' if hours != 1 else ''}"
        elif hours > 0:
            return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            minutes = age.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
    
    def on_activity(self, activity: str) -> Optional[EvolutionStage]:
        """Handle an activity event. Returns new evolution stage if evolved, None otherwise."""
        if activity not in self.EFFECTS:
            return None

        effects = self.EFFECTS[activity]

        # Handle resurrection
        if self.is_dead and activity == "commit":
            self._handle_resurrect_commit()
            return None

        if self.is_dead:
            return None

        evolved_to = None
        with self._lock:
            # Apply effects
            self.state.hunger = min(100, max(0, self.state.hunger + effects.get("hunger", 0)))
            self.state.happiness = min(100, max(0, self.state.happiness + effects.get("happiness", 0)))
            self.state.energy = min(100, max(0, self.state.energy + effects.get("energy", 0)))

            self.state.last_activity = time.time()

            if activity == "commit":
                evolved_to = self._handle_commit()
            elif activity == "feed":
                self.state.last_fed = time.time()
            elif activity == "play":
                self.state.last_played = time.time()

        self.save()
        return evolved_to
    
    def _handle_commit(self) -> Optional[EvolutionStage]:
        """Handle a commit event. Returns new evolution stage if evolved, None otherwise."""
        old_stage = self.evolution_stage
        self.state.total_commits += 1
        new_stage = self.evolution_stage

        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        if self.state.last_commit_date == today:
            pass  # Already committed today
        elif self.state.last_commit_date == yesterday:
            self.state.current_streak += 1
        else:
            self.state.current_streak = 1

        self.state.last_commit_date = today
        self.state.longest_streak = max(self.state.longest_streak, self.state.current_streak)

        # Return new stage if evolution occurred
        if new_stage != old_stage:
            return new_stage
        return None
    
    def _handle_resurrect_commit(self):
        """Handle a commit while dead (resurrection progress)."""
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        if self.state.last_commit_date == today:
            return  # Already committed today
        elif self.state.last_commit_date == yesterday or self.state.resurrect_streak == 0:
            self.state.resurrect_streak += 1
        else:
            self.state.resurrect_streak = 1  # Streak broken, restart
        
        self.state.last_commit_date = today
        self.state.total_commits += 1
        
        # Check if resurrection complete
        if self.state.resurrect_streak >= 3:
            self._resurrect()
        
        self.save()
    
    def _resurrect(self):
        """Resurrect the pet."""
        self.state.died_at = None
        self.state.resurrect_streak = 0
        self.state.hunger = 50
        self.state.happiness = 50
        self.state.energy = 50
        self.state.total_resurrections += 1
        self.state.current_streak = 3
    
    def start_resurrection(self):
        """Start the resurrection process."""
        if self.is_dead and not self.is_ghost:
            self.state.resurrect_streak = 0
            self.save()
    
    def get_message(self) -> str:
        """Get a contextual message from the pet."""
        mood = self.mood
        
        messages = {
            PetMood.ECSTATIC: [
                "I LOVE YOU! 🎉",
                "Best. Day. EVER!",
                "*does a happy dance*",
                "You're on fire today! 🔥",
            ],
            PetMood.HAPPY: [
                "Life is good! 😊",
                "Thanks for the commits!",
                "*wags tail*",
                "You're awesome!",
            ],
            PetMood.CONTENT: [
                "Doing alright!",
                "Keep up the good work!",
                "*purrs contentedly*",
                "Nice and cozy here.",
            ],
            PetMood.NEUTRAL: [
                "Hey there.",
                "What's up?",
                "*looks around*",
                "Could use some attention...",
            ],
            PetMood.SAD: [
                "I miss you... 😢",
                "It's been a while...",
                "*sighs*",
                "Remember me?",
            ],
            PetMood.HUNGRY: [
                "SO HUNGRY! 🍕",
                "Feed me! (commit something!)",
                "*stomach growls*",
                "Is that... a commit I smell?",
            ],
            PetMood.TIRED: [
                "So... tired... 😴",
                "*yawns*",
                "Need... sleep...",
                "Long day, huh?",
            ],
            PetMood.CRITICAL: [
                "I'm not doing so well...",
                "Please... commit something...",
                "*weakly waves*",
                "Don't let me die! 😰",
            ],
            PetMood.DEAD: [
                "...",
                "💀",
                "*silence*",
                "I trusted you...",
            ],
            PetMood.GHOST: [
                "I'm still here... barely",
                "*floats spookily* 👻",
                f"Resurrection: {self.state.resurrect_streak}/3 days",
                "Keep committing to bring me back!",
            ],
        }
        
        return random.choice(messages.get(mood, ["..."]))
