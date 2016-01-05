
'use strict';

angular.module('pokeapi-core')

    .factory('APIService', ['$http',

        function ($http) {

        	var BASE_URL = 'api/v2/';
            var service = {};

        	service.getResource = function (endpoint, id) {

                if (id) {

                    id = id + '/';
                }

        		var cb = $http
                    .get(BASE_URL + endpoint + id)
                    .then(function (response) {
						return response;
                    });

                return cb;
        	};

        	return service;
        }
    ]);