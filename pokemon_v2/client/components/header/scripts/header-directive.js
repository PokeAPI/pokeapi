
'use strict';

angular.module('pokeapi-header')
	
	.directive('pokeapiHeader', function () {

		return {

			restrict: 'A',

			templateUrl: 'static/pokemon_v2/partials/header.html',

			replace: true
		};
		
	});