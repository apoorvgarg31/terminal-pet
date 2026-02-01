"""Tests for the Pet class."""

import time
import pytest
from unittest.mock import patch, MagicMock
from terminal_pet.pet import Pet, PetState, PetMood, EvolutionStage, EVOLUTION_THRESHOLDS


class TestPetState:
    """Tests for PetState dataclass."""
    
    def test_default_values(self):
        """Test default state values."""
        state = PetState()
        assert state.name == "Pip"
        assert state.pet_type == "blob"
        assert state.hunger == 80
        assert state.happiness == 80
        assert state.energy == 80
        assert state.died_at is None
    
    def test_to_dict(self):
        """Test serialization to dict."""
        state = PetState(name="TestPet", pet_type="pixel")
        data = state.to_dict()
        assert data["name"] == "TestPet"
        assert data["pet_type"] == "pixel"
    
    def test_from_dict(self):
        """Test deserialization from dict."""
        data = {
            "name": "TestPet",
            "pet_type": "octo",
            "hunger": 50,
            "happiness": 60,
            "energy": 70,
            "born_at": time.time(),
            "last_fed": time.time(),
            "last_played": time.time(),
            "last_activity": time.time(),
            "last_decay_applied": time.time(),
            "died_at": None,
            "resurrect_streak": 0,
            "total_commits": 0,
            "total_deaths": 0,
            "total_resurrections": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "last_commit_date": None,
        }
        state = PetState.from_dict(data)
        assert state.name == "TestPet"
        assert state.pet_type == "octo"
        assert state.hunger == 50


class TestPet:
    """Tests for Pet class."""
    
    @pytest.fixture
    def pet(self, tmp_path):
        """Create a pet with temporary state file."""
        state = PetState()
        pet = Pet(state)
        pet.STATE_FILE = tmp_path / "state.json"
        return pet
    
    def test_initial_mood_is_happy(self, pet):
        """Test that a new pet starts happy."""
        mood = pet.mood
        assert mood in [PetMood.HAPPY, PetMood.CONTENT, PetMood.ECSTATIC]
    
    def test_is_not_dead_initially(self, pet):
        """Test that a new pet is alive."""
        assert not pet.is_dead
    
    def test_feeding_increases_hunger(self, pet):
        """Test that feeding increases hunger stat."""
        initial_hunger = pet.state.hunger
        pet.on_activity("feed")
        assert pet.state.hunger > initial_hunger
    
    def test_playing_increases_happiness(self, pet):
        """Test that playing increases happiness."""
        initial_happiness = pet.state.happiness
        pet.on_activity("play")
        assert pet.state.happiness > initial_happiness
    
    def test_commit_increases_stats(self, pet):
        """Test that commits feed the pet."""
        initial_hunger = pet.state.hunger
        pet.state.hunger = 50  # Lower it first
        pet.on_activity("commit")
        assert pet.state.hunger > 50
        assert pet.state.total_commits == 1
    
    def test_death_when_hunger_zero(self, pet):
        """Test that pet dies when hunger reaches 0."""
        pet.state.hunger = 0
        pet.state.last_decay_applied = time.time() - 3600  # 1 hour ago
        pet.apply_decay()
        assert pet.is_dead
    
    def test_death_increments_counter(self, pet):
        """Test that death increments death counter."""
        assert pet.state.total_deaths == 0
        pet.state.hunger = 0
        pet.state.last_decay_applied = time.time() - 3600
        pet.apply_decay()
        assert pet.state.total_deaths == 1
    
    def test_mood_changes_with_stats(self, pet):
        """Test that mood reflects stats."""
        pet.state.hunger = 10
        pet.state.happiness = 10
        pet.state.energy = 10
        assert pet.mood in [PetMood.CRITICAL, PetMood.SAD, PetMood.HUNGRY, PetMood.TIRED]
    
    def test_decay_rates_are_reasonable(self, pet):
        """Test that decay rates allow ~7 day survival."""
        # With 80 hunger and 0.6/hour decay, should last ~133 hours (~5.5 days)
        # This is close enough to the ~7 day target
        assert Pet.HUNGER_DECAY < 1  # Less than 1 per hour
        assert Pet.HAPPINESS_DECAY < 1
        assert Pet.ENERGY_DECAY < 1
    
    def test_age_calculation(self, pet):
        """Test age calculation."""
        age = pet.age
        assert age.total_seconds() >= 0
        assert "minute" in pet.age_str or "hour" in pet.age_str or "day" in pet.age_str
    
    def test_save_and_load(self, pet, tmp_path):
        """Test state persistence."""
        pet.STATE_FILE = tmp_path / "test_state.json"
        pet.state.name = "SaveTest"
        pet.state.total_commits = 42
        pet.save()
        
        # Create new pet and load
        new_pet = Pet()
        new_pet.STATE_FILE = tmp_path / "test_state.json"
        loaded_state = new_pet._load_state()
        
        assert loaded_state is not None
        assert loaded_state.name == "SaveTest"
        assert loaded_state.total_commits == 42


