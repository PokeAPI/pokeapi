
'use strict';

angular.module('pokeapi-core')

    .factory('APIService', ['$http',

        function ($http) {

        	var BASE_URL = "api/v2/";
            var ID = '/{id}';

            // var ABILITY = BASE_URL + "ability";
            // var ABILITY_DETAIL = ABILITY + ID

            var service = {};

        	service.getResource = function (endpoint, id) {

        		var cb = $http
                    .get(BASE_URL + endpoint + id)
                    .then(function (response) {
						return response;
                    });

                return cb;
        	}

        	return service;
        }
    ]);