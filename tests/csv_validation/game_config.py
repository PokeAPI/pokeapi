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

    game_id: str
    name: str
    version_ids: list[int]  # PokeAPI version IDs
    version_group_id: int  # PokeAPI version group ID
    valid_pokemon: set[int]
    valid_method_ids: set[int]
    version_exclusives: dict[int, int] = field(
        default_factory=dict
    )  # pokemon_id -> version_id
    level_bounds: tuple[int, int] = (1, 100)


# =============================================================================
# LGPE Configuration
# =============================================================================

LGPE_POKEMON = set(range(1, 152)) | {808, 809}

LGPE_VERSION_PIKACHU = 31
LGPE_VERSION_EEVEE = 32
LGPE_VERSION_GROUP = 19

LGPE_METHOD_IDS = {38, 39, 40, 41}

LGPE_VERSION_EXCLUSIVES = {
    # Pikachu exclusives (version_id = 31)
    27: 31,
    28: 31,  # Sandshrew, Sandslash
    43: 31,
    44: 31,
    45: 31,  # Oddish line
    56: 31,
    57: 31,  # Mankey, Primeape
    58: 31,
    59: 31,  # Growlithe, Arcanine
    88: 31,
    89: 31,  # Grimer, Muk
    123: 31,  # Scyther
    # Eevee exclusives (version_id = 32)
    23: 32,
    24: 32,  # Ekans, Arbok
    37: 32,
    38: 32,  # Vulpix, Ninetales
    52: 32,
    53: 32,  # Meowth, Persian
    69: 32,
    70: 32,
    71: 32,  # Bellsprout line
    109: 32,
    110: 32,  # Koffing, Weezing
    127: 32,  # Pinsir
}

LGPE_CONFIG = GameConfig(
    game_id="lgpe",
    name="Let's Go Pikachu/Eevee",
    version_ids=[LGPE_VERSION_PIKACHU, LGPE_VERSION_EEVEE],
    version_group_id=LGPE_VERSION_GROUP,
    valid_pokemon=LGPE_POKEMON,
    valid_method_ids=LGPE_METHOD_IDS,
    version_exclusives=LGPE_VERSION_EXCLUSIVES,
    level_bounds=(1, 100),
)


# =============================================================================
# Game Registry
# =============================================================================

GAME_CONFIGS: dict[str, GameConfig] = {
    "lgpe": LGPE_CONFIG,
}


def get_game_config(game_id: str) -> GameConfig:
    if game_id not in GAME_CONFIGS:
        available = ", ".join(GAME_CONFIGS.keys())
        raise ValueError(f"Unknown game '{game_id}'. Available: {available}")
    return GAME_CONFIGS[game_id]
