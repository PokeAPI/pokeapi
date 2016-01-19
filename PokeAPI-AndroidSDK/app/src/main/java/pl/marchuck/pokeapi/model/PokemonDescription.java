package pl.marchuck.pokeapi.model;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Łukasz Marczak
 *
 * @since 30.12.15
 */
public class PokemonDescription {
    public String created;
    public String description;
    public List<PokeDetail> games = new ArrayList<PokeDetail>();
    public Integer id;
    public String modified;
    public String name;
    public PokeDetail pokemon;
    public String resource_uri;
}
