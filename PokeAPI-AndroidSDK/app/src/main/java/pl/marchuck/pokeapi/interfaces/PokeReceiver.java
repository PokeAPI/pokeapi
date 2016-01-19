package pl.marchuck.pokeapi.interfaces;

import pl.marchuck.pokeapi.model.Pokemon;

/**
 * Created by Łukasz Marczak
 *
 * @since 19.01.16
 */
public interface PokeReceiver {
    void onReceived(Pokemon pokemon);
}
