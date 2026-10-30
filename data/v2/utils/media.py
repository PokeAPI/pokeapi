import contextlib
import gzip
import json
import os
import urllib.error
import urllib.request
from collections.abc import Callable
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any

MEDIA_DIR = "{prefix}{{file_name}}".format(
    prefix=os.environ.get(
        "POKEAPI_SPRITES_PREFIX",
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/",
    )
)
SOUND_DIR = "{prefix}{{file_name}}".format(
    prefix=os.environ.get(
        "POKEAPI_CRIES_PREFIX",
        "https://raw.githubusercontent.com/PokeAPI/cries/main/cries/",
    )
)
DATA_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = DATA_DIR / "sprites" / "sprites"
CRIES_DIR = DATA_DIR / "cries" / "cries"


def _load_manifest_from_path(path: Path) -> set[str] | None:
    try:
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return set(json.load(f))
    except (OSError, json.JSONDecodeError) as e:
        print(f"Warning: Failed to read local sprite manifest at {path}: {e}")
        return None


def _fetch_manifest(url: str, cache_file: Path) -> set[str] | None:
    try:
        if cache_file.is_file():
            try:
                head_req = urllib.request.Request(url, method="HEAD")
                with urllib.request.urlopen(head_req, timeout=10) as head_resp:
                    last_mod_header = head_resp.headers.get("Last-Modified")
                    if last_mod_header:
                        remote_mtime = parsedate_to_datetime(last_mod_header).timestamp()
                        if cache_file.stat().st_mtime >= remote_mtime:
                            return _load_manifest_from_path(cache_file)
            except (OSError, urllib.error.URLError, ValueError):
                pass

        with urllib.request.urlopen(url, timeout=30) as resp:
            raw_bytes: bytes = resp.read()
            data = json.loads(gzip.decompress(raw_bytes).decode("utf-8"))

            with contextlib.suppress(OSError):
                cache_file.write_bytes(raw_bytes)
                last_mod = resp.headers.get("Last-Modified")
                if last_mod:
                    mtime = parsedate_to_datetime(last_mod).timestamp()
                    os.utime(cache_file, (mtime, mtime))

            return set(data)
    except (OSError, urllib.error.URLError, json.JSONDecodeError, gzip.BadGzipFile) as e:
        print(f"Warning: Failed to fetch sprite manifest from {url}: {e}")
        return None


def _load_local_sprites() -> set[str]:
    """Scan the local cloned sprites submodule directory."""
    if not IMAGE_DIR.is_dir():
        return set()

    images: set[str] = set()
    for image_path in IMAGE_DIR.rglob("*"):
        if not image_path.is_dir():
            images.add(image_path.relative_to(IMAGE_DIR).as_posix())
    return images


def _load_resource_images() -> set[str]:
    use_local = os.environ.get("POKEAPI_USE_LOCAL_SPRITES", "").lower() in ("1", "true", "yes")
    if use_local and (local_images := _load_local_sprites()):
        return local_images

    cache_file = DATA_DIR / "manifest.json.gz"
    manifest_urls: list[str] = list(
        filter(
            None,
            [
                os.environ.get("POKEAPI_SPRITES_MANIFEST_URL", ""),
                "https://pokeapi.github.io/sprites/manifest.json.gz",
                "https://github.com/PokeAPI/sprites/releases/latest/download/manifest.json.gz",
            ],
        )
    )

    for url in manifest_urls:
        if (data := _fetch_manifest(url, cache_file)) is not None:
            return data

    # If offline / all remote requests failed, use cached manifest if available
    if cache_file.is_file() and (cached := _load_manifest_from_path(cache_file)) is not None:
        return cached

    # Fallback to local files if manifest is completely unavailable
    if local_images := _load_local_sprites():
        return local_images

    print("Warning: Could not load sprite resources from local files or remote manifest. Sprites will be empty.")
    return set()


RESOURCE_IMAGES: set[str] = _load_resource_images()
RESOURCE_CRIES: set[str] = set()

for cry_path in CRIES_DIR.rglob("*"):
    if not cry_path.is_dir():
        cry_key = cry_path.relative_to(CRIES_DIR).as_posix()
        RESOURCE_CRIES.add(cry_key)


