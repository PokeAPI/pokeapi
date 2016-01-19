package pl.marchuck.pokeapi;

/**
 * @author Lukasz Marczak
 * @since 2015-08-25.
 */
class SpriteGET {
    private SpriteGET() {
    }

    /**
     *
     * @param pokemonName name of pokemon
     * @return
     */
    public static String pokemonBigImage(String pokemonName) {
        return "http://img.pokemondb.net/artwork/" + lowerCaseName(pokemonName) + ".jpg";
    }

    private static String lowerCaseName(String pokemonName) {
        if (pokemonName == null || pokemonName.length() < 3)
            pokemonName = "pikachu";
        return pokemonName.toLowerCase();
    }

    private static String camelCaseName(String pokemonName) {
        if (pokemonName == null || pokemonName.length() < 3)
            pokemonName = "Pikachu";
        String firstLetter = String.valueOf(pokemonName.charAt(0)).toUpperCase();
        String lowercase = pokemonName.toLowerCase();
        return firstLetter + lowercase.substring(1);
    }


    /**
     * @param pokomonName one of 493 pokemons available
     * @return string url for image
     */
    public static String pokemonBack(String pokomonName) {
        return "http://img.pokemondb.net/sprites/heartgold-soulsilver/back-normal/" + lowerCaseName(pokomonName) + ".png";
    }

    /**
     * @param pokomonName one of 493 pokemons available
     * @return string url for image
     */
    public static String pokemonFront(String pokomonName) {
        return "http://img.pokemondb.net/sprites/heartgold-soulsilver/normal/" + lowerCaseName(pokomonName) + ".png";
    }

    /**
     * @param pokemonId   1
     * @param pokemonName Bulbasaur
     * @return url to icon image
     */
    public static String pokemonIcon(int pokemonId, String pokemonName) {
        String fixedId = getFixedId(pokemonId);
        String fixedName = camelCaseName(pokemonName);
//        Log.d(TAG, "id = " + fixedId + "," + fixedName);
        if (pokemonId == 29) {
            return "http://icons.iconarchive.com/icons/hektakun/pokemon/72/" + fixedId + "-Nidoran-icon.png";
        } else if (pokemonId == 30) {
            return "http://icons.iconarchive.com/icons/hektakun/pokemon/72/" + fixedId + "-Nidorina-icon.png";
        } else if (pokemonId == 31) {
            return "http://icons.iconarchive.com/icons/hektakun/pokemon/72/" + fixedId + "-Nidoqueen-icon.png";
        } else if (pokemonId == 32) {
            return "http://icons.iconarchive.com/icons/hektakun/pokemon/72/" + fixedId + "-Nidorano-icon.png";
        } else if (pokemonId == 33) {
            return "http://icons.iconarchive.com/icons/hektakun/pokemon/72/" + fixedId + "-Nidorino-icon.png";
        } else if (pokemonId == 34) {
            return "http://icons.iconarchive.com/icons/hektakun/pokemon/72/" + fixedId + "-Nidoking-icon.png";
        } else if (pokemonId == 122) {
            return "http://icons.iconarchive.com/icons/hektakun/pokemon/72/122-Mr-Mime-icon.png";
        }
        return "http://icons.iconarchive.com/icons/hektakun/pokemon/72/" + fixedId + "-" + fixedName + "-icon.png";
    }

    private static String getFixedId(int id) {
        if (id < 10) {
            return "00" + id;
        } else if (id < 100) {
            return "0" + id;
        } else return String.valueOf(id);
    }
}
