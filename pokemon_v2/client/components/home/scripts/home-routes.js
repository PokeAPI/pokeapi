
(function () {

	'use strict';

	angular.module('pokeapi-home')

	.config(['$stateProvider', function ($stateProvider) {

		$stateProvider.state('home', {

			url         : '/',
			templateUrl : 'static/pokemon_v2/partials/home.html',
			controller 	: 'HomeController'
		});

	}]);

})();