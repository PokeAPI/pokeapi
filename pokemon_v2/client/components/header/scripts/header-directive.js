
'use strict';

angular.module('pokeapi-header')
	
	.directive('pokeapiHeader', function () {

		return {

			restrict: 'A',

			templateUrl: 'static/views/header.html',

			replace: true
		};
		
	});