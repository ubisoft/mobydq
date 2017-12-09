(function () {

  'use strict';

  angular.module('DataQualityApp', ['ngMaterial'])
  .config(function($mdThemingProvider) {
    $mdThemingProvider.theme('default')
    .primaryPalette('lime')
    .accentPalette('purple')
    .warnPalette('red')
    .backgroundPalette('grey')
    .dark();
  })
  .controller('AppController', ['$scope', '$log', '$http', '$mdToast', '$location',
    function($scope, $log, $http, $mdToast, $location) {

      $scope.BatchOwners = [];
      $scope.DataSources = [];
      $scope.Indicators = [];

      $http.get('/config', {params: {}}).
        success(function(result) {
          $scope.host = result.host;
          $scope.port = result.port;
          $scope.GetBatchOwners();
        }).
        error(function(error) {
          $log.log(error);
        });

        $scope.ApiRoute = function(endpoint) {
          $log.log("http://"+$scope.host+":"+$scope.port+"/dataquality/api/v1/"+endpoint);
          return "http://"+$scope.host+":"+$scope.port+"/dataquality/api/v1/"+endpoint;
        }


        $scope.GetBatchOwners = function() {
          $http.get($scope.ApiRoute('batchowners'), {params: {}}).
          success(function(result) {
            $scope.BatchOwners = result;
          }).
          error(function(error) {
            $log.log(error);
          });
        };

        $scope.PostBatchOwners = function(batch) {
          $http.post($scope.ApiRoute('batchowners'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.PutBatchOwners = function(batch) {
          $http.put($scope.ApiRoute('batchowners'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.DeleteBatchOwners = function(batch) {
          $http.delete($scope.ApiRoute('batchowners'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };


        $scope.GetDataSources = function() {
          $http.get($scope.ApiRoute('datasources'), {params: {}}).
          success(function(result) {
            $scope.DataSources = result;
          }).
          error(function(error) {
            $log.log(error);
          });
        };

        $scope.PostDataSources = function(datasource) {
          $http.post($scope.ApiRoute('datasources'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.PutDataSources = function(datasource) {
          $http.put($scope.ApiRoute('datasources'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.DeleteDataSources = function(datasource) {
          $http.delete($scope.ApiRoute('datasources'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };


        $scope.GetIndicators = function() {
          $http.get($scope.ApiRoute('indicators'), {params: {}}).
          success(function(result) {
            $scope.Indicators = result;
          }).
          error(function(error) {
            $log.log(error);
          });
        };

        $scope.PostIndicators = function(datasource) {
          $http.post($scope.ApiRoute('indicators'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.PutIndicators = function(datasource) {
          $http.put($scope.ApiRoute('indicators'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.DeleteIndicators = function(datasource) {
          $http.delete($scope.ApiRoute('indicators'), {}).
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
