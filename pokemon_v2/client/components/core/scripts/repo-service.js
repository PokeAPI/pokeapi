
'use strict';

angular.module('pokeapi-core')

    .factory('RepoService', ['$http',

        function ($http) {

        	var BASE_URL = "http://api.github.com/repos/phalt/pokeapi/"
            var CONTRIBUTORS_PATH = BASE_URL + "contributors";

            var service = {};

        	service.getContributors = function () {

        		var cb = $http
                    .get(CONTRIBUTORS_PATH)
                    .then(function (response) {
						return response;
                    });

                return cb;
        	}

        	return service;
        }
    ]);