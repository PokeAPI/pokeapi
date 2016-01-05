
'use strict';

angular.module('pokeapi-core')

	.directive('sideNav', ['$window', function ($window) {

		return {

			restrict: 'EA',

			templateUrl: 'static/pokemon_v2/partials/side-nav.html',

			replace: true,

			link: function (scope) {

				function calculate () {

					console.log('scroll');
				}

				function getAnchorText (el) {

					return el.getAttribute('side-nav-title') || el.textContent;
				}

				scope.nav = [];
				var parent = null;
				var anchors = angular.element(document.querySelectorAll('[side-nav-parent], [side-nav-child]'));

				for (var i = 0; i < anchors.length; i++) {

					var anchor = anchors[i];

					if (anchor.hasAttribute('side-nav-parent')) {

						parent = {};
						parent.anchorText = getAnchorText(anchor);
						parent.el = anchor;
						parent.children = [];
						scope.nav.push(parent);

					} else {

						parent.children.push({

							anchorText: getAnchorText(anchor),
							el: anchor
						});

					}
				}

				angular.element($window).bind('scroll', calculate);
			},

			controller: ['$scope', function ($scope) {

				$scope.anchorize = function (str) {

					return str.replace(' ', '').toLowerCase();
				};
			}]
		};

	}]);