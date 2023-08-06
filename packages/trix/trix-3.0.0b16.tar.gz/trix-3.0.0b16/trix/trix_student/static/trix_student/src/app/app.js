(function() {
  angular.module('trixStudent', ['ngCookies', 'ngRoute', 'ui.bootstrap', 'trixStudent.directives', 'trixStudent.assignments.controllers']).config([
    '$httpProvider',
    function($httpProvider) {
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      return $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    }
  ]).run([
    '$http',
    '$cookies',
    function($http,
    $cookies) {
      return $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
    }
  ]);

}).call(this);
