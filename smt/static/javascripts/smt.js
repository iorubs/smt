(function () {
    'use strict';

    angular
        .module('smt', [
            'smt.config',
            'smt.routes',
            'smt.home',
        ])
        .run(run);

    run.$inject = ['$http'];

    function run($http) {
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';
    }

    angular
        .module('smt.config', []);

    angular
        .module('smt.routes', ['ngRoute']);
})();
