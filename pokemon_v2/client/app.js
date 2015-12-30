
(function () {

    'use strict';

    angular.module('pokeapi_v2', [
    	'pokeapi-header'
    ])

    .config(['$locationProvider', '$httpProvider',

        function ($locationProvider, $httpProvider) {

            $locationProvider.html5Mode(true);

            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }
    ]);

})();