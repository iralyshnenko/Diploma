angular.module('AttendanceJournal').controller('LoginController', function ($scope, $mdToast, $location, Api) {
    $scope.login = '';
    $scope.password = '';
    $scope.errorMessage = undefined;
    $scope.showErrorMessage = function () {
        return $scope.errorMessage !== undefined;
    };
    $scope.authorize = function () {
        Api.auth.authorize($scope.login, $scope.password, function success() {
            $scope.errorMessage = undefined;
            $scope.back();
            $mdToast.showSimple('Welcome, ' + Api.auth.fio);
        }, function failure(status) {
            switch (status) {
                case 401:
                    $scope.errorMessage = 'Wrong login or password';
                    break;
                default:
                    $scope.errorMessage = 'Service is not available right now';
                    break;
            }
        });
    }
});