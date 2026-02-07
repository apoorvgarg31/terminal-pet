"""Achievement system for terminal-pet."""

import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Callable


class AchievementTier(Enum):
    """Achievement rarity tiers."""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


# Tier display config
TIER_EMOJI = {
    AchievementTier.BRONZE: "🥉",
    AchievementTier.SILVER: "🥈",
    AchievementTier.GOLD: "🥇",
    AchievementTier.PLATINUM: "💎",
    AchievementTier.DIAMOND: "👑",
}

TIER_COLOR = {
    AchievementTier.BRONZE: "#cd7f32",
    AchievementTier.SILVER: "#c0c0c0",
    AchievementTier.GOLD: "#ffd700",
    AchievementTier.PLATINUM: "#e5e4e2",
    AchievementTier.DIAMOND: "#b9f2ff",
}


@dataclass
class Achievement:
    """Definition of a single achievement."""
    id: str
    name: str
    description: str
    tier: AchievementTier
    icon: str
    hidden: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tier": self.tier.value,
            "icon": self.icon,
            "hidden": self.hidden,
        }


@dataclass
class EarnedAchievement:
    """Record of an achievement earned by the user."""
    achievement_id: str
    earned_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "EarnedAchievement":
        return cls(**data)


# ─── Achievement Definitions ────────────────────────────────────────

ACHIEVEMENTS: Dict[str, Achievement] = {}


def _register(achievement: Achievement) -> Achievement:
    """Register an achievement in the global registry."""
    ACHIEVEMENTS[achievement.id] = achievement
    return achievement


# ── Commit Milestones ──
_register(Achievement("first_commit", "First Commit", "Feed your pet for the first time", AchievementTier.BRONZE, "🎉"))
_register(Achievement("ten_commits", "Getting Started", "Reach 10 total commits", AchievementTier.BRONZE, "📝"))
_register(Achievement("twenty_five_commits", "Quarter Century", "Reach 25 total commits", AchievementTier.BRONZE, "🔢"))
_register(Achievement("fifty_commits", "Half Century", "Reach 50 total commits", AchievementTier.SILVER, "🎯"))
_register(Achievement("hundred_commits", "Century Club", "Reach 100 total commits", AchievementTier.GOLD, "💯"))
_register(Achievement("two_fifty_commits", "Prolific Coder", "Reach 250 total commits", AchievementTier.GOLD, "📚"))
_register(Achievement("five_hundred_commits", "Code Machine", "Reach 500 total commits", AchievementTier.PLATINUM, "⚙️"))
_register(Achievement("thousand_commits", "Legendary", "Reach 1000 total commits", AchievementTier.DIAMOND, "🏆"))

# ── Streak Achievements ──
_register(Achievement("streak_3", "Consistent", "Maintain a 3-day commit streak", AchievementTier.BRONZE, "🔥"))
_register(Achievement("streak_7", "Streak Master", "Maintain a 7-day commit streak", AchievementTier.SILVER, "🔥"))
_register(Achievement("streak_14", "Two Week Warrior", "Maintain a 14-day commit streak", AchievementTier.SILVER, "⚡"))
_register(Achievement("streak_30", "Monthly Marathon", "Maintain a 30-day commit streak", AchievementTier.GOLD, "🏃"))
_register(Achievement("streak_60", "Iron Will", "Maintain a 60-day commit streak", AchievementTier.PLATINUM, "🦾"))
_register(Achievement("streak_100", "Unstoppable", "Maintain a 100-day commit streak", AchievementTier.DIAMOND, "💫"))
_register(Achievement("streak_365", "Year of Code", "Maintain a 365-day commit streak", AchievementTier.DIAMOND, "🌍"))

# ── Time-based Achievements ──
_register(Achievement("night_owl", "Night Owl", "Make a commit between midnight and 4 AM", AchievementTier.BRONZE, "🦉"))
_register(Achievement("early_bird", "Early Bird", "Make a commit between 5 AM and 7 AM", AchievementTier.BRONZE, "🐦"))
_register(Achievement("weekend_warrior", "Weekend Warrior", "Make a commit on a Saturday or Sunday", AchievementTier.BRONZE, "⚔️"))
_register(Achievement("midnight_coder", "Midnight Coder", "Make a commit at exactly midnight", AchievementTier.SILVER, "🌙"))
_register(Achievement("holiday_hacker", "Holiday Hacker", "Commit on a major holiday (Dec 25, Jan 1)", AchievementTier.GOLD, "🎄"))

# ── Pet Care Achievements ──
_register(Achievement("first_feed", "Caretaker", "Manually feed your pet for the first time", AchievementTier.BRONZE, "🍕"))
_register(Achievement("first_play", "Playful", "Play with your pet for the first time", AchievementTier.BRONZE, "🎮"))
_register(Achievement("full_stats", "Perfect Balance", "Get all pet stats to 100%", AchievementTier.SILVER, "⚖️"))
_register(Achievement("close_call", "Close Call", "Feed your pet when hunger is below 10%", AchievementTier.SILVER, "😰"))
_register(Achievement("resurrection", "Phoenix", "Resurrect your dead pet", AchievementTier.GOLD, "🔥"))
_register(Achievement("three_resurrections", "Necromancer", "Resurrect your pet 3 times", AchievementTier.PLATINUM, "💀"))

