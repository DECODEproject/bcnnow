/*********************************************************************************************************************
                                                    GLOBAL VARIABLES 
**********************************************************************************************************************/
//var url_api = 'http://93ff8837.ngrok.io/api/v0/'; // Get the endpoint url of BarcelonaNow API
//var url_api = 'http://172.20.120.110:9530/api/v0/'; // Get the endpoint url of BarcelonaNow API
//var url_root = 'http://172.20.120.110:9530/';
var url_api = 'http://127.0.0.1:8080/api/v0/'; // Get the endpoint url of BarcelonaNow API
var url_root = 'http://127.0.0.1:8080/';
var dashboards = getDashboards(); // Get the available dashboards from MongoDB
var datasets = getDatasets(); // Get the available datasets from MongoDB
var private_dashboards = getPrivateDashboards(); // Get the available dashboards from MongoDB
var page = 'page-6'; // + (Object.keys(dashboards).length - 1); // Get the current dashboard to show (the last by default)
var color_palette = ['#4D9DE0', '#E15554', '#E1BC29', '#3BB273', '#7768AE']; // Default color palette for time series
var start_date = moment().subtract('days', 6).toISOString();
var end_date = moment().toISOString();
