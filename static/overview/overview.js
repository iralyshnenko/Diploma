angular.module('AttendanceJournal').controller('OverviewController', function ($scope, $routeParams, $location,
                                                                               $mdToast, $mdBottomSheet, $mdDialog,
                                                                               Api) {
    function referenceAttribute(item) {
        return item.indexOf($scope.parent.name) > -1 && item.indexOf('_id') > -1;
    }
    function onlyChildren(item) {
        return item[$scope.parent.referenceAttribute] === $scope.parent.id;
    }
    function shouldFilter() {
        return $scope.parent.name !== undefined && $scope.parent.id !== undefined;
    }
    function isReadOnly(entity) {
        return ['student_performance', 'attendance', 'score', 'teacher'].indexOf(entity) > -1;
    }
    function urlToEntityName(url) {
        return url === undefined ? 'student_performance' : url;
    }
    function getAttributes(entity) {
        var attributes = {
            group: ['id', 'name'],
            student: ['id', 'fio', 'student_group_id'],
            teacher: ['id', 'fio'],
            subject: ['id', 'name', 'teacher_id'],
            score: ['id', 'international', 'percentage', 'student_id', 'subject_id'],
            attendance: ['id', 'attendance_date', 'student_id', 'subject_id'],
            student_performance: ['id', 'fio', 'student_group_id', 'attended_days', 'performance']
        };
        return attributes[entity];
    }
    function getMenuController(entity) {
        var controllers = {
            group: 'GroupMenuController',
            student: 'StudentMenuController'
        };
        return controllers[entity] || 'MenuController';
    }
    function formatValue(value) {
        var values = value.split('_');
        values.forEach(function (item, index) {
            values[index] = item.charAt(0).toUpperCase() + item.substr(1)
        });
        return values.join(' ');
    }
    function getEntityContext(rawEntityName) {
        rawEntityName = urlToEntityName(rawEntityName);
        return {
            rawEntityName: rawEntityName,
            prettyEntityName: formatValue(rawEntityName),
            attributes: getAttributes(rawEntityName),
            menuController: getMenuController(rawEntityName),
            isReadOnly: isReadOnly(rawEntityName)
        };
    }
    function loadData() {
        $scope.entity = getEntityContext($routeParams.entity);
        $scope.parent = {
            name: $routeParams.parent,
            id: parseInt($routeParams.id)
        };
        $scope.parent.referenceAttribute = $scope.entity.attributes.find(referenceAttribute);
        var url = '/api/' + $scope.entity.rawEntityName;
        Api.send(Api.request(url, Api.GET), function success(data) {
            $scope.dataList = shouldFilter() ? data.filter(onlyChildren) : data;
        }, function failure(status) {
            switch (status) {
                case 401:
                    $mdToast.showSimple('"Sign In" to do that');
                    break;
                default:
                    $mdToast.showSimple('Service is not available right now');
                    break;
            }
        });
    }
    function deleteEntity(item) {
        var url = '/api/' + $scope.entity.rawEntityName + '/' + item.id;
        var entityDescription = $scope.entity.prettyEntityName + ' with Id - ' + item.id;
        Api.send(Api.request(url, Api.DELETE), function success() {
            $mdToast.showSimple(entityDescription + ' was successfully deleted');
            loadData();
        }, function failure(status) {
            switch (status) {
                case 400:
                    $mdToast.showSimple('Cannot delete ' + entityDescription);
                    break;
                case 401:
                    $mdToast.showSimple('"Sign In" to do that');
                    break;
                default:
                    $mdToast.showSimple('Service is not available right now');
                    break;
            }
        });
    }
    function addAttendance(item) {
        var date = new Date();
        var rawDate = [date.getFullYear(), date.getMonth(), date.getDate()].join('-');
        var readableDate = date.toDateString();
        $mdDialog.show({
            controller: 'AttendanceDialogController',
            templateUrl: 'attendance-dialog/attendance-dialog.html',
            clickOutsideToClose: true
        }).then(function (subject) {
            var data = {
                attendance_date: rawDate,
                subject_id: subject.id,
                student_id: item.id
            };
            Api.send(Api.request('/api/attendance', Api.POST, data), function success() {
                $mdToast.showSimple(item.fio + ' attended ' + subject.name + ' ' + readableDate);
            }, function failure(status) {
                switch (status) {
                    case 400:
                        $mdToast.showSimple(item.fio + ' has already attended ' + subject.name + ' today');
                        break;
                    case 401:
                        $mdToast.showSimple('"Sign In" to do that');
                        break;
                    case 403:
                        $mdToast.showSimple(subject.name + ' is not your subject');
                        break;
                    default:
                        $mdToast.showSimple('Service is not available right now');
                        break;
                }
            })
        });
    }
    function addScore(item) {
        $mdDialog.show({
            controller: 'ScoreDialogController',
            templateUrl: 'score-dialog/score-dialog.html',
            clickOutsideToClose: true
        }).then(function (formData) {
            var subject = formData.subject;
            var score = formData.score;
            var data = {
                international: score.international,
                percentage: score.percentage,
                student_id: item.id,
                subject_id: subject.id
            };
            Api.send(Api.request('/api/score', Api.POST, data), function success() {
                $mdToast.showSimple(item.fio + ' got "' + score.international + '" at ' + subject.name);
            }, function failure(status) {
                switch (status) {
                    case 401:
                        $mdToast.showSimple('"Sign In" to do that');
                        break;
                    case 403:
                        $mdToast.showSimple(subject.name + ' is not your subject');
                        break;
                    default:
                        $mdToast.showSimple('Service is not available right now');
                        break;
                }
            });
        });
    }

    $scope.formatValue = formatValue;
    $scope.getRowClass = function (value) {
        return typeof value === 'string' ? 'mdl-data-table__cell--non-numeric' : '';
    };
    $scope.createEntity = function () {
        var url = '/' + $scope.entity.rawEntityName + '/edit';
        $location.path(url);
    };
    $scope.showActionsMenu = function (item) {
        if ($scope.entity.isReadOnly) {
            return;
        }
        $mdBottomSheet.show({
            templateUrl: 'menu/menu.html',
            controller: $scope.entity.menuController
        }).then(function (action) {
            var url;
            switch (action) {
                case 'edit':
                    url = '/' + $scope.entity.rawEntityName + '/edit/' + item.id;
                    $location.path(url);
                    break;
                case 'delete':
                    deleteEntity(item);
                    break;
                case 'mark_attendance':
                    addAttendance(item);
                    break;
                case 'add_score':
                    addScore(item);
                    break;
                default:
                    url = '/' + $scope.entity.rawEntityName + '/' + item.id + '/' + action + '/overview';
                    $location.path(url);
                    break;
            }
        });
    };

    loadData();
});