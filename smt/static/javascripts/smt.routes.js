(function () {
    'use strict';

    angular
        .module('smt.routes')
        .config(config);

    config.$inject = ['$routeProvider'];

    function config($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: '/static/templates/home/home.html'
        }).otherwise('/');
    }
})();