TYPE_SPRITE_GAME_MAP: dict[str, list[str]] = {
    "generation-iii": [
        "colosseum",
        "emerald",
        "firered-leafgreen",
        "ruby-sapphire",
        "xd",
    ],
    "generation-iv": ["diamond-pearl", "heartgold-soulsilver", "platinum"],
    "generation-v": ["black-2-white-2", "black-white"],
    "generation-vi": ["omega-ruby-alpha-sapphire", "x-y"],
    "generation-vii": [
        "lets-go-pikachu-lets-go-eevee",
        "sun-moon",
        "ultra-sun-ultra-moon",
    ],
    "generation-viii": [
        "brilliant-diamond-shining-pearl",
        "legends-arceus",
        "sword-shield",
    ],
    "generation-ix": ["scarlet-violet", "champions"],
}


POKEMON_SPRITE_CONFIG: dict[str, Any] = {
    "front_default": ("pokemon/", "png"),
    "front_female": ("pokemon/female/", "png"),
    "front_shiny": ("pokemon/shiny/", "png"),
    "front_shiny_female": ("pokemon/shiny/female/", "png"),
    "back_default": ("pokemon/back/", "png"),
    "back_female": ("pokemon/back/female/", "png"),
    "back_shiny": ("pokemon/back/shiny/", "png"),
    "back_shiny_female": ("pokemon/back/shiny/female/", "png"),
    "other": {
        "dream_world": {
            "front_default": ("pokemon/other/dream-world/", "svg"),
            "front_female": ("pokemon/other/dream-world/female/", "svg"),
        },
        "home": {
            "front_default": ("pokemon/other/home/", "png"),
            "front_female": ("pokemon/other/home/female/", "png"),
            "front_shiny": ("pokemon/other/home/shiny/", "png"),
            "front_shiny_female": ("pokemon/other/home/shiny/female/", "png"),
        },
        "official-artwork": {
            "front_default": ("pokemon/other/official-artwork/", "png"),
            "front_shiny": ("pokemon/other/official-artwork/shiny/", "png"),
            "versions": {
                "generation-i": {
                    "red-and-blue": {
                        "front_default": ("pokemon/other/official-artwork/versions/generation-i/red-and-blue/", "png")
                    },
                    "red-and-green": {
                        "front_default": ("pokemon/other/official-artwork/versions/generation-i/red-and-green/", "png")
                    },
                },
                "generation-ii": {
                    "gold-and-silver": {
                        "front_default": (
                            "pokemon/other/official-artwork/versions/generation-ii/gold-and-silver/",
                            "png",
                        )
                    }
                },
            },
        },
        "showdown": {
            "front_default": ("pokemon/other/showdown/", "gif"),
            "front_female": ("pokemon/other/showdown/female/", "gif"),
            "front_shiny": ("pokemon/other/showdown/shiny/", "gif"),
            "front_shiny_female": ("pokemon/other/showdown/shiny/female/", "gif"),
            "back_default": ("pokemon/other/showdown/back/", "gif"),
            "back_female": ("pokemon/other/showdown/back/female/", "gif"),
            "back_shiny": ("pokemon/other/showdown/back/shiny/", "gif"),
            "back_shiny_female": ("pokemon/other/showdown/back/shiny/female/", "gif"),
        },
    },
    "versions": {
        "generation-i": {
            "red-blue": {
                "front_default": ("pokemon/versions/generation-i/red-blue/", "png"),
                "front_gray": ("pokemon/versions/generation-i/red-blue/gray/", "png"),
                "front_transparent": ("pokemon/versions/generation-i/red-blue/transparent/", "png"),
                "front_transparent_gray": ("pokemon/versions/generation-i/red-blue/transparent/gray/", "png"),
                "back_default": ("pokemon/versions/generation-i/red-blue/back/", "png"),
                "back_gray": ("pokemon/versions/generation-i/red-blue/back/gray/", "png"),
                "back_transparent": ("pokemon/versions/generation-i/red-blue/transparent/back/", "png"),
                "back_transparent_gray": ("pokemon/versions/generation-i/red-blue/transparent/back/gray/", "png"),
            },
            "red-green-japan": {
                "front_default": ("pokemon/versions/generation-i/red-green-japan/", "png"),
                "front_gray": ("pokemon/versions/generation-i/red-green-japan/gray/", "png"),
                "back_default": ("pokemon/versions/generation-i/red-green-japan/back/", "png"),
                "back_gray": ("pokemon/versions/generation-i/red-green-japan/back/gray/", "png"),
            },
            "yellow": {
                "front_default": ("pokemon/versions/generation-i/yellow/", "png"),
                "front_gbc": ("pokemon/versions/generation-i/yellow/gbc/", "png"),
                "front_gray": ("pokemon/versions/generation-i/yellow/gray/", "png"),
                "front_transparent": ("pokemon/versions/generation-i/yellow/transparent/", "png"),
                "front_transparent_gray": ("pokemon/versions/generation-i/yellow/transparent/gray/", "png"),
                "back_default": ("pokemon/versions/generation-i/yellow/back/", "png"),
                "back_gbc": ("pokemon/versions/generation-i/yellow/back/gbc/", "png"),
                "back_gray": ("pokemon/versions/generation-i/yellow/back/gray/", "png"),
                "back_transparent": ("pokemon/versions/generation-i/yellow/transparent/back/", "png"),
                "back_transparent_gray": ("pokemon/versions/generation-i/yellow/transparent/back/gray/", "png"),
            },
        },
        "generation-ii": {
            "crystal": {
                "front_default": ("pokemon/versions/generation-ii/crystal/", "png"),
                "front_shiny": ("pokemon/versions/generation-ii/crystal/shiny/", "png"),
                "front_transparent": ("pokemon/versions/generation-ii/crystal/transparent/", "png"),
                "front_shiny_transparent": ("pokemon/versions/generation-ii/crystal/transparent/shiny/", "png"),
                "back_default": ("pokemon/versions/generation-ii/crystal/back/", "png"),
                "back_shiny": ("pokemon/versions/generation-ii/crystal/back/shiny/", "png"),
                "back_transparent": ("pokemon/versions/generation-ii/crystal/transparent/back/", "png"),
                "back_shiny_transparent": ("pokemon/versions/generation-ii/crystal/transparent/back/shiny/", "png"),
                "animated": {
                    "front_default": ("pokemon/versions/generation-ii/crystal/animated/", "gif"),
                    "front_shiny": ("pokemon/versions/generation-ii/crystal/animated/shiny/", "gif"),
                },
            },
            "gold": {
                "front_default": ("pokemon/versions/generation-ii/gold/", "png"),
                "front_shiny": ("pokemon/versions/generation-ii/gold/shiny/", "png"),
                "front_transparent": ("pokemon/versions/generation-ii/gold/transparent/", "png"),
                "front_shiny_transparent": ("pokemon/versions/generation-ii/gold/transparent/shiny/", "png"),
                "back_default": ("pokemon/versions/generation-ii/gold/back/", "png"),
                "back_shiny": ("pokemon/versions/generation-ii/gold/back/shiny/", "png"),
                "back_transparent": ("pokemon/versions/generation-ii/gold/transparent/back/", "png"),
                "back_shiny_transparent": ("pokemon/versions/generation-ii/gold/transparent/back/shiny/", "png"),
            },
            "silver": {
                "front_default": ("pokemon/versions/generation-ii/silver/", "png"),
                "front_shiny": ("pokemon/versions/generation-ii/silver/shiny/", "png"),
                "front_transparent": ("pokemon/versions/generation-ii/silver/transparent/", "png"),
                "front_shiny_transparent": ("pokemon/versions/generation-ii/silver/transparent/shiny/", "png"),
                "back_default": ("pokemon/versions/generation-ii/silver/back/", "png"),
                "back_shiny": ("pokemon/versions/generation-ii/silver/back/shiny/", "png"),
                "back_transparent": ("pokemon/versions/generation-ii/silver/transparent/back/", "png"),
                "back_shiny_transparent": ("pokemon/versions/generation-ii/silver/transparent/back/shiny/", "png"),
            },
        },
        "generation-iii": {
            "emerald": {
                "front_default": ("pokemon/versions/generation-iii/emerald/", "png"),
                "front_shiny": ("pokemon/versions/generation-iii/emerald/shiny/", "png"),
                "back_default": ("pokemon/versions/generation-iii/emerald/back/", "png"),
                "back_shiny": ("pokemon/versions/generation-iii/emerald/back/shiny/", "png"),
                "animated": {
                    "front_default": ("pokemon/versions/generation-iii/emerald/animated/", "png"),
                    "front_shiny": ("pokemon/versions/generation-iii/emerald/animated/shiny/", "png"),
                    "back_default": ("pokemon/versions/generation-iii/emerald/animated/back/", "png"),
                    "back_shiny": ("pokemon/versions/generation-iii/emerald/animated/back/shiny/", "png"),
                },
            },
            "firered-leafgreen": {
                "front_default": ("pokemon/versions/generation-iii/firered-leafgreen/", "png"),
                "front_shiny": ("pokemon/versions/generation-iii/firered-leafgreen/shiny/", "png"),
                "back_default": ("pokemon/versions/generation-iii/firered-leafgreen/back/", "png"),
                "back_shiny": ("pokemon/versions/generation-iii/firered-leafgreen/back/shiny/", "png"),
            },
            "icons": {
                "front_default": ("pokemon/versions/generation-iii/icons/", "png"),
            },
            "ruby-sapphire": {
                "front_default": ("pokemon/versions/generation-iii/ruby-sapphire/", "png"),
                "front_shiny": ("pokemon/versions/generation-iii/ruby-sapphire/shiny/", "png"),
                "back_default": ("pokemon/versions/generation-iii/ruby-sapphire/back/", "png"),
                "back_shiny": ("pokemon/versions/generation-iii/ruby-sapphire/back/shiny/", "png"),
            },
        },
        "generation-iv": {
            "diamond-pearl": {
                "front_default": ("pokemon/versions/generation-iv/diamond-pearl/", "png"),
                "front_female": ("pokemon/versions/generation-iv/diamond-pearl/female/", "png"),
                "front_shiny": ("pokemon/versions/generation-iv/diamond-pearl/shiny/", "png"),
                "front_shiny_female": ("pokemon/versions/generation-iv/diamond-pearl/shiny/female/", "png"),
                "back_default": ("pokemon/versions/generation-iv/diamond-pearl/back/", "png"),
                "back_female": ("pokemon/versions/generation-iv/diamond-pearl/back/female/", "png"),
                "back_shiny": ("pokemon/versions/generation-iv/diamond-pearl/back/shiny/", "png"),
                "back_shiny_female": ("pokemon/versions/generation-iv/diamond-pearl/back/shiny/female/", "png"),
                "animated": {
                    "front_default": ("pokemon/versions/generation-iv/diamond-pearl/animated/", "png"),
                    "front_female": ("pokemon/versions/generation-iv/diamond-pearl/animated/female/", "png"),
                    "front_shiny": ("pokemon/versions/generation-iv/diamond-pearl/animated/shiny/", "png"),
                    "front_shiny_female": (
                        "pokemon/versions/generation-iv/diamond-pearl/animated/shiny/female/",
                        "png",
                    ),
                },
            },
            "heartgold-soulsilver": {
                "front_default": ("pokemon/versions/generation-iv/heartgold-soulsilver/", "png"),
                "front_female": ("pokemon/versions/generation-iv/heartgold-soulsilver/female/", "png"),
                "front_shiny": ("pokemon/versions/generation-iv/heartgold-soulsilver/shiny/", "png"),
                "front_shiny_female": ("pokemon/versions/generation-iv/heartgold-soulsilver/shiny/female/", "png"),
                "back_default": ("pokemon/versions/generation-iv/heartgold-soulsilver/back/", "png"),
                "back_female": ("pokemon/versions/generation-iv/heartgold-soulsilver/back/female/", "png"),
                "back_shiny": ("pokemon/versions/generation-iv/heartgold-soulsilver/back/shiny/", "png"),
                "back_shiny_female": ("pokemon/versions/generation-iv/heartgold-soulsilver/back/shiny/female/", "png"),
                "animated": {
                    "front_default": ("pokemon/versions/generation-iv/heartgold-soulsilver/animated/", "png"),
                    "front_female": ("pokemon/versions/generation-iv/heartgold-soulsilver/animated/female/", "png"),
                    "front_shiny": ("pokemon/versions/generation-iv/heartgold-soulsilver/animated/shiny/", "png"),
                    "front_shiny_female": (
                        "pokemon/versions/generation-iv/heartgold-soulsilver/animated/shiny/female/",
                        "png",
                    ),
                },
            },
            "icons": {
                "front_default": ("pokemon/versions/generation-iv/icons/", "png"),
            },
            "platinum": {
                "front_default": ("pokemon/versions/generation-iv/platinum/", "png"),
                "front_female": ("pokemon/versions/generation-iv/platinum/female/", "png"),
                "front_shiny": ("pokemon/versions/generation-iv/platinum/shiny/", "png"),
                "front_shiny_female": ("pokemon/versions/generation-iv/platinum/shiny/female/", "png"),
                "back_default": ("pokemon/versions/generation-iv/platinum/back/", "png"),
                "back_female": ("pokemon/versions/generation-iv/platinum/back/female/", "png"),
                "back_shiny": ("pokemon/versions/generation-iv/platinum/back/shiny/", "png"),
                "back_shiny_female": ("pokemon/versions/generation-iv/platinum/back/shiny/female/", "png"),
                "animated": {
                    "front_default": ("pokemon/versions/generation-iv/platinum/animated/", "png"),
                    "front_female": ("pokemon/versions/generation-iv/platinum/animated/female/", "png"),
                    "front_shiny": ("pokemon/versions/generation-iv/platinum/animated/shiny/", "png"),
                    "front_shiny_female": ("pokemon/versions/generation-iv/platinum/animated/shiny/female/", "png"),
                },
            },
        },
        "generation-v": {
            "black-white": {
                "front_default": ("pokemon/versions/generation-v/black-white/", "png"),
                "front_female": ("pokemon/versions/generation-v/black-white/female/", "png"),
                "front_shiny": ("pokemon/versions/generation-v/black-white/shiny/", "png"),
                "front_shiny_female": ("pokemon/versions/generation-v/black-white/shiny/female/", "png"),
                "back_default": ("pokemon/versions/generation-v/black-white/back/", "png"),
                "back_female": ("pokemon/versions/generation-v/black-white/back/female/", "png"),
                "back_shiny": ("pokemon/versions/generation-v/black-white/back/shiny/", "png"),
                "back_shiny_female": ("pokemon/versions/generation-v/black-white/back/shiny/female/", "png"),
                "animated": {
                    "front_default": ("pokemon/versions/generation-v/black-white/animated/", "gif"),
                    "front_female": ("pokemon/versions/generation-v/black-white/animated/female/", "gif"),
                    "front_shiny": ("pokemon/versions/generation-v/black-white/animated/shiny/", "gif"),
                    "front_shiny_female": ("pokemon/versions/generation-v/black-white/animated/shiny/female/", "gif"),
                    "back_default": ("pokemon/versions/generation-v/black-white/animated/back/", "gif"),
                    "back_female": ("pokemon/versions/generation-v/black-white/animated/back/female/", "gif"),
                    "back_shiny": ("pokemon/versions/generation-v/black-white/animated/back/shiny/", "gif"),
                    "back_shiny_female": (
                        "pokemon/versions/generation-v/black-white/animated/back/shiny/female/",
                        "gif",
                    ),
                },
            },
            "icons": {
                "front_default": ("pokemon/versions/generation-v/icons/", "png"),
                "animated": {
                    "front_default": ("pokemon/versions/generation-v/icons/animated/", "png"),
                },
            },
        },
        "generation-vi": {
            "icons": {
                "front_default": ("pokemon/versions/generation-vi/icons/", "png"),
                "front_female": ("pokemon/versions/generation-vi/icons/female/", "png"),
            },
            "omega-ruby-alpha-sapphire": {
                "front_default": ("pokemon/versions/generation-vi/omega-ruby-alpha-sapphire/", "png"),
                "front_female": ("pokemon/versions/generation-vi/omega-ruby-alpha-sapphire/female/", "png"),
                "front_shiny": ("pokemon/versions/generation-vi/omega-ruby-alpha-sapphire/shiny/", "png"),
                "front_shiny_female": ("pokemon/versions/generation-vi/omega-ruby-alpha-sapphire/shiny/female/", "png"),
                "back_default": ("pokemon/versions/generation-vi/omega-ruby-alpha-sapphire/back/", "png"),
                "back_female": ("pokemon/versions/generation-vi/omega-ruby-alpha-sapphire/back/female/", "png"),
                "back_shiny": ("pokemon/versions/generation-vi/omega-ruby-alpha-sapphire/back/shiny/", "png"),
                "back_shiny_female": (
                    "pokemon/versions/generation-vi/omega-ruby-alpha-sapphire/back/shiny/female/",
                    "png",
                ),
            },
            "x-y": {
                "front_default": ("pokemon/versions/generation-vi/x-y/", "png"),
                "front_female": ("pokemon/versions/generation-vi/x-y/female/", "png"),
                "front_shiny": ("pokemon/versions/generation-vi/x-y/shiny/", "png"),
                "front_shiny_female": ("pokemon/versions/generation-vi/x-y/shiny/female/", "png"),
                "back_default": ("pokemon/versions/generation-vi/x-y/back/", "png"),
                "back_female": ("pokemon/versions/generation-vi/x-y/back/female/", "png"),
                "back_shiny": ("pokemon/versions/generation-vi/x-y/back/shiny/", "png"),
                "back_shiny_female": ("pokemon/versions/generation-vi/x-y/back/shiny/female/", "png"),
            },
        },
        "generation-vii": {
            "icons": {
                "front_default": ("pokemon/versions/generation-vii/icons/", "png"),
                "front_female": ("pokemon/versions/generation-vii/icons/female/", "png"),
            },
            "lets-go-pikachu-lets-go-eevee": {
                "front_default": ("pokemon/versions/generation-vii/lets-go-pikachu-lets-go-eevee/", "gif"),
                "front_female": ("pokemon/versions/generation-vii/lets-go-pikachu-lets-go-eevee/female/", "gif"),
                "front_shiny": ("pokemon/versions/generation-vii/lets-go-pikachu-lets-go-eevee/shiny/", "gif"),
                "front_shiny_female": (
                    "pokemon/versions/generation-vii/lets-go-pikachu-lets-go-eevee/shiny/female/",
                    "gif",
                ),
                "back_default": ("pokemon/versions/generation-vii/lets-go-pikachu-lets-go-eevee/back/", "gif"),
                "back_female": ("pokemon/versions/generation-vii/lets-go-pikachu-lets-go-eevee/back/female/", "gif"),
                "back_shiny": ("pokemon/versions/generation-vii/lets-go-pikachu-lets-go-eevee/back/shiny/", "gif"),
                "back_shiny_female": (
                    "pokemon/versions/generation-vii/lets-go-pikachu-lets-go-eevee/back/shiny/female/",
                    "gif",
                ),
                "icons": {
                    "front_default": ("pokemon/versions/generation-vii/lets-go-pikachu-lets-go-eevee/icons/", "png")
                },
            },
            "ultra-sun-ultra-moon": {
                "front_default": ("pokemon/versions/generation-vii/ultra-sun-ultra-moon/", "gif"),
                "front_female": ("pokemon/versions/generation-vii/ultra-sun-ultra-moon/female/", "gif"),
                "front_shiny": ("pokemon/versions/generation-vii/ultra-sun-ultra-moon/shiny/", "gif"),
                "front_shiny_female": ("pokemon/versions/generation-vii/ultra-sun-ultra-moon/shiny/female/", "gif"),
                "back_default": ("pokemon/versions/generation-vii/ultra-sun-ultra-moon/back/", "gif"),
                "back_female": ("pokemon/versions/generation-vii/ultra-sun-ultra-moon/back/female/", "gif"),
                "back_shiny": ("pokemon/versions/generation-vii/ultra-sun-ultra-moon/back/shiny/", "gif"),
                "back_shiny_female": ("pokemon/versions/generation-vii/ultra-sun-ultra-moon/back/shiny/female/", "gif"),
            },
        },
        "generation-viii": {
            "brilliant-diamond-shining-pearl": {
                "front_default": ("pokemon/versions/generation-viii/brilliant-diamond-shining-pearl/", "webp"),
                "front_female": ("pokemon/versions/generation-viii/brilliant-diamond-shining-pearl/female/", "webp"),
                "front_shiny": ("pokemon/versions/generation-viii/brilliant-diamond-shining-pearl/shiny/", "webp"),
                "front_shiny_female": (
                    "pokemon/versions/generation-viii/brilliant-diamond-shining-pearl/shiny/female/",
                    "webp",
                ),
                "back_default": ("pokemon/versions/generation-viii/brilliant-diamond-shining-pearl/back/", "webp"),
                "back_female": (
                    "pokemon/versions/generation-viii/brilliant-diamond-shining-pearl/back/female/",
                    "webp",
                ),
                "back_shiny": ("pokemon/versions/generation-viii/brilliant-diamond-shining-pearl/back/shiny/", "webp"),
                "back_shiny_female": (
                    "pokemon/versions/generation-viii/brilliant-diamond-shining-pearl/back/shiny/female/",
                    "webp",
                ),
                "icons": {
                    "front_default": ("pokemon/versions/generation-viii/brilliant-diamond-shining-pearl/icons/", "png"),
                },
            },
            "legends-arceus": {
                "front_default": ("pokemon/versions/generation-viii/legends-arceus/", "webp"),
                "front_female": ("pokemon/versions/generation-viii/legends-arceus/female/", "webp"),
                "front_shiny": ("pokemon/versions/generation-viii/legends-arceus/shiny/", "webp"),
                "front_shiny_female": ("pokemon/versions/generation-viii/legends-arceus/shiny/female/", "webp"),
                "back_default": ("pokemon/versions/generation-viii/legends-arceus/back/", "webp"),
                "back_female": ("pokemon/versions/generation-viii/legends-arceus/back/female/", "webp"),
                "back_shiny": ("pokemon/versions/generation-viii/legends-arceus/back/shiny/", "webp"),
                "back_shiny_female": ("pokemon/versions/generation-viii/legends-arceus/back/shiny/female/", "webp"),
                "icons": {
                    "front_default": ("pokemon/versions/generation-viii/legends-arceus/icons/", "png"),
                    "front_female": ("pokemon/versions/generation-viii/legends-arceus/icons/female/", "png"),
                    "front_shiny": ("pokemon/versions/generation-viii/legends-arceus/icons/shiny/", "png"),
                    "front_shiny_female": (
                        "pokemon/versions/generation-viii/legends-arceus/icons/shiny/female/",
                        "png",
                    ),
                },
            },
            "sword-shield": {
                "front_default": ("pokemon/versions/generation-viii/sword-shield/", "webp"),
                "front_female": ("pokemon/versions/generation-viii/sword-shield/female/", "webp"),
                "front_shiny": ("pokemon/versions/generation-viii/sword-shield/shiny/", "webp"),
                "front_shiny_female": ("pokemon/versions/generation-viii/sword-shield/shiny/female/", "webp"),
                "back_default": ("pokemon/versions/generation-viii/sword-shield/back/", "webp"),
                "back_female": ("pokemon/versions/generation-viii/sword-shield/back/female/", "webp"),
                "back_shiny": ("pokemon/versions/generation-viii/sword-shield/back/shiny/", "webp"),
                "back_shiny_female": ("pokemon/versions/generation-viii/sword-shield/back/shiny/female/", "webp"),
                "icons": {
                    "front_default": ("pokemon/versions/generation-viii/sword-shield/icons/", "png"),
                    "front_female": ("pokemon/versions/generation-viii/sword-shield/icons/female/", "png"),
                },
            },
        },
        "generation-ix": {
            "champions": {
                "front_default": ("pokemon/versions/generation-ix/champions/", "webp"),
                "front_female": ("pokemon/versions/generation-ix/champions/female/", "webp"),
                "front_shiny": ("pokemon/versions/generation-ix/champions/shiny/", "webp"),
                "front_shiny_female": ("pokemon/versions/generation-ix/champions/shiny/female/", "webp"),
                "back_default": ("pokemon/versions/generation-ix/champions/back/", "webp"),
                "back_female": ("pokemon/versions/generation-ix/champions/back/female/", "webp"),
                "back_shiny": ("pokemon/versions/generation-ix/champions/back/shiny/", "webp"),
                "back_shiny_female": ("pokemon/versions/generation-ix/champions/back/shiny/female/", "webp"),
                "icons": {
                    "front_default": ("pokemon/versions/generation-ix/champions/icons/", "png"),
                    "front_shiny": ("pokemon/versions/generation-ix/champions/icons/shiny/", "png"),
                },
            },
            "legends-za": {
                "front_default": ("pokemon/versions/generation-ix/legends-za/", "webp"),
                "front_female": ("pokemon/versions/generation-ix/legends-za/female/", "webp"),
                "front_shiny": ("pokemon/versions/generation-ix/legends-za/shiny/", "webp"),
                "front_shiny_female": ("pokemon/versions/generation-ix/legends-za/shiny/female/", "webp"),
                "back_default": ("pokemon/versions/generation-ix/legends-za/back/", "webp"),
                "back_female": ("pokemon/versions/generation-ix/legends-za/back/female/", "webp"),
                "back_shiny": ("pokemon/versions/generation-ix/legends-za/back/shiny/", "webp"),
                "back_shiny_female": ("pokemon/versions/generation-ix/legends-za/back/shiny/female/", "webp"),
                "icons": {
                    "front_default": ("pokemon/versions/generation-ix/legends-za/icons/", "png"),
                    "front_female": ("pokemon/versions/generation-ix/legends-za/icons/female/", "png"),
                    "front_shiny": ("pokemon/versions/generation-ix/legends-za/icons/shiny/", "png"),
                    "front_shiny_female": ("pokemon/versions/generation-ix/legends-za/icons/shiny/female/", "png"),
                },
            },
            "scarlet-violet": {
                "front_default": ("pokemon/versions/generation-ix/scarlet-violet/", "webp"),
                "front_female": ("pokemon/versions/generation-ix/scarlet-violet/female/", "webp"),
                "front_shiny": ("pokemon/versions/generation-ix/scarlet-violet/shiny/", "webp"),
                "front_shiny_female": ("pokemon/versions/generation-ix/scarlet-violet/shiny/female/", "webp"),
                "back_default": ("pokemon/versions/generation-ix/scarlet-violet/back/", "webp"),
                "back_female": ("pokemon/versions/generation-ix/scarlet-violet/back/female/", "webp"),
                "back_shiny": ("pokemon/versions/generation-ix/scarlet-violet/back/shiny/", "webp"),
                "back_shiny_female": ("pokemon/versions/generation-ix/scarlet-violet/back/shiny/female/", "webp"),
                "icons": {
                    "front_default": ("pokemon/versions/generation-ix/scarlet-violet/icons/", "png"),
                    "front_female": ("pokemon/versions/generation-ix/scarlet-violet/icons/female/", "png"),
                },
            },
        },
    },
}


def file_path_or_none(file_name: str, image_file: bool = True) -> str | None:
    if not image_file:
        return SOUND_DIR.format(file_name=file_name) if file_name in RESOURCE_CRIES else None
    return MEDIA_DIR.format(file_name=file_name) if file_name in RESOURCE_IMAGES else None


def resolve_sprite_config(config: dict[str, Any], lookup: Callable[[str, str], str | None]) -> dict[str, Any]:
    resolved: dict[str, Any] = {}
    for name, value in config.items():
        if isinstance(value, dict):
            resolved[name] = resolve_sprite_config(value, lookup)  # pyright: ignore[reportUnknownArgumentType]
        else:
            path, extension = value
            resolved[name] = lookup(path, extension)
    return resolved


def pokemon_sprite_lookup(info: list[str]) -> Callable[[str, str], str | None]:
    pokemon_id, identifier, species_id = info[:3]
    file_names = [pokemon_id]
    if "-" in identifier:
        file_names.append(f"{species_id}-{identifier.split('-', 1)[1]}")

    def lookup(path: str, extension: str) -> str | None:
        for file_name in file_names:
            sprite = file_path_or_none(f"{path}{file_name}.{extension}")
            if sprite:
                return sprite
        return None

    return lookup


def pokemon_form_sprite_lookup(info: list[str]) -> Callable[[str, str], str | None]:
    form_identifier = info[2]
    pokemon_id = int(info[3])
    is_default = info[5] == "1"

    file_names: list[str] = []
    if form_identifier:
        file_names.append(f"{pokemon_id}-{form_identifier}")
    if is_default or not form_identifier:
        file_names.append(str(pokemon_id))

    def lookup(path: str, extension: str) -> str | None:
        for file_name in file_names:
            sprite = file_path_or_none(f"{path}{file_name}.{extension}")
            if sprite:
                return sprite
        return None

    return lookup
