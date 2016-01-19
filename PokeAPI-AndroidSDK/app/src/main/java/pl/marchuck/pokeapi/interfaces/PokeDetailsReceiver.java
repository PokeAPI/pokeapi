package pl.marchuck.pokeapi.interfaces;

import java.util.List;

import pl.marchuck.pokeapi.model.PokemonDescription;

/**
 * Created by Łukasz Marczak
 *
 * @since 19.01.16
 */
public interface PokeDetailsReceiver {
    void onReceived(List<PokemonDescription> pokemonDescription);
}
