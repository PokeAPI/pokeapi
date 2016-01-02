
(function () {

    'use strict';

    angular.module('pokeapi_v2', [
        'pokeapi-core',
    	'pokeapi-header',
        'pokeapi-home',
        'pokeapi-about',
        'pokeapi-docs',
        'pokeapi-contributors'
    ])

    .config(['$locationProvider', '$stateProvider',

        function ($locationProvider, $stateProvider) {

            $locationProvider.html5Mode(true);

            // Allow navigation to V1. Leaves the single page app.
            $stateProvider.state('v1', {

                url         : 'v1/',
                controller  : function () {

                    window.location.reload(true);
                }
            });
        }
    ]);

})();