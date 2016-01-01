
'use strict';

angular.module('pokeapi-contributors')
	
	.controller('ContributorsController', [ '$scope', 'RepoService',

		function ($scope, Repo) {

			$scope.failure = false;
			$scope.contributors = [];

			Repo.getContributors().then( function (response) {

				if (response.status == 200) {

					$scope.contributors = response.data;
					console.log(response);

				} else {

					$scope.failure = true;
				}

			});
		}

	]);


