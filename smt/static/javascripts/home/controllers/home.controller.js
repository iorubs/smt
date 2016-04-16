//HomeController
(function () {
  'use strict';

  angular
    .module('smt.home.controllers')
    .controller('HomeController', [ '$scope', 'Home', function($scope, Home) {

		Home.bleu_score("some input", "some output").then(getBleuScoreSuccessFn, getBleuScoreErrorFn);

		function getBleuScoreSuccessFn(data, status, headers, config) {
			$scope.bleu_score = data.data;
		}

		function getBleuScoreErrorFn(data, status, headers, config) {
			console.log(data.data);
		}

		Home.meteor_score("some input", "some output").then(getMeteorScoreSuccessFn, getMeteorScoreErrorFn);

		function getMeteorScoreSuccessFn(data, status, headers, config) {
			$scope.meteor_score = data.data;
		}

		function getMeteorScoreErrorFn(data, status, headers, config) {
			console.log(data.data);
		}

		Home.nist_score("some input", "some output").then(getNistScoreSuccessFn, getNistScoreErrorFn);

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
			Home.translate($scope.input).then(translateScoreSuccessFn, translateScoreErrorFn);
		}

		function translateScoreSuccessFn(data, status, headers, config) {
			$scope.output = data.data.OUTPUT;
			$scope.inputSize = data.data.INPUT_SIZE;
			$scope.outputSize = data.data.OUTPUT_SIZE;
			$scope.translationDuration = data.data.DURATION;
		}

		function translateScoreErrorFn(data, status, headers, config) {
			console.log(data);
		}


    }]);
})();
