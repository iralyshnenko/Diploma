function Auth(api) {
    this.localStorage = window.localStorage;
    this.login = this.localStorage.getItem('login');
    this.password = this.localStorage.getItem('password');
    this.fio = this.localStorage.getItem('fio');
    this.api = api;
}
Auth.prototype.authorize = function (login, password, onSuccess, onFailure) {
    var obj = this;
    var Api = this.api;
    this.login = login;
    this.password = password;
    Api.send(Api.request('/api/teacher', Api.GET), function success(data) {
        var authorizedEntity = data.find(function (item) {
            return item.login === login;
        });
        if (authorizedEntity !== undefined) {
            obj.fio = authorizedEntity.fio;
            obj.localStorage.setItem('login', obj.login);
            obj.localStorage.setItem('password', obj.password);
            obj.localStorage.setItem('fio', obj.fio);
            onSuccess(data);
        }
        else {
            onFailure(401);
        }
    }, onFailure);
};
Auth.prototype.logout = function () {
    this.localStorage.clear();
    this.login = null;
    this.password = null;
    this.fio = null;
};
Auth.prototype.isAuthorized = function () {
    return this.login !== null && this.password !== null && this.fio !== null;
};
Auth.prototype.makeHeader = function () {
    if (this.login !== undefined && this.password !== undefined) {
        return {'Authorization': [this.login, this.password].join(' ')};
    }
    else {
        return {};
    }
};

angular.module('AttendanceJournal').service('Api', function ($http) {
    this.GET = 'GET';
    this.POST = 'POST';
    this.PUT = 'PUT';
    this.DELETE = 'DELETE';
    this.auth = new Auth(this);

    this.request = function (url, method, data) {
        return {
            url: url,
            method: method,
            data: data
        };
    };
    this.send = function (request, onSuccess, onFailure) {
        var headers = this.auth.makeHeader();
        $http({
            method: request.method,
            url: request.url,
            data: request.data,
            headers: headers
        }).then(function success(response) {
            onSuccess(response.data);
        }, function failure(response) {
            onFailure(response.status);
        });
    }
});