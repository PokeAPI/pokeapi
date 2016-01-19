package pl.marchuck.pokeapi.interfaces;

/**
 * Created by Łukasz Marczak
 *
 * @since 19.01.16
 */
public interface PokeAPIError {
    void onPokeAPIError(Throwable throwable);
}
