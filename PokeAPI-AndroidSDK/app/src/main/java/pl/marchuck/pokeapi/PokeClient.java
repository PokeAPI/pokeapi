package pl.marchuck.pokeapi;

import pl.marchuck.pokeapi.model.Pokemon;
import pl.marchuck.pokeapi.model.PokemonDescription;
import retrofit.http.GET;
import retrofit.http.Path;

/**
 * Created by Łukasz Marczak
 *
 * @since 25.12.15
 */
interface PokeClient {
    String POKEAPI_ENDPOINT = "http://pokeapi.co";

    @GET("/api/v1/pokemon/{id}/")
    rx.Observable<Pokemon> getPokemonById(@Path("id") Integer id);

    @GET("/api/v1/description/{id}/")
    rx.Observable<PokemonDescription> getPokemonDescription(@Path("id") Integer id);


}
