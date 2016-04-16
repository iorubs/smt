(function () {
  'use strict';

  angular
    .module('smt.home.services')
    .factory('Home', Home);

  Home.$inject = ['$http'];

  function Home($http) {
    var Home = {
      bleu_score: bleu_score,
      meteor_score: meteor_score,
      nist_score: nist_score,
      translate: translate
    };

    return Home;

    function bleu_score(input, output) {
      return $http.post('api/v1/bleu-score/', {input: input, output: output});
    }

    function meteor_score(input, output) {
      return $http.post('api/v1/meteor-score/', {input: input, output: output});
    }

    function nist_score(input, output) {
      return $http.post('api/v1/nist-score/', {input: input, output: output});
    }

    function translate(input) {
      return $http.post('api/v1/translate/', {input: input});
    }

  }
})();
