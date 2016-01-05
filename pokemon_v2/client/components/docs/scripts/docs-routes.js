
(function () {

	'use strict';

	angular.module('pokeapi-docs')

	.config(['$stateProvider', function ($stateProvider) {

		$stateProvider.state('docs', {

			url         : '/documentation',
			templateUrl : 'static/pokemon_v2/partials/docs2.html',
			controller 	: 'DocsController'
		});

	}]);

})();