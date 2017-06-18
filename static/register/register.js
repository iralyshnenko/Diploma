angular.module('AttendanceJournal').controller('RegisterController', function ($scope, $mdToast, Api) {
    $scope.login = '';
    $scope.password = '';
    $scope.fio = '';
    $scope.errorMessage = undefined;
    $scope.showErrorMessage = function () {
        return $scope.errorMessage !== undefined;
    };
    $scope.register = function () {
        var data = {
            login: $scope.login,
            password: $scope.password,
            fio: $scope.fio
        };
        Api.send(Api.request('/auth/teacher/register', Api.POST, data), function success() {
            $scope.errorMessage = undefined;
            $scope.back();
            $mdToast.showSimple('Registration successful');
        }, function failure(status) {
            switch (status) {
                case 400:
                    $scope.errorMessage = 'User with this login already exists';
                    break;
                default:
                    $scope.errorMessage = 'Service is not available right now';
                    break;
            }
        });
    }
});