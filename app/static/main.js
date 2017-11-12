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

      $scope.BatchOwners = [];
      $scope.DataSource = [];
      $scope.DataSourceTypes = [];
      $scope.EventTypes = [];

      $http.get('/config', {params: {}}).
        success(function(result) {
          $log.log("Config fetched: ");
          $scope.host = result.api.host;
          $scope.port = result.api.port;
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
            $log.log("BatchOwner fetched: " + result);
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
            $log.log("DataSource fetched: " + result);
            $scope.DataSource = result;
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


        $scope.GetDataSourceTypes = function() {
          $http.get($scope.ApiRoute('datasourcetypes'), {params: {}}).
          success(function(result) {
            $log.log("DataDourceType fetched: " + result);
            $scope.DataSourceTypes = result;
          }).
          error(function(error) {
            $log.log(error);
          });
        };

        $scope.PostDataSourceTypes = function(datasourcetype) {
          $http.post($scope.ApiRoute('datasourcetypes'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.PutDataSourceTypes = function(datasourcetype) {
          $http.put($scope.ApiRoute('datasourcetypes'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.DeleteDataSourceTypes = function(datasourcetype) {
          $http.delete($scope.ApiRoute('datasourcetypes'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };


        $scope.GetEventTypes = function(eventType) {
          $http.get($scope.ApiRoute('eventtypes'), {params: {}}).
          success(function(result) {
            $log.log("EventType fetched: " + result);
            $scope.EventTypes = result;
          }).
          error(function(error) {
            $log.log(error);
          });
        };

        $scope.PostEventTypes = function(eventType) {
          $http.post($scope.ApiRoute('eventtypes'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.PutEventTypes = function(eventType) {
          $http.put($scope.ApiRoute('eventtypes'), {}).
            success(function(results) {
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.DeleteEventTypes = function(eventType) {
          $http.delete($scope.ApiRoute('eventtypes'), {}).
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
