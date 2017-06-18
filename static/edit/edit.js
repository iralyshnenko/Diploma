angular.module('AttendanceJournal').controller('EditController', function ($scope, $mdToast, $routeParams, Api) {
    function getAttributes(entity) {
        var attributes = {
            group: ['name'],
            student: ['fio', 'student_group_id'],
            subject: ['name', 'teacher_id']
        };
        return attributes[entity];
    }
    function formatValue(value) {
        var values = value.split('_');
        values.forEach(function (item, index) {
            values[index] = item.charAt(0).toUpperCase() + item.substr(1)
        });
        return values.join(' ');
    }
    function getEntityContext(rawEntityName) {
        return {
            rawEntityName: rawEntityName,
            prettyEntityName: formatValue(rawEntityName),
            attributes: getAttributes(rawEntityName)
        };
    }

    $scope.formatValue = formatValue;
    $scope.showErrorMessage = function () {
        return $scope.errorMessage !== undefined;
    };
    $scope.apply = function () {
        var url = $scope.currentEntity.id !== undefined ? $scope.url + '/' + $scope.currentEntity.id : $scope.url;
        var method = $scope.currentEntity.id !== undefined ? Api.PUT : Api.POST;
        Api.send(Api.request(url, method, $scope.currentEntity), function success() {
            $mdToast.showSimple('Changes to ' + $scope.entity.prettyEntityName + ' are successfully applied');
            $scope.back();
        }, function failure(status) {
            switch (status) {
                case 400:
                    $scope.errorMessage = 'Cannot apply changes to ' + $scope.entity.prettyEntityName;
                    break;
                case 401:
                    $scope.errorMessage = '"Sign In" to do that';
                    break;
                default:
                    $scope.errorMessage = 'Service is not available right now';
                    break;
            }
        })
    };

    $scope.entity = getEntityContext($routeParams.entity);
    $scope.url = '/api/' + $scope.entity.rawEntityName;
    $scope.currentEntity = {};
    $scope.errorMessage = undefined;
    var id = $routeParams.id;
    if (id !== undefined) {
        Api.send(Api.request($scope.url, Api.GET), function success(data) {
            if (data.length === 0) {
                $mdToast.showSimple('Looks like this ' + $scope.entity.prettyEntityName + ' was just deleted');
            }
            else {
                $scope.currentEntity = data.pop();
            }
        }, function failure(status) {
            switch (status) {
                case 401:
                    $scope.errorMessage = '"Sign In" to do that';
                    break;
                default:
                    $scope.errorMessage = 'Service is not available right now';
                    break;
            }
        })
    }
});