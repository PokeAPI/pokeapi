package pl.marchuck.pokeapi.interfaces;

import pl.marchuck.pokeapi.model.PokemonDescription;

/**
 * Created by Łukasz Marczak
 *
 * @since 19.01.16
 */
public interface PokeDetailReceiver {
    void onReceived(PokemonDescription pokemonDescription);
}
