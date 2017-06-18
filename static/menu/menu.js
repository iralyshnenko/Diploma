angular.module('AttendanceJournal').controller('MenuController', function ($scope, $mdBottomSheet) {
    $scope.actions = [
        {
            icon: 'edit',
            action: 'edit',
            name: 'Edit'
        },
        {
            icon: 'delete',
            action: 'delete',
            name: 'Delete'
        }
    ];
    $scope.doAction = function (action) {
        $mdBottomSheet.hide(action);
    };
}).controller('GroupMenuController', function ($scope, $mdBottomSheet) {
    $scope.actions = [
        {
            icon: 'account_circle',
            action: 'student',
            name: 'Show students'
        },
        {
            icon: 'edit',
            action: 'edit',
            name: 'Edit'
        },
        {
            icon: 'delete',
            action: 'delete',
            name: 'Delete'
        }
    ];
    $scope.doAction = function (action) {
        $mdBottomSheet.hide(action);
    };
}).controller('StudentMenuController', function ($scope, $mdBottomSheet) {
    $scope.actions = [
        {
            icon: 'check_circle',
            action: 'attendance',
            name: 'Show attended days'
        },
        {
            icon: 'insert_invitation',
            action: 'mark_attendance',
            name: 'Attended today'
        },
        {
            icon: 'grade',
            action: 'score',
            name: 'Show scores'
        },
        {
            icon: 'star_half',
            action: 'add_score',
            name: 'Put mark'
        },
        {
            icon: 'edit',
            action: 'edit',
            name: 'Edit'
        },
        {
            icon: 'delete',
            action: 'delete',
            name: 'Delete'
        }
    ];
    $scope.doAction = function (action) {
        $mdBottomSheet.hide(action);
    };
});