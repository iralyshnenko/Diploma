angular.module('AttendanceJournal').controller('ScoreDialogController', function ($scope, $mdDialog, Api) {
    function getInternational(percentage) {
        if (100 >= percentage && percentage >= 90) {
            return 'A';
        }
        else if (89 >= percentage && percentage >= 80) {
            return 'B';
        }
        else if (79 >= percentage && percentage >= 70) {
            return 'C';
        }
        else if (69 >= percentage && percentage >= 60) {
            return 'D';
        }
        else {
            return 'E';
        }
    }

    $scope.percentage = 0;
    $scope.subjects = [];
    $scope.selectedSubject = null;
    $scope.confirm = function () {
        if ($scope.selectedSubject !== null) {
            $mdDialog.hide({
                subject: $scope.selectedSubject,
                score: {
                    international: getInternational($scope.percentage),
                    percentage: $scope.percentage
                }
            });
        }
    };
    $scope.cancel = function () {
        $mdDialog.cancel();
    };
    Api.send(Api.request('/api/subject', Api.GET), function success(data) {
        $scope.subjects = data;
    }, function failure() {
        $mdDialog.cancel();
    })
});