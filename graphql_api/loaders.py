from promise import Promise
from promise.dataloader import DataLoader

from pokemon_v2 import models as m
from .loader_util import unbatch, batch_fetch, add_filters


########################################################################################
# Data loaders batch and cache requests to the database. Each request gets a new instance
# of Loaders, so this is per-request only (see middleware for the specifics). Each data
# loader returns a list of Django model objects. Any manipulation occurs elsewhere in the
# program (in field resolvers).
#
# To use a data loader, instantiate a Loaders object (or get it from the context), then
# call the `load()` method on a specific loader, passing in a key. Data loaders take one
# of two kinds of keys: simple integer IDs, or instances of LoaderKey. Loaders that return
# simple objects take integer IDs, while loaders that return lists of objects take
# LoaderKey instances, allowing for complex filtering. The loader will return a Promise.
#
# For more information about DataLoader, see https://github.com/syrusakbary/aiodataloader.
########################################################################################


class Loaders:
    """Create a new set of data loaders."""

    def __init__(self):

        # Single resources by the resource's primary key
        self.generation = SingleLoader(m.Generation)
        self.language = SingleLoader(m.Language)
        self.location = SingleLoader(m.Location)
        self.locationarea = SingleLoader(m.LocationArea)
        self.pokedex = SingleLoader(m.Pokedex)
        self.pokemon = SingleLoader(m.Pokemon)
        self.region = SingleLoader(m.Region)
        self.version = SingleLoader(m.Version)
        self.versiongroup = SingleLoader(m.VersionGroup)

        # Single resources by the resource's name attribute
        self.n_generation = SingleLoaderByName(m.Generation)
        self.n_language = SingleLoaderByName(m.Language)
        self.n_location = SingleLoaderByName(m.Location)
        self.n_locationarea = SingleLoaderByName(m.LocationArea)
        self.n_pokedex = SingleLoaderByName(m.Pokedex)
        self.n_pokemon = SingleLoaderByName(m.Pokemon)
        self.n_region = SingleLoaderByName(m.Region)
        self.n_version = SingleLoaderByName(m.Version)
        self.n_versiongroup = SingleLoaderByName(m.VersionGroup)

        # Other single resources
        self.generation_by_region = GenerationByRegionLoader()

        # Lists of Sub-Resources (Names, Descriptions, etc.) for a Resource
        self.generation_names = TranslationsLoader(m.GenerationName, "generation_id")
        self.generation_types = ListLoader(m.Type, "generation_id")
        self.generation_versiongroups = ListLoader(m.VersionGroup, "generation_id")
        self.language_names = TranslationsLoader(
            m.LanguageName, "language_id", "local_language"
        )
        self.location_gameindices = ListLoader(m.LocationGameIndex, "location_id")
        self.location_locationareas = ListLoader(m.LocationArea, "location_id")
        self.locationarea_encounterrates = ListLoader(
            m.LocationAreaEncounterRate, "location_area_id"
        )
        self.location_names = TranslationsLoader(m.LocationName, "location_id")
        self.locationarea_names = TranslationsLoader(
            m.LocationAreaName, "location_area_id"
        )
        self.pokedex_descriptions = TranslationsLoader(
            m.PokedexDescription, "pokedex_id"
        )
        self.pokedex_names = TranslationsLoader(m.PokedexName, "pokedex_id")
        self.pokemon_abilities = ListLoader(m.PokemonAbility, "pokemon_id")
        self.pokemon_forms = ListLoader(m.PokemonForm, "pokemon_id")
        self.pokemon_gameindices = ListLoader(m.PokemonGameIndex, "pokemon_id")
        self.pokemon_sprites = PokemonSpritesLoader()
        self.pokemon_stats = ListLoader(m.PokemonStat, "pokemon_id")
        self.pokemon_types = ListLoader(m.PokemonType, "pokemon_id")
        self.region_names = TranslationsLoader(m.RegionName, "region_id")
        self.region_versiongroups = RegionVersionGroupsLoader()
        self.version_names = TranslationsLoader(m.VersionName, "version_id")
        self.versiongroup_versions = ListLoader(m.Version, "version_group_id")


# Abstract Loaders


class SingleLoader(DataLoader):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def batch_load_fn(self, keys):
        q = self.model.objects.filter(pk__in=keys)
        return Promise.resolve(unbatch(keys, q, "pk"))


class SingleLoaderByName(DataLoader):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def batch_load_fn(self, keys):
        q = self.model.objects.filter(name__in=keys)
        return Promise.resolve(unbatch(keys, q, "name"))


class ListLoader(DataLoader):
    def __init__(self, model, id_attr):
        super().__init__()
        self.model = model
        self.id_attr = id_attr

    def batch_load_fn(self, keys):
        results = batch_fetch(keys, self.get_query_set, self.id_attr)
        return Promise.resolve(results)

    def get_query_set(self, ids, **args):
        return self.model.objects.filter(**{self.id_attr + "__in": ids})


class TranslationsLoader(DataLoader):
    def __init__(self, model, id_attr, language_attr="language"):
        super().__init__()
        self.model = model
        self.id_attr = id_attr
        self.language_attr = language_attr

    def batch_load_fn(self, keys):
        """Required args: lang"""

        results = batch_fetch(keys, self.get_query_set, self.id_attr)

        sorted_results = []
        for i, result in enumerate(results):
            args = keys[i].args._asdict()
            languages = args.get("lang", None)

            # Sort results based on the order in the 'lang' argument, if present
            def sort_key(translation, languages=languages):
                if languages:
                    name = getattr(translation, self.language_attr).name
                    return languages.index(name)
                return translation.pk

            sorted_results.append(sorted(result, key=sort_key))

        return Promise.resolve(sorted_results)

    def get_query_set(self, ids, **args):
        q = self.model.objects.filter(**{self.id_attr + "__in": ids})
        q = q.select_related(self.language_attr)
        q = add_filters(q, args, **{self.language_attr + "__name__in": "lang"})
        return q


# Loaders for lists of resources


class RegionVersionGroupsLoader(DataLoader):
    def batch_load_fn(self, keys):
        data = batch_fetch(keys, self.get_query_set, "region_id")
        results = [[result.version_group for result in d] for d in data]
        return Promise.resolve(results)

    def get_query_set(self, ids, **args):
        q = m.VersionGroupRegion.objects.filter(region_id__in=ids)
        q = q.select_related("version_group")
        return q


# Loaders for single resources


class GenerationByRegionLoader(DataLoader):
    def batch_load_fn(self, keys):
        q = m.Generation.objects.filter(region_id__in=keys)
        results = unbatch(keys, q, "region_id")
        return Promise.resolve(results)


class PokemonSpritesLoader(DataLoader):
    def batch_load_fn(self, keys):
        q = m.PokemonSprites.objects.filter(pokemon_id__in=keys)
        results = unbatch(keys, q, "pokemon_id")
        return Promise.resolve(results)