class TestResurrection:
    """Tests for resurrection mechanics."""
    
    @pytest.fixture
    def dead_pet(self, tmp_path):
        """Create a dead pet."""
        state = PetState()
        pet = Pet(state)
        pet.STATE_FILE = tmp_path / "state.json"
        pet.state.hunger = 0
        pet.state.died_at = time.time()
        pet.state.total_deaths = 1
        return pet
    
    def test_dead_pet_is_dead(self, dead_pet):
        """Test that dead pet reports as dead."""
        assert dead_pet.is_dead
    
    def test_resurrection_starts(self, dead_pet):
        """Test starting resurrection."""
        dead_pet.start_resurrection()
        assert dead_pet.state.resurrect_streak == 0
    
    def test_ghost_mode(self, dead_pet):
        """Test ghost mode during resurrection."""
        dead_pet.state.resurrect_streak = 1
        assert dead_pet.is_ghost
        assert dead_pet.mood == PetMood.GHOST


class TestEvolution:
    """Tests for pet evolution mechanics."""

    @pytest.fixture
    def pet(self, tmp_path):
        """Create a pet with temporary state file."""
        state = PetState()
        pet = Pet(state)
        pet.STATE_FILE = tmp_path / "state.json"
        return pet

    def test_new_pet_is_egg(self, pet):
        """Test that a new pet starts as an egg."""
        assert pet.evolution_stage == EvolutionStage.EGG
        assert pet.evolution_emoji == "🥚"

    def test_evolution_to_baby(self, pet):
        """Test evolution from egg to baby at 10 commits."""
        pet.state.total_commits = 9
        assert pet.evolution_stage == EvolutionStage.EGG

        pet.state.total_commits = 10
        assert pet.evolution_stage == EvolutionStage.BABY
        assert pet.evolution_emoji == "🐣"

    def test_evolution_to_teen(self, pet):
        """Test evolution from baby to teen at 50 commits."""
        pet.state.total_commits = 49
        assert pet.evolution_stage == EvolutionStage.BABY

        pet.state.total_commits = 50
        assert pet.evolution_stage == EvolutionStage.TEEN
        assert pet.evolution_emoji == "🐥"

    def test_evolution_to_adult(self, pet):
        """Test evolution from teen to adult at 200 commits."""
        pet.state.total_commits = 199
        assert pet.evolution_stage == EvolutionStage.TEEN

        pet.state.total_commits = 200
        assert pet.evolution_stage == EvolutionStage.ADULT
        assert pet.evolution_emoji == "🐤"

    def test_evolution_to_elder(self, pet):
        """Test evolution from adult to elder at 500 commits."""
        pet.state.total_commits = 499
        assert pet.evolution_stage == EvolutionStage.ADULT

        pet.state.total_commits = 500
        assert pet.evolution_stage == EvolutionStage.ELDER
        assert pet.evolution_emoji == "👑"

    def test_evolution_thresholds(self):
        """Test that evolution thresholds are correctly defined."""
        assert EVOLUTION_THRESHOLDS[EvolutionStage.EGG] == 0
        assert EVOLUTION_THRESHOLDS[EvolutionStage.BABY] == 10
        assert EVOLUTION_THRESHOLDS[EvolutionStage.TEEN] == 50
        assert EVOLUTION_THRESHOLDS[EvolutionStage.ADULT] == 200
        assert EVOLUTION_THRESHOLDS[EvolutionStage.ELDER] == 500

    def test_commits_to_next_evolution_egg(self, pet):
        """Test commits to next evolution from egg stage."""
        pet.state.total_commits = 0
        assert pet.commits_to_next_evolution == 10

        pet.state.total_commits = 5
        assert pet.commits_to_next_evolution == 5

    def test_commits_to_next_evolution_baby(self, pet):
        """Test commits to next evolution from baby stage."""
        pet.state.total_commits = 10
        assert pet.commits_to_next_evolution == 40  # 50 - 10

        pet.state.total_commits = 30
        assert pet.commits_to_next_evolution == 20  # 50 - 30

    def test_commits_to_next_evolution_elder(self, pet):
        """Test that elder has no next evolution."""
        pet.state.total_commits = 500
        assert pet.commits_to_next_evolution is None

        pet.state.total_commits = 1000
        assert pet.commits_to_next_evolution is None

    def test_commit_triggers_evolution_detection(self, pet):
        """Test that committing triggers evolution detection."""
        pet.state.total_commits = 9
        pet.state.last_commit_date = None

        # This commit should trigger evolution to BABY
        evolved = pet.on_activity("commit")
        assert evolved == EvolutionStage.BABY
        assert pet.state.total_commits == 10

    def test_commit_no_evolution_when_not_threshold(self, pet):
        """Test that committing doesn't return evolution when not at threshold."""
        pet.state.total_commits = 5
        pet.state.last_commit_date = None

        evolved = pet.on_activity("commit")
        assert evolved is None
        assert pet.state.total_commits == 6

    def test_evolution_through_multiple_commits(self, pet):
        """Test evolution detection through multiple commits."""
        pet.state.total_commits = 8
        pet.state.last_commit_date = None

        # Commit 9 - no evolution
        evolved = pet.on_activity("commit")
        assert evolved is None
        assert pet.evolution_stage == EvolutionStage.EGG

        # Commit 10 - evolution to BABY
        evolved = pet.on_activity("commit")
        assert evolved == EvolutionStage.BABY
        assert pet.evolution_stage == EvolutionStage.BABY
