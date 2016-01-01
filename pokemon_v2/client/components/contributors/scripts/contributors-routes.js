
(function () {

	'use strict';

	angular.module('pokeapi-contributors')

	.config(['$stateProvider', function ($stateProvider) {

		$stateProvider.state('contributors', {

			url         : '/contributors',
			templateUrl : 'static/pokemon_v2/partials/contributors.html',
			controller 	: 'ContributorsController'
		});

	}]);

})();