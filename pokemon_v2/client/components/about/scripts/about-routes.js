
(function () {

	'use strict';

	angular.module('pokeapi-about')

	.config(['$stateProvider', function ($stateProvider) {

		$stateProvider.state('about', {

			url         : '/about',
			templateUrl : 'static/pokemon_v2/partials/about.html'
		});

	}]);

})();