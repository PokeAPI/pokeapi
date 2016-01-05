
'use strict';

angular.module('pokeapi-core')

	.directive('markdown', ['$window', function ($window) {

		return {

			restrict: 'EA',

			link: function (scope, el) {
				
				el.html(marked(el.text(), {
					gfm: true,
					sanitize: true
				}));
			}
		};

	}]);