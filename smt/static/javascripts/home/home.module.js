(function () {
    'use strict';

    angular
        .module('smt.home', [
            'smt.home.controllers',
            'smt.home.services'
        ]);

    angular
        .module('smt.home.controllers', []);

    angular
        .module('smt.home.services', ['ngCookies']);
})();
