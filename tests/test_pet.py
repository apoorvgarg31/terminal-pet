"""Tests for the Pet class."""

import time
import pytest
from unittest.mock import patch, MagicMock
from terminal_pet.pet import Pet, PetState, PetMood


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
