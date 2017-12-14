(function () {

  'use strict';

  angular.module('DataQualityApp', ['ngMaterial'])
  .config(function($mdThemingProvider) {
    $mdThemingProvider.theme('default')
      .dark();
  })
  .controller('AppController', ['$scope', '$log', '$http', '$mdToast', '$location',
    function($scope, $log, $http, $mdToast, $location) {
      $log.log("Controller initialiation");

      $scope.data = {
        BatchOwners: [],
        DataSource: [],
        DataSourceTypes: [],
        EventTypes: []
      }

      $scope.currentModel = 'BatchOwners';
      $scope.models = {
        'BatchOwners': {'name': 'string'},
        'DataSource': {'name': 'string'},
        'DataSourceTypes': {'name': 'string', 'type': 'string'},
        'EventTypes': {'name': 'string'}
      };

      $scope.new = {};

      $http.get('/config', {params: {}}).
        success(function(result) {
          $log.log("Config fetched: ");
          $scope.host = result.api.host;
          $scope.port = result.api.port;
          $scope.GetModel($scope.model);
        }).
        error(function(error) {
          $log.log(error);
        });

        $scope.ApiRoute = function(endpoint) {
          $log.log("http://"+$scope.host+":"+$scope.port+"/dataquality/api/v1/"+endpoint);
          return "http://"+$scope.host+":"+$scope.port+"/dataquality/api/v1/"+endpoint;
        }

        $scope.GetModel = function(model) {
          $scope.currentModel = model;
          $scope.new = {};
          $http.get($scope.ApiRoute(model.toLowerCase()), {params: {}}).
          success(function(result) {
            $log.log(model + "fetched: " + result);
            $scope.data[model] = result;
          }).
          error(function(error) {
            $log.log(error);
          });
        };

        $scope.PostModel = function(model, batch) {
          $http.post($scope.ApiRoute(model.toLowerCase()), $scope.new).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.PutModel = function(model, batch) {
          $http.put($scope.ApiRoute(model.toLowerCase()), $scope.new).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.DeleteModel = function(model, batch) {
          $http.delete($scope.ApiRoute(model.toLowerCase()), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.showSuccessToast = function() {
          $mdToast.show(
            $mdToast.simple()
              .textContent('Success')
              .position('bottom center')
              .theme("success-toast")
          );
        };

      }
  ]);

}());
