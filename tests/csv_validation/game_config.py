"""
Game-specific configuration for encounter data validation.

Each game configuration defines validation rules that encounters must satisfy.
These configs are used by the CSV validation tests to ensure data quality
before merging PRs.

To add a new game:
1. Define the valid Pokemon set (national dex numbers available in that game)
2. Define valid encounter methods for that game
3. Define version information and exclusives
4. Add to GAME_CONFIGS registry
"""

from dataclasses import dataclass, field


@dataclass
class GameConfig:
    """Configuration for validating a specific game's encounter data."""

    version_group_id: int
    name: str
    version_ids: list[int]
    valid_pokemon: set[int]
    valid_method_ids: set[int]
    version_exclusives: dict[int, int] = field(
        default_factory=dict
    )  # pokemon_id -> version_id


# =============================================================================
# LGPE Configuration
# =============================================================================

# PokeAPI IDs
LGPE_VERSION_PIKACHU = 31
LGPE_VERSION_EEVEE = 32
LGPE_VERSION_GROUP = 19

# Pokemon available in LGPE (Kanto dex + Meltan/Melmetal)
LGPE_POKEMON = set(range(1, 152)) | {808, 809}

# Encounter method IDs
LGPE_METHOD_OVERWORLD = 38
LGPE_METHOD_OVERWORLD_WATER = 39
LGPE_METHOD_OVERWORLD_FLYING = 40
LGPE_METHOD_RARE_SPAWN = 41

LGPE_METHOD_IDS = {
    LGPE_METHOD_OVERWORLD,
    LGPE_METHOD_OVERWORLD_WATER,
    LGPE_METHOD_OVERWORLD_FLYING,
    LGPE_METHOD_RARE_SPAWN,
}

LGPE_VERSION_EXCLUSIVES = {
    # Pikachu exclusives
    # Sandshrew, Sandslash
    27: LGPE_VERSION_PIKACHU,
    28: LGPE_VERSION_PIKACHU,
    # Oddish, Gloom, Vileplume
    43: LGPE_VERSION_PIKACHU,
    44: LGPE_VERSION_PIKACHU,
    45: LGPE_VERSION_PIKACHU,
    # Mankey, Primeape
    56: LGPE_VERSION_PIKACHU,
    57: LGPE_VERSION_PIKACHU,
    # Growlithe, Arcanine
    58: LGPE_VERSION_PIKACHU,
    59: LGPE_VERSION_PIKACHU,
    # Grimer, Muk
    88: LGPE_VERSION_PIKACHU,
    89: LGPE_VERSION_PIKACHU,
    # Scyther
    123: LGPE_VERSION_PIKACHU,

    # Eevee exclusives
    # Ekans, Arbok
    23: LGPE_VERSION_EEVEE,
    24: LGPE_VERSION_EEVEE,
    # Vulpix, Ninetales
    37: LGPE_VERSION_EEVEE,
    38: LGPE_VERSION_EEVEE,
    # Meowth, Persian
    52: LGPE_VERSION_EEVEE,
    53: LGPE_VERSION_EEVEE,
    # Bellsprout, Weepinbell, Victreebel
    69: LGPE_VERSION_EEVEE,
    70: LGPE_VERSION_EEVEE,
    71: LGPE_VERSION_EEVEE,
    # Koffing, Weezing
    109: LGPE_VERSION_EEVEE,
    110: LGPE_VERSION_EEVEE,
    # Pinsir
    127: LGPE_VERSION_EEVEE,
}

LGPE_CONFIG = GameConfig(
    version_group_id=LGPE_VERSION_GROUP,
    name="Let's Go Pikachu/Eevee",
    version_ids=[LGPE_VERSION_PIKACHU, LGPE_VERSION_EEVEE],
    valid_pokemon=LGPE_POKEMON,
    valid_method_ids=LGPE_METHOD_IDS,
    version_exclusives=LGPE_VERSION_EXCLUSIVES,
)


# =============================================================================
# Game Registry
# =============================================================================

GAME_CONFIGS: dict[int, GameConfig] = {
    LGPE_VERSION_GROUP: LGPE_CONFIG,
}
