package pl.marchuck.pokeapi;

import java.util.ArrayList;
import java.util.List;

import pl.marchuck.pokeapi.interfaces.PokeDetailReceiver;
import pl.marchuck.pokeapi.interfaces.PokeDetailsReceiver;
import pl.marchuck.pokeapi.model.PokemonDescription;
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
public class PokeDetailGET {
    private rx.Subscription detailsSubscription;
    private Integer singleId;
    private List<Integer> integerList = new ArrayList<>();

    public void unSubscribe() {
        if (detailsSubscription != null && !detailsSubscription.isUnsubscribed())
            detailsSubscription.unsubscribe();
    }

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

    public PokeDetailGET onDownloadStart(Action0 actionStart) {
        this.onStart = actionStart;
        return this;
    }

    public PokeDetailGET onDownloadEnd(Action0 actionEnd) {
        this.onStart = actionEnd;
        return this;
    }

    public PokeDetailGET onError(Action1<Throwable> actionError) {
        this.onError = actionError;
        return this;
    }

    public void manyPokes(List<Integer> pokemonIds, final  PokeDetailsReceiver receiver) {
        manyPokes(pokemonIds, receiver, PokeSort.ASCENDING);
    }


    public void manyPokes(List<Integer> pokemonIds, final PokeDetailsReceiver receiver, final PokeSort sort) {
        GenericAdapter<PokemonDescription> a =
                new GenericAdapter<>(PokeClient.POKEAPI_ENDPOINT, PokemonDescription.class);

        final PokeClient service = a.adapter.create(PokeClient.class);

        detailsSubscription = rx.Observable.from(pokemonIds).flatMap(new Func1<Integer,
                Observable<PokemonDescription>>() {
            @Override
            public Observable<PokemonDescription> call(Integer id) {
                return service.getPokemonDescription(id);
            }
        }).doOnSubscribe(onStart).doOnCompleted(onEnd)
                .subscribeOn(Schedulers.trampoline())
                .observeOn(AndroidSchedulers.mainThread())
                .toSortedList(new Func2<PokemonDescription, PokemonDescription, Integer>() {
                    @Override
                    public Integer call(PokemonDescription p1,
                                        PokemonDescription p2) {
                        switch (sort) {
                            case ASCENDING:
                                return p1.id < p2.id ? -1 : 1;
                            default:
                                return p1.id > p2.id ? -1 : 1;
                        }
                    }
                })
                .subscribe(new Action1<List<PokemonDescription>>() {
                    @Override
                    public void call(List<PokemonDescription> pokemonDescriptions) {
                        receiver.onReceived(pokemonDescriptions);
                    }
                }, onError);
    }

    public void singlePoke(Integer pokemonId, final PokeDetailReceiver receiver) {

        GenericAdapter<PokemonDescription> a =
                new GenericAdapter<>(PokeClient.POKEAPI_ENDPOINT, PokemonDescription.class);
        detailsSubscription = a.adapter.create(PokeClient.class).getPokemonDescription(pokemonId)
                .doOnSubscribe(onStart).doOnCompleted(onEnd)
                .subscribeOn(Schedulers.trampoline())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(new Action1<PokemonDescription>() {
                    @Override
                    public void call(PokemonDescription pokemonDescription) {
                        receiver.onReceived(pokemonDescription);
                    }
                }, onError);
    }

}
