
angular.module('pokeapi-core')

	.directive('sideNav', ['$window', function ($window) {

		return {

			restrict: 'EA',

			templateUrl: 'static/pokemon_v2/partials/side-nav.html',

			replace: true,

			link: function (scope, element, attrs) {

				scope.nav = [];
				var parent = null;
				var anchors = angular.element(document.querySelectorAll('[side-nav-parent], [side-nav-child]'));

				for (i = 0; i < anchors.length; i++) {

					anchor = anchors[i];

					console.log(anchor);

					if (anchor.hasAttribute('side-nav-parent')) {

						parent = {};
						parent.anchorText = getAnchorText(anchor);
						parent.children = []
						scope.nav.push(parent);

					} else {

						parent.children.push({

							anchorText: getAnchorText(anchor)
						});

					}
				}

				console.log(scope.nav);

				function getAnchorText (el) {

					return el.getAttribute('side-nav-title') || anchor.textContent;
				}

				angular.element($window).bind('scroll', calculate);

				function calculate () {

					console.log('scroll');
				}
			}
		}

	}]);