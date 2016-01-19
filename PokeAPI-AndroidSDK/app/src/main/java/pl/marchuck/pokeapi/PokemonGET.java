package pl.marchuck.pokeapi;

import java.util.ArrayList;
import java.util.List;

import pl.marchuck.pokeapi.interfaces.PokeReceiver;
import pl.marchuck.pokeapi.interfaces.PokesReceiver;
import pl.marchuck.pokeapi.model.Pokemon;
import rx.Observable;
import rx.android.schedulers.AndroidSchedulers;
import rx.functions.Action0;
import rx.functions.Action1;
import rx.functions.Func1;
import rx.functions.Func2;
import rx.schedulers.Schedulers;

/**
 * Created by Łukasz Marczak
 *
 * @since 19.01.16
 */
public class PokemonGET {
    private rx.Subscription pokeSubscription;

    public void unSubscribe() {
        if (pokeSubscription != null && !pokeSubscription.isUnsubscribed())
            pokeSubscription.unsubscribe();
    }

    private Integer singleId;
    private List<Integer> integerList = new ArrayList<>();
    private Action1<Throwable> onError = new Action1<Throwable>() {
        @Override
        public void call(Throwable throwable) {

        }
    };
    private Action0 onStart = new Action0() {
        @Override
        public void call() {

        }
    };
    private Action0 onEnd = new Action0() {
        @Override
        public void call() {

        }
    };

    public PokemonGET onDownloadStart(Action0 actionStart) {
        this.onStart = actionStart;
        return this;
    }

    public PokemonGET onDownloadEnd(Action0 actionEnd) {
        this.onStart = actionEnd;
        return this;
    }

    public PokemonGET onError(Action1<Throwable> actionError) {
        this.onError = actionError;
        return this;
    }

    public void manyPokes(List<Integer> pokemonIds, final PokesReceiver receiver) {
        manyPokes(pokemonIds, receiver, PokeSort.ASCENDING);
    }

    public void manyPokes(List<Integer> pokemonIds, final  PokesReceiver receiver,
                                  final PokeSort sort) {
        GenericAdapter<Pokemon> a =
                new GenericAdapter<>(PokeClient.POKEAPI_ENDPOINT, Pokemon.class);

        final PokeClient service = a.adapter.create(PokeClient.class);

        pokeSubscription = Observable.from(pokemonIds).flatMap(new Func1<Integer,
                Observable<Pokemon>>() {
            @Override
            public Observable<Pokemon> call(Integer id) {
                return service.getPokemonById(id);
            }
        }).doOnSubscribe(onStart).doOnCompleted(onEnd)
                .subscribeOn(Schedulers.trampoline())
                .observeOn(AndroidSchedulers.mainThread())
                .toSortedList(new Func2<Pokemon, Pokemon, Integer>() {
                    @Override
                    public Integer call(Pokemon p1,
                                        Pokemon p2) {
                        switch (sort) {
                            case ASCENDING:
                                return p1.pkdx_id < p2.pkdx_id ? -1 : 1;
                            default:
                                return p1.pkdx_id > p2.pkdx_id ? -1 : 1;
                        }
                    }
                })
                .subscribe(new Action1<List<Pokemon>>() {
                    @Override
                    public void call(List<Pokemon> pokemons) {
                        receiver.onReceived(pokemons);
                    }
                }, onError);
    }

    /**
     *
     * @param pokemonId for example 1
     * @param receiver how you can use fetched pokemon
     */
    public void singlePoke(Integer pokemonId, final PokeReceiver receiver) {

        GenericAdapter<Pokemon> a =
                new GenericAdapter<>(PokeClient.POKEAPI_ENDPOINT, Pokemon.class);
        pokeSubscription = a.adapter.create(PokeClient.class).getPokemonById(pokemonId)
                .doOnSubscribe(onStart).doOnCompleted(onEnd)
                .subscribeOn(Schedulers.trampoline())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(new Action1<Pokemon>() {
                    @Override
                    public void call(Pokemon pokemonDescription) {
                        receiver.onReceived(pokemonDescription);
                    }
                }, onError);
    }

}