# ── Evolution Achievements ──
_register(Achievement("evolve_baby", "Hatched!", "Evolve your pet to Baby stage", AchievementTier.BRONZE, "🐣"))
_register(Achievement("evolve_teen", "Growing Up", "Evolve your pet to Teen stage", AchievementTier.SILVER, "🐥"))
_register(Achievement("evolve_adult", "All Grown Up", "Evolve your pet to Adult stage", AchievementTier.GOLD, "🐤"))
_register(Achievement("evolve_elder", "Elder Wisdom", "Evolve your pet to Elder stage", AchievementTier.DIAMOND, "👑"))

# ── Hidden Achievements ──
_register(Achievement("speed_demon", "Speed Demon", "Make 10 commits within a single hour", AchievementTier.GOLD, "⚡", hidden=True))
_register(Achievement("pet_whisperer", "Pet Whisperer", "Keep your pet happy for 30 consecutive days", AchievementTier.PLATINUM, "🐾", hidden=True))
_register(Achievement("five_deaths", "Grim Reaper", "Let your pet die 5 times", AchievementTier.SILVER, "☠️", hidden=True))
_register(Achievement("reset_master", "Fresh Start", "Reset your pet and start over", AchievementTier.BRONZE, "🔄", hidden=True))


def get_achievement(achievement_id: str) -> Optional[Achievement]:
    """Get an achievement by ID."""
    return ACHIEVEMENTS.get(achievement_id)


def get_all_achievements() -> List[Achievement]:
    """Get all registered achievements."""
    return list(ACHIEVEMENTS.values())


def get_achievements_by_tier(tier: AchievementTier) -> List[Achievement]:
    """Get all achievements of a specific tier."""
    return [a for a in ACHIEVEMENTS.values() if a.tier == tier]


def get_visible_achievements() -> List[Achievement]:
    """Get all non-hidden achievements."""
    return [a for a in ACHIEVEMENTS.values() if not a.hidden]


def get_hidden_achievements() -> List[Achievement]:
    """Get all hidden achievements."""
    return [a for a in ACHIEVEMENTS.values() if a.hidden]


class AchievementTracker:
    """Tracks and checks achievement conditions against pet state."""

    STATE_FILE = Path.home() / ".terminal-pet" / "achievements.json"

    def __init__(self):
        self.earned: Dict[str, EarnedAchievement] = {}
        self._commit_timestamps: List[float] = []
        self._load()

    def _load(self):
        """Load earned achievements from disk."""
        if self.STATE_FILE.exists():
            try:
                with open(self.STATE_FILE) as f:
                    data = json.load(f)
                self.earned = {
                    k: EarnedAchievement.from_dict(v)
                    for k, v in data.get("earned", {}).items()
                }
                self._commit_timestamps = data.get("commit_timestamps", [])
            except (json.JSONDecodeError, KeyError):
                self.earned = {}
                self._commit_timestamps = []

    def save(self):
        """Save earned achievements to disk."""
        self.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "earned": {k: v.to_dict() for k, v in self.earned.items()},
            "commit_timestamps": self._commit_timestamps[-1000:],  # Keep last 1000
        }
        with open(self.STATE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def is_earned(self, achievement_id: str) -> bool:
        """Check if an achievement has been earned."""
        return achievement_id in self.earned

    def earn(self, achievement_id: str) -> Optional[Achievement]:
        """Mark an achievement as earned. Returns the Achievement if newly earned."""
        if self.is_earned(achievement_id):
            return None
        achievement = get_achievement(achievement_id)
        if achievement is None:
            return None
        self.earned[achievement_id] = EarnedAchievement(achievement_id=achievement_id)
        self.save()
        return achievement

    def record_commit_timestamp(self, timestamp: Optional[float] = None):
        """Record a commit timestamp for speed-based achievements."""
        ts = timestamp or time.time()
        self._commit_timestamps.append(ts)
        self.save()

    def get_earned_achievements(self) -> List[Achievement]:
        """Get all earned achievements as Achievement objects."""
        result = []
        for aid in self.earned:
            achievement = get_achievement(aid)
            if achievement:
                result.append(achievement)
        return result

    def get_earned_count(self) -> int:
        """Get the number of earned achievements."""
        return len(self.earned)

    def get_total_count(self) -> int:
        """Get the total number of achievements."""
        return len(ACHIEVEMENTS)

    def get_progress_percentage(self) -> float:
        """Get percentage of achievements earned."""
        total = self.get_total_count()
        if total == 0:
            return 0.0
        return (self.get_earned_count() / total) * 100

    def get_earned_timestamp(self, achievement_id: str) -> Optional[float]:
        """Get the timestamp when an achievement was earned."""
        earned = self.earned.get(achievement_id)
        return earned.earned_at if earned else None
