from promise import Promise
from promise.dataloader import DataLoader
from pokemon_v2 import models as m
from .utils import batch_fetch


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


def unbatch(keys, values, id_attr):
    return [[v for v in values if key == getattr(v, id_attr)] for key in keys]


def match_values_to_keys(keys, values, id_attr):
    """Match each value to its associated key."""

    results = []
    for key in keys:
        value = None
        for obj in values:
            if str(getattr(obj, id_attr)) == str(key):
                value = obj
                break
        results.append(value)
    return results


class Loaders:
    """Create a new set of data loaders."""

    def __init__(self):

        # Single resources by the resource's primary key
        self.generation = SingleLoader(m.Generation, "pk")
        self.language = SingleLoader(m.Language, "pk")
        self.location = SingleLoader(m.Location, "pk")
        self.locationarea = SingleLoader(m.LocationArea, "pk")
        self.pokedex = SingleLoader(m.Pokedex, "pk")
        self.pokemon = SingleLoader(m.Pokemon, "pk")
        self.region = SingleLoader(m.Region, "pk")
        self.version = SingleLoader(m.Version, "pk")
        self.versiongroup = SingleLoader(m.VersionGroup, "pk")

        # Single resources by the resource's name attribute
        self.n_generation = SingleLoader(m.Generation, "name")
        self.n_language = SingleLoader(m.Language, "name")
        self.n_location = SingleLoader(m.Location, "name")
        self.n_locationarea = SingleLoader(m.LocationArea, "name")
        self.n_pokedex = SingleLoader(m.Pokedex, "name")
        self.n_pokemon = SingleLoader(m.Pokemon, "name")
        self.n_region = SingleLoader(m.Region, "name")
        self.n_version = SingleLoader(m.Version, "name")
        self.n_versiongroup = SingleLoader(m.VersionGroup, "name")

        # Other single resources
        self.region_generations = SingleLoader(m.Generation, "region_id")
        self.pokemon_sprites = SingleLoader(m.PokemonSprites, "pokemon_id")

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
        self.pokemon_stats = ListLoader(m.PokemonStat, "pokemon_id")
        self.pokemon_types = ListLoader(m.PokemonType, "pokemon_id")
        self.region_names = TranslationsLoader(m.RegionName, "region_id")
        self.region_pokedexes = ListLoader(m.Pokedex, "region_id")
        self.region_versiongroups = RegionVersionGroupsLoader()
        self.version_names = TranslationsLoader(m.VersionName, "version_id")
        self.versiongroup_versions = ListLoader(m.Version, "version_group_id")


# Abstract Loaders


class SingleLoader(DataLoader):
    def __init__(self, model, id_attr):
        super().__init__()
        self.model = model
        self.id_attr = id_attr

    def batch_load_fn(self, keys):
        q = self.model.objects.filter(**{self.id_attr + "__in": keys})
        results = match_values_to_keys(keys, q, self.id_attr)
        return Promise.resolve(results)


class ListLoader(DataLoader):
    def __init__(self, model, id_attr):
        super().__init__()
        self.model = model
        self.id_attr = id_attr

    def batch_load_fn(self, keys):
        data = self.model.objects.filter(**{self.id_attr + "__in": keys})
        results = unbatch(keys, data, self.id_attr)
        return Promise.resolve(results)


class TranslationsLoader(DataLoader):
    def __init__(self, model, id_attr, language_attr="language"):
        super().__init__()
        self.model = model
        self.id_attr = id_attr
        self.language_attr = language_attr

    def batch_load_fn(self, keys):
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

    def get_query_set(self, ids, lang=None):
        q = self.model.objects.filter(**{self.id_attr + "__in": ids})
        q = q.select_related(self.language_attr)
        if lang:
            q = q.filter(**{self.language_attr + "__name__in": lang})
        return q


# Loaders for lists of resources


class RegionVersionGroupsLoader(DataLoader):
    def batch_load_fn(self, keys):
        data = m.VersionGroupRegion.objects.filter(region_id__in=keys)
        data = data.select_related("version_group")

        data = unbatch(keys, data, "region_id")
        results = [[result.version_group for result in d] for d in data]

        return Promise.resolve(results)
