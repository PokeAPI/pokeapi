
'use strict';

angular.module('pokeapi-home')
	
	.controller('HomeController', ['$scope', 'APIService',

		function ($scope, API) {

			$scope.loading = false;
			$scope.failure = false;
			$scope.dropdownExpanded = false;
			$scope.endpointIndex = 5;
			$scope.endpointOptions = [
				'ability/',
				'egg-group/',
				'item/',
				'move/',
				'pokedex/',
				'pokemon-species/',
				'type/'
			];
			$scope.resourceID = '1';
			$scope.resource = null;

			$scope.toggleDropdown = function () {

				$scope.dropdownExpanded = !$scope.dropdownExpanded;
			};

			$scope.setEndpoint = function (index) {

				$scope.endpointIndex = index;
			};

			$scope.getResource = function () {

				$scope.loading = true;

				API.getResource($scope.endpointOptions[$scope.endpointIndex], $scope.resourceID).then( 

					function (response) {

						if (response.status === 200) {

							$scope.resource = response.data;
							intercept();

						} else {

							$scope.failure = true;
						}

						$scope.loading = false;
					}
				)
			};

			$scope.getResource();

			function intercept () {

				var links = document.querySelector('.json-body a');


			}
		}

	]);


