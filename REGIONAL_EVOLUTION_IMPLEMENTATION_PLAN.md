# Regional Evolution Metadata Implementation Plan

## Overview
This document outlines a **simplified implementation plan** for adding regional evolution metadata to PokeAPI, addressing [GitHub issue #639](https://github.com/PokeAPI/pokeapi/issues/639).

## Problem Statement
PokeAPI currently lacks metadata about region-specific evolution requirements. For example:
- Galarian Yamask can only evolve into Runerigus in specific Galar locations
- Galarian Slowpoke requires Galar-specific items (Galarica Cuff/Wreath)
- The API doesn't specify which base form is required for regional evolutions

## Key Insight: Leverage Existing Structure

**The existing PokeAPI structure already supports most regional evolution requirements!**

### Existing Fields That Already Work
- ✅ **`location`** - For location-specific evolutions (Galarian Yamask → Runerigus)
- ✅ **`evolution_item`** - For item-based evolutions (Galarica Cuff, Black Augurite)
- ✅ **`min_level`** - For level-based evolutions (Galarian Meowth → Perrserker)
- ✅ **`time_of_day`** - For time-based evolutions (Linoone → Obstagoon at night)
- ✅ **`needs_overworld_rain`** - For weather-based evolutions (Sliggoo → Goodra in rain)

### What's Missing: Two Key Fields

1. **Region Restriction** - The ability to specify that an evolution can only occur in a specific region
2. **Base Form Required** - The ability to specify which specific form is required for evolution

For example, the current system can't distinguish between:
- Regular Slowpoke → Regular Slowbro (with Water Stone, any region)
- Galarian Slowpoke → Galarian Slowbro (with Galarica Cuff, Galar region only)

## Proposed Solution: Two New Fields

### 1. Database Schema Changes

#### Add Two New Fields to PokemonEvolution Model
```python
class PokemonEvolution(models.Model):
    # ... all existing fields remain unchanged ...
    
    # New field for regional restrictions
    region_restriction = models.ForeignKey(
        'Region', 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE,
        help_text="Region where this evolution can occur (null = any region)"
    )
    
    # New field for base form requirements
    base_form_required = models.ForeignKey(
        'PokemonSpecies',
        blank=True,
        null=True,
        related_name="base_form_evolutions",
        on_delete=models.CASCADE,
        help_text="Specific form required for evolution (null = any form)"
    )
```

#### Migration Strategy
```python
# Migration: 0020_add_regional_evolution_fields.py
class Migration(migrations.Migration):
    dependencies = [
        ('pokemon_v2', '0019_pokemonsummary'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonevolution',
            name='region_restriction',
            field=models.ForeignKey(
                blank=True, 
                null=True, 
                on_delete=models.CASCADE, 
                to='pokemon_v2.Region'
            ),
        ),
        migrations.AddField(
            model_name='pokemonevolution',
            name='base_form_required',
            field=models.ForeignKey(
                blank=True,
                null=True,
                related_name='base_form_evolutions',
                on_delete=models.CASCADE,
                to='pokemon_v2.PokemonSpecies'
            ),
        ),
    ]
```

### 2. API Response Changes

#### Updated Evolution Details Structure
The API response would add two new fields to existing evolution details:

```json
{
  "evolution_details": [
    {
      "trigger": {
        "name": "use-item",
        "url": "https://pokeapi.co/api/v2/evolution-trigger/3/"
      },
      "item": {
        "name": "water-stone",
        "url": "https://pokeapi.co/api/v2/item/84/"
      },
      "location": null,
      "min_level": null,
      "region_restriction": null,
      "base_form_required": null
    },
    {
      "trigger": {
        "name": "use-item",
        "url": "https://pokeapi.co/api/v2/evolution-trigger/3/"
      },
      "item": {
        "name": "galarica-cuff",
        "url": "https://pokeapi.co/api/v2/item/1234/"
      },
      "location": null,
      "min_level": null,
      "region_restriction": {
        "name": "galar",
        "url": "https://pokeapi.co/api/v2/region/8/"
      },
      "base_form_required": {
        "name": "slowpoke-galar",
        "url": "https://pokeapi.co/api/v2/pokemon-species/10164/"
      }
    }
  ]
}
```

## Real-World JSON Examples

Here's how the API responses would look for actual regional evolutions:

### Example 1: Galarian Yamask → Runerigus (Location + Region)
```json
{
  "evolution_details": [
    {
      "trigger": {
        "name": "region-specific",
        "url": "https://pokeapi.co/api/v2/evolution-trigger/8/"
      },
      "item": null,
      "location": {
        "name": "dusty-bowl-arch",
        "url": "https://pokeapi.co/api/v2/location/123/"
      },
      "min_level": null,
      "region_restriction": {
        "name": "galar",
        "url": "https://pokeapi.co/api/v2/region/8/"
      },
      "base_form_required": {
        "name": "yamask-galar",
        "url": "https://pokeapi.co/api/v2/pokemon-species/10164/"
      }
    }
  ]
}
```

### Example 2: Slowpoke → Slowbro (Regular vs Galarian)
```json
{
  "evolution_details": [
    {
      "trigger": {
        "name": "use-item",
        "url": "https://pokeapi.co/api/v2/evolution-trigger/3/"
      },
      "item": {
        "name": "water-stone",
        "url": "https://pokeapi.co/api/v2/item/84/"
      },
      "location": null,
      "min_level": null,
      "region_restriction": null,
      "base_form_required": null
    },
    {
      "trigger": {
        "name": "use-item",
        "url": "https://pokeapi.co/api/v2/evolution-trigger/3/"
      },
      "item": {
        "name": "galarica-cuff",
        "url": "https://pokeapi.co/api/v2/item/1234/"
      },
      "location": null,
      "min_level": null,
      "region_restriction": {
        "name": "galar",
        "url": "https://pokeapi.co/api/v2/region/8/"
      },
      "base_form_required": {
        "name": "slowpoke-galar",
        "url": "https://pokeapi.co/api/v2/pokemon-species/10164/"
      }
    }
  ]
}
```

### Example 3: Galarian Meowth → Perrserker (Level + Region)
```json
{
  "evolution_details": [
    {
      "trigger": {
        "name": "level-up",
        "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
      },
      "item": null,
      "location": null,
      "min_level": 28,
      "region_restriction": null,
      "base_form_required": {
        "name": "meowth-galar",
        "url": "https://pokeapi.co/api/v2/pokemon-species/10164/"
      }
    }
  ]
}
```

### Example 4: Hisui Scyther → Kleavor (Item + Region)
```json
{
  "evolution_details": [
    {
      "trigger": {
        "name": "use-item",
        "url": "https://pokeapi.co/api/v2/evolution-trigger/3/"
      },
      "item": {
        "name": "black-augurite",
        "url": "https://pokeapi.co/api/v2/item/2345/"
      },
      "location": null,
      "min_level": null,
      "region_restriction": {
        "name": "hisui",
        "url": "https://pokeapi.co/api/v2/region/9/"
      },
      "base_form_required": null
    }
  ]
}
```

### Example 5: Linoone → Obstagoon (Level + Time + Region)
```json
{
  "evolution_details": [
    {
      "trigger": {
        "name": "level-up",
        "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
      },
      "item": null,
      "location": null,
      "min_level": 35,
      "time_of_day": "night",
      "region_restriction": null,
      "base_form_required": {
        "name": "linoone-galar",
        "url": "https://pokeapi.co/api/v2/pokemon-species/10164/"
      }
    }
  ]
}
```

### Example 6: Sliggoo → Goodra (Level + Weather + Region)
```json
{
  "evolution_details": [
    {
      "trigger": {
        "name": "level-up",
        "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
      },
      "item": null,
      "location": null,
      "min_level": 50,
      "needs_overworld_rain": true,
      "region_restriction": {
        "name": "hisui",
        "url": "https://pokeapi.co/api/v2/region/9/"
      },
      "base_form_required": {
        "name": "sliggoo-hisui",
        "url": "https://pokeapi.co/api/v2/pokemon-species/10164/"
      }
    }
  ]
}
```

## Key Benefits of This Approach

1. **Minimal Change**: Only adds two new fields (`region_restriction` and `base_form_required`)
2. **Leverages Existing Structure**: Uses all existing fields (location, item, level, time, weather)
3. **Backward Compatible**: All existing evolution data continues to work unchanged
4. **Clear and Simple**: Easy to understand and implement
5. **Extensible**: Can handle future regional evolutions easily
6. **Complete Solution**: Handles both region restrictions and form requirements

### 3. Data Population Strategy

#### CSV Data Structure
```csv
pokemon,evolves_to,method,region,level,item,location,requirements
yamask-galar,runerigus,region_specific,galar,,,dusty-bowl-arch
slowpoke-galar,slowbro-galar,use_item,galar,,galarica-cuff,
slowpoke,slowbro,use_item,,,water-stone,
```

## Implementation Steps

### Phase 1: Database Schema (Minimal)
1. Add `region_restriction` field to `PokemonEvolution` model
2. Create and run migration
3. Update `PokemonEvolutionSerializer` to include new field

### Phase 2: Data Population
1. Import regional evolution data using existing CSV structure
2. Map regional data to new `region_restriction` field
3. Verify data integrity

### Phase 3: Testing
1. Test API responses with regional evolution examples
2. Verify backward compatibility
3. Test edge cases

## Summary

This simplified approach adds **only one new field** (`region_restriction`) to the existing `PokemonEvolution` model, leveraging all the existing infrastructure for location, item, level, time, and weather requirements. This makes the implementation:

- **Minimal and focused**
- **Backward compatible** 
- **Easy to understand and maintain**
- **Leverages existing PokeAPI patterns**

## Backward Compatibility

- All existing evolution data remains unchanged
- New `region_restriction` and `base_form_required` fields are optional (nullable)
- Existing clients continue to work without modification
- New fields default to `null` for all existing evolution entries

## Data Coverage

Based on our collected data:
- **Galar**: 12 regional evolutions
- **Alola**: 11 regional evolutions  
- **Hisui**: 16 regional evolutions
- **Total**: 39 evolution entries with regional metadata

## Conclusion

This simplified implementation adds **only two new fields** (`region_restriction` and `base_form_required`) to the existing `PokemonEvolution` model, leveraging all the existing infrastructure. This approach:

1. **Minimizes changes** to the existing codebase
2. **Maintains backward compatibility** completely
3. **Leverages existing fields** for location, item, level, time, and weather requirements
4. **Provides clear, simple API responses** that are easy to understand
5. **Addresses the core issue** raised in GitHub issue #639
6. **Handles both region restrictions and form requirements** completely

The implementation is focused, practical, and follows existing PokeAPI patterns while providing the regional evolution metadata that users need.
