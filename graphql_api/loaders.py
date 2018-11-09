from itertools import islice
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


BATCH_SIZE = 999


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


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
        self.ability = SingleLoader(m.Ability, "pk")
        self.characteristic = SingleLoader(m.Characteristic, "pk")
        self.egggroup = SingleLoader(m.EggGroup, "pk")
        self.encounter = SingleLoader(m.Encounter, "pk")
        self.encountercondition = SingleLoader(m.EncounterCondition, "pk")
        self.encountermethod = SingleLoader(m.EncounterMethod, "pk")
        self.gender = SingleLoader(m.Gender, "pk")
        self.generation = SingleLoader(m.Generation, "pk")
        self.growthrate = SingleLoader(m.GrowthRate, "pk")
        self.language = SingleLoader(m.Language, "pk")
        self.location = SingleLoader(m.Location, "pk")
        self.locationarea = SingleLoader(m.LocationArea, "pk")
        self.nature = SingleLoader(m.Nature, "pk")
        self.pokedex = SingleLoader(m.Pokedex, "pk")
        self.pokemon = SingleLoader(m.Pokemon, "pk")
        self.pokemoncolor = SingleLoader(m.PokemonColor, "pk")
        self.pokemonform = SingleLoader(m.PokemonForm, "pk")
        self.pokemonhabitat = SingleLoader(m.PokemonHabitat, "pk")
        self.pokemonshape = SingleLoader(m.PokemonShape, "pk")
        self.pokemonspecies = SingleLoader(m.PokemonSpecies, "pk")
        self.region = SingleLoader(m.Region, "pk")
        self.stat = SingleLoader(m.Stat, "pk")
        self.type = SingleLoader(m.Type, "pk")
        self.version = SingleLoader(m.Version, "pk")
        self.versiongroup = SingleLoader(m.VersionGroup, "pk")

        # Single resources by the resource's name attribute
        self.n_ability = SingleLoader(m.Ability, "name")
        self.n_egggroup = SingleLoader(m.EggGroup, "name")
        self.n_encountercondition = SingleLoader(m.EncounterCondition, "name")
        self.n_encountermethod = SingleLoader(m.EncounterMethod, "name")
        self.n_gender = SingleLoader(m.Gender, "name")
        self.n_generation = SingleLoader(m.Generation, "name")
        self.n_growthrate = SingleLoader(m.GrowthRate, "name")
        self.n_language = SingleLoader(m.Language, "name")
        self.n_location = SingleLoader(m.Location, "name")
        self.n_locationarea = SingleLoader(m.LocationArea, "name")
        self.n_nature = SingleLoader(m.Nature, "name")
        self.n_pokedex = SingleLoader(m.Pokedex, "name")
        self.n_pokemon = SingleLoader(m.Pokemon, "name")
        self.n_pokemoncolor = SingleLoader(m.PokemonColor, "name")
        self.n_pokemonform = SingleLoader(m.PokemonForm, "name")
        self.n_pokemonhabitat = SingleLoader(m.PokemonHabitat, "name")
        self.n_pokemonshape = SingleLoader(m.PokemonShape, "name")
        self.n_pokemonspecies = SingleLoader(m.PokemonSpecies, "name")
        self.n_region = SingleLoader(m.Region, "name")
        self.n_stat = SingleLoader(m.Stat, "name")
        self.n_type = SingleLoader(m.Type, "name")
        self.n_version = SingleLoader(m.Version, "name")
        self.n_versiongroup = SingleLoader(m.VersionGroup, "name")

        # Other single resources
        self.region_generation = SingleLoader(m.Generation, "region_id")
        self.pokemonsprites = SingleLoader(m.PokemonSprites, "pokemon_id")
        self.pokemonformsprites = SingleLoader(m.PokemonFormSprites, "pokemon_form_id")

        # Lists of Sub-Resources (Names, Descriptions, etc.) for a Resource
        self.ability_effectentries = TranslationsLoader(
            m.AbilityEffectText, "ability_id"
        )
        self.ability_flavortextentries = TranslationsLoader(
            m.AbilityFlavorText, "ability_id"
        )
        self.ability_names = TranslationsLoader(m.AbilityName, "ability_id")
        self.ability_changes = ListLoader(m.AbilityChange, "ability_id")
        self.abilitychange_effectentries = TranslationsLoader(
            m.AbilityChangeEffectText, "ability_change_id"
        )
        self.characteristic_descriptions = TranslationsLoader(
            m.CharacteristicDescription, "characteristic_id"
        )
        self.damagetype_typeefficacies = ListLoader(
            m.TypeEfficacy, "damage_type_id", select_related=["target_type"]
        )
        self.decreasedstat_natures = ListLoader(m.Nature, "decreased_stat_id")
        self.egggroup_names = TranslationsLoader(m.EggGroupName, "egg_group_id")
        self.encounter_conditionvalues = ListMapLoader(
            m.EncounterConditionValueMap, "encounter_id", "encounter_condition_value"
        )
        self.encountercondition_names = TranslationsLoader(
            m.EncounterConditionName, "encounter_condition_id"
        )
        self.encountercondition_values = ListLoader(
            m.EncounterConditionValue, "encounter_condition_id"
        )
        self.encountermethod_names = TranslationsLoader(
            m.EncounterMethodName, "encounter_method_id"
        )
        self.encountercondition_names = TranslationsLoader(
            m.EncounterConditionName, "encounter_condition_id"
        )
        self.encounterconditionvalue_names = TranslationsLoader(
            m.EncounterConditionValueName, "encounter_condition_value_id"
        )
        self.generation_names = TranslationsLoader(m.GenerationName, "generation_id")
        self.generation_types = ListLoader(m.Type, "generation_id")
        self.generation_versiongroups = ListLoader(m.VersionGroup, "generation_id")
        self.growthrate_descriptions = TranslationsLoader(
            m.GrowthRateDescription, "growth_rate_id"
        )
        self.growthrate_experiences = ListLoader(m.Experience, "growth_rate_id")
        self.increasedstat_natures = ListLoader(m.Nature, "increased_stat_id")
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
        self.nature_names = TranslationsLoader(m.NatureName, "nature_id")
        self.nature_pokeathlonstats = ListLoader(m.NaturePokeathlonStat, "nature_id")
        self.nature_battlestylepreferences = ListLoader(
            m.NatureBattleStylePreference, "nature_id"
        )
        self.pokedex_descriptions = TranslationsLoader(
            m.PokedexDescription, "pokedex_id"
        )
        self.pokedex_names = TranslationsLoader(m.PokedexName, "pokedex_id")
        self.pokemon_abilities = ListLoader(m.PokemonAbility, "pokemon_id")
        self.pokemon_forms = ListLoader(m.PokemonForm, "pokemon_id")
        self.pokemon_gameindices = ListLoader(m.PokemonGameIndex, "pokemon_id")
        self.pokemon_locationareas = LocationAreasByPokemonLoader()
        self.pokemon_stats = ListLoader(m.PokemonStat, "pokemon_id")
        self.pokemon_types = ListLoader(m.PokemonType, "pokemon_id")
        self.pokemoncolor_names = TranslationsLoader(
            m.PokemonColorName, "pokemon_color_id"
        )
        self.pokemonform_names = TranslationsLoader(
            m.PokemonFormName, "pokemon_form_id"
        )
        self.pokemonhabitat_names = TranslationsLoader(
            m.PokemonHabitatName, "pokemon_habitat_id"
        )
        self.pokemonshape_names = TranslationsLoader(
            m.PokemonShapeName, "pokemon_shape_id"
        )
        self.pokemonspecies_egggroups = ListMapLoader(
            m.PokemonEggGroup, "pokemon_species_id", "egg_group"
        )
        self.pokemonspecies_flavortextentries = TranslationsLoader(
            m.PokemonSpeciesFlavorText, "pokemon_species_id"
        )
        self.pokemonspecies_descriptions = TranslationsLoader(
            m.PokemonSpeciesDescription, "pokemon_species_id"
        )
        self.pokemonspecies_names = TranslationsLoader(
            m.PokemonSpeciesName, "pokemon_species_id"
        )
        self.pokemonspecies_dexnumbers = ListLoader(
            m.PokemonDexNumber, "pokemon_species_id"
        )
        self.pokemonspecies_palparks = ListLoader(m.PalPark, "pokemon_species_id")
        # pardon the ugrammaticality of "pokemons":
        self.pokemonspecies_pokemons = ListLoader(m.Pokemon, "pokemon_species_id")
        self.region_names = TranslationsLoader(m.RegionName, "region_id")
        self.region_pokedexes = ListLoader(m.Pokedex, "region_id")
        self.region_versiongroups = ListMapLoader(
            m.VersionGroupRegion, "region_id", "version_group"
        )
        self.stat_characteristics = TranslationsLoader(m.Characteristic, "stat_id")
        self.stat_names = TranslationsLoader(m.StatName, "stat_id")
        self.targettype_typeefficacies = ListLoader(
            m.TypeEfficacy, "target_type_id", select_related=["damage_type"]
        )
        self.type_gameindices = ListLoader(m.TypeGameIndex, "type_id")
        self.type_names = TranslationsLoader(m.TypeName, "type_id")

        self.version_names = TranslationsLoader(m.VersionName, "version_id")
        self.versiongroup_versions = ListLoader(m.Version, "version_group_id")

        # Other
        self.encounters_by_locationarea_and_pokemon = (
            EncountersByLocationAreaAndPokemonLoader()
        )
        self.encounters_by_parts = EncountersByPartsLoader()


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
    def __init__(self, model, id_attr, select_related=None):
        super().__init__()
        self.model = model
        self.id_attr = id_attr
        self.select_related = select_related

    def batch_load_fn(self, keys):
        results = []
        # Limit the size of each batch
        for key_group in chunk(keys, BATCH_SIZE):
            data = self.model.objects.filter(**{self.id_attr + "__in": key_group})
            if self.select_related:
                data = data.select_related(*self.select_related)
            results = unbatch(key_group, data, self.id_attr) + results

        return Promise.resolve(results)


class ListMapLoader(DataLoader):
    def __init__(self, model, id_attr, data_attr):
        super().__init__()
        self.model = model
        self.id_attr = id_attr
        self.data_attr = data_attr

    def batch_load_fn(self, keys):
        results = []
        # Limit the size of each batch
        for key_group in chunk(keys, BATCH_SIZE):
            data = self.model.objects.filter(**{self.id_attr + "__in": key_group})
            if self.data_attr:
                data = data.select_related(self.data_attr)

            data = unbatch(key_group, data, self.id_attr)
            results = [
                [getattr(result, self.data_attr) for result in d] for d in data
            ] + results

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

            result = sorted(result, key=sort_key)
            sorted_results.append(result)

        return Promise.resolve(sorted_results)

    def get_query_set(self, ids, lang=None):
        q = self.model.objects.filter(**{self.id_attr + "__in": ids})
        q = q.select_related(self.language_attr)
        if lang:
            q = q.filter(**{self.language_attr + "__name__in": lang})
        return q


class EncountersByLocationAreaAndPokemonLoader(DataLoader):
    def batch_load_fn(self, keys):
        (location_area_ids, pokemon_ids) = zip(*keys)
        encounters = m.Encounter.objects.filter(
            location_area_id__in=location_area_ids, pokemon_id__in=pokemon_ids
        ).select_related("encounter_slot")

        results = [
            [
                e
                for e in encounters
                if e.location_area_id == key[0]
                if e.pokemon_id == key[1]
            ]
            for key in keys
        ]

        return Promise.resolve(results)


class LocationAreasByPokemonLoader(DataLoader):
    def batch_load_fn(self, keys):
        data = m.LocationArea.objects.filter(encounter__pokemon_id__in=keys)
        data = data.distinct().prefetch_related("encounter")

        results = []
        for key in keys:
            result = []
            for location_area in data:
                for encounter in location_area.encounter.all():
                    if encounter.pokemon_id == key:
                        result.append(location_area)
                        break
            results.append(result)

        return Promise.resolve(results)


class EncountersByPartsLoader(DataLoader):
    def batch_load_fn(self, keys):
        results = []
        for key_group in chunk(keys, BATCH_SIZE):
            (location_area_ids, pokemon_ids, version_ids) = zip(*key_group)
            encounters = m.Encounter.objects.filter(
                location_area_id__in=location_area_ids,
                pokemon_id__in=pokemon_ids,
                version_id__in=version_ids,
            ).select_related("encounter_slot")

            results = [
                [
                    e
                    for e in encounters
                    if e.location_area_id == key[0]
                    if e.pokemon_id == key[1]
                    if e.version_id == key[2]
                ]
                for key in key_group
            ] + results

        return Promise.resolve(results)
