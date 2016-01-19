package pl.marchuck.pokeapi.interfaces;

import java.util.List;

import pl.marchuck.pokeapi.model.Pokemon;

/**
 * Created by Łukasz Marczak
 *
 * @since 19.01.16
 */
public interface PokesReceiver {
    void onReceived(List<Pokemon> pokemons);
}
