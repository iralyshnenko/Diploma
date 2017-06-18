angular.module('AttendanceJournal').controller('AttendanceDialogController', function ($scope, $mdDialog, Api) {
    $scope.subjects = [];
    $scope.selectedSubject = null;

    $scope.confirm = function () {
        if ($scope.selectedSubject !== null) {
            $mdDialog.hide($scope.selectedSubject);
        }
    };
    $scope.cancel = function () {
        $mdDialog.cancel();
    };

    Api.send(Api.request('/api/subject', Api.GET), function success(data) {
        $scope.subjects = data;
    }, function failure() {
        $mdDialog.cancel();
    });
});