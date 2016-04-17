//HomeController
(function () {
  'use strict';

  angular
    .module('smt.home.controllers')
    .controller('HomeController', [ '$scope', 'Home', function($scope, Home) {

		$scope.bleu_score = 0;
		$scope.meteor_score = 0;
		$scope.nist_score = 0;
		function getBleuScoreSuccessFn(data, status, headers, config) {
			$scope.bleu_score = data.data;
		}

		function getBleuScoreErrorFn(data, status, headers, config) {
			console.log(data.data);
		}


		function getMeteorScoreSuccessFn(data, status, headers, config) {
			$scope.meteor_score = data.data;
		}

		function getMeteorScoreErrorFn(data, status, headers, config) {
			console.log(data.data);
		}


		function getNistScoreSuccessFn(data, status, headers, config) {
			$scope.nist_score = data.data;
		}

		function getNistScoreErrorFn(data, status, headers, config) {
			console.log(data.data);
		}

		$scope.output = "Output";

		//Input Size
		$scope.inputSize = "0";

		//Translation Duration
		$scope.translationDuration = "0.0";
		
		//Output Size
		$scope.outputSize = "0";

		$scope.translate = function() {
			$scope.running = true;
			Home.translate($scope.input).then(translateScoreSuccessFn, translateScoreErrorFn);
		}

		function translateScoreSuccessFn(data, status, headers, config) {
			$scope.output = data.data.OUTPUT;
			$scope.inputSize = data.data.INPUT_SIZE;
			$scope.outputSize = data.data.OUTPUT_SIZE;
			$scope.translationDuration = data.data.DURATION;
			$scope.running = false;
			Home.bleu_score($scope.input, $scope.output).then(getBleuScoreSuccessFn, getBleuScoreErrorFn);
			Home.meteor_score($scope.input, $scope.output).then(getMeteorScoreSuccessFn, getMeteorScoreErrorFn);
			Home.nist_score($scope.input, $scope.output).then(getNistScoreSuccessFn, getNistScoreErrorFn);
		}

		function translateScoreErrorFn(data, status, headers, config) {
			console.log(data);
			$scope.running = false;
		}


    }]);
})();
