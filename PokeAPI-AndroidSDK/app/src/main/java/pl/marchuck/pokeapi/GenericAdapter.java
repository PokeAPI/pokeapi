package pl.marchuck.pokeapi;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonParseException;

import retrofit.RestAdapter;
import retrofit.converter.GsonConverter;

/**
 * @author Lukasz Marczak
 * @since 2015-10-05
 * Generic deserializer for lists of objects, or simple POJO objects
 */
class GenericAdapter<T> {
    public RestAdapter adapter;

    /**
     * Special generic adapter, whose json representation is equal to POJO model representation
     */
    public GenericAdapter(String endpoint, final Class<T> templateClass) {
        GsonBuilder builder = new GsonBuilder();
        builder.registerTypeAdapter(templateClass, new Deserializer<T>() {
            @Override
            public Class<T> setDestinationClass() {
                return templateClass;
            }
        });
        Gson gson = builder.create();
        GsonConverter converter = new GsonConverter(gson);
        adapter = new RestAdapter.Builder()
                .setEndpoint(endpoint)
                .setConverter(converter)
                .build();
    }
    private static abstract class Deserializer<T> implements JsonDeserializer<T> {
        public abstract Class<T> setDestinationClass();
        @Override
        public T deserialize(JsonElement json, java.lang.reflect.Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
            return new Gson().fromJson(json, setDestinationClass());
        }
    }
}
