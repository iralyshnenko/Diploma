angular.module('AttendanceJournal', ['ngMaterial', 'ngRoute']).config(function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'overview/overview.html',
            controller: 'OverviewController'
        })
        .when('/login', {
            templateUrl: 'login/login.html',
            controller: 'LoginController'
        })
        .when('/register', {
            templateUrl: 'register/register.html',
            controller: 'RegisterController'
        })
        .when('/:entity/overview', {
            templateUrl: 'overview/overview.html',
            controller: 'OverviewController'
        })
        .when('/:parent/:id/:entity/overview', {
            templateUrl: 'overview/overview.html',
            controller: 'OverviewController'
        })
        .when('/:entity/edit/:id', {
            templateUrl: 'edit/edit.html',
            controller: 'EditController'
        })
        .when('/:entity/edit', {
            templateUrl: 'edit/edit.html',
            controller: 'EditController'
        });
}).controller('HeaderController', function ($scope, $mdSidenav, Api) {
    $scope.auth = Api.auth;
    $scope.toggleSideBar = function () {
        $mdSidenav('side-navigation').toggle();
    };
}).run(function ($rootScope, $location) {
    $rootScope.currentLocation = $rootScope.previousLocation = '/';
    $rootScope.$on('$routeChangeSuccess', function () {
        $rootScope.previousLocation = $rootScope.currentLocation;
        $rootScope.currentLocation = $location.$$path;
    });
    $rootScope.back = function () {
        $location.path($rootScope.previousLocation);
    }
});