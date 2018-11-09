/*********************************************************************************************************************
                                                    GLOBAL VARIABLES 
**********************************************************************************************************************/

var url_api = 'http://127.0.0.1:9530/api/v0/'; // Get the endpoint url of BarcelonaNow API
var datasets = getDatasets(); // Get the available datasets from datasets.js file
var dashboards = getDashboards(); // Get the available dashboards from dashboards.js file
var page = 'page-5';// + (Object.keys(dashboards).length - 1); // Get the current dashboard to show (the last by default)
var color_palette = ['#4D9DE0', '#E15554', '#E1BC29', '#3BB273', '#7768AE']; // Default color palette for time series
var start_date = moment().subtract('days', 6).toISOString();
var end_date = moment().toISOString();

/********************************************************************************************************************
                                                    SHARE
*********************************************************************************************************************/

/*
    Adds a listener to the shared dashboard icon, so that a Google short url is created after the user clicks on it
*/
function addEventsShareDashboard() {
    $('#popup-dashboard').click(function(e){
        var page_id = page;
        var shared_widgets = {'widgets': []};
        dashboards[page_id]['widgets'].forEach(function(widget, windex){
            shared_widget = widget;
            shared_widget['sources'].forEach(function(source, sindex){
                widget['map'] = null;
                widget['sources'][sindex]['markers'] = null;
                widget['sources'][sindex]['dataset'] = null;
                widget['timeinterval'] = null;
            });
            shared_widgets.widgets.push(shared_widget);
        });
        makeShort('Copy this link to share your dashboard', window.location.href + '?widgets=' + JSON.stringify(shared_widgets));
    });
}

/*
    Adds a listener to the shared widget icon, so that a Google short url is created after the user clicks on it
    @element The shared widget icon object clicked by the user
*/
function addEventsShareWidget(element) {
    var widget_id = dashboards[page]['widgets'][$(element).attr('id').split('-')[0]]['id'];
    var page_id = page;
    var shared_widget = {};
    dashboards[page_id]['widgets'].forEach(function(widget, windex){
        if(widget['id'] == widget_id) {
            shared_widget = widget;
            shared_widget['sources'].forEach(function(source, sindex){
                widget['sources'][sindex]['markers'] = null;
                widget['sources'][sindex]['dataset'] = null;
                widget['map'] = null;
                widget['timeinterval'] = null;
                widget['highmarkericon'] = [];
                widget['refreshIntervalId'] = null;
                widget['highmarker'] = [];
                widget['data'] = [];
            });
        }
    });

    makeShort('Copy this link to share your widget', window.location.href + '?widget=' + JSON.stringify(shared_widget));
}

/*
    Opens a dialog showing the short url associated to the requested resource (widget or dashboard)
    @text The text to show in the dialog
    @link The long url to the requested resource
*/
function makeShort(text, link, show=true){
        gapi.client.setApiKey('AIzaSyBnD5ih866EjgWgzL01iTjngGMWaSdFhiw');
        gapi.client.load('urlshortener', 'v1', function(){
            var request = gapi.client.urlshortener.url.insert({
                'resource': {
                    'longUrl': link
                }
            });
            request.execute(function(response)  {
                if(show) {
                    try {
                        BootstrapDialog.alert({
                            title: text,
                            message: '<a href="' + response.id + '" target="_blank">' + response.id + '</a>'
                        });
                    }
                    catch(err) {
                    }
                }
            });
        });
    }

$(document).ready(function() {

    /*********************************************************************************************************************
                                                        DRAG&DROP
    **********************************************************************************************************************/

    /*

    */
    var previous_position = -1;

    /*
    */
    function array_move(arr, old_index, new_index) {
        if (new_index >= arr.length) {
            var k = new_index - arr.length + 1;
            while (k--) {
                arr.push(undefined);
            }
        }
        arr.splice(new_index, 0, arr.splice(old_index, 1)[0]);
        return arr;
    }

    /*
    */
    function dragDropSamePage() {
         $( "#sortable" ).sortable({
            handle: ".panel-heading",
            start: function (event, ui) {
                previous_position = ui.item.index();
            },
            stop:  function (event, ui) {
                dashboards[page]['widgets'] = array_move(dashboards[page]['widgets'], previous_position, ui.item.index());
            }
        });
        $("#sortable").disableSelection();
    }

    /*
    */
    function dragDropDifferentPage(id) {
        var windex = "0";
        $.each(dashboards[page]['widgets'], function(index, element) {
            if(element['id'] == id) {
                windex = index;
            }
        });

        var widget = dashboards[page]['widgets'][windex];

        var message = '<div class="form-group">' +
                        '<label for="sel1">Select the target dashboard:</label>' +
                        '<select class="form-control" id="' + widget['id'] + '-' + windex + '-select-dashboard">';
                        $.each(dashboards, function(index, element) {
                            message += '<option value="' + index + '" ' + ((index == page) ? 'selected' : '') + '>' + element['name'] + '</option>';
                        });
        message +=      '</select>' +
                      '</div>';

        var text = 'Move "' + widget['title'] + '" to another dashboard';

        // Move widget
        var script = "<script>" +
                        "$('#" + widget['id'] + "-" + windex + "-select-dashboard').on('change', function() { " +
                            "new_page = this.value;" +
                            "old_index = $(this).attr('id').split('-')[2];" +
                            "dashboards[new_page]['widgets'].push(dashboards[page]['widgets'][old_index]);" +
                            "$.notify('You have moved the widget ' + dashboards[page]['widgets'][old_index]['title'] + ' on ' + dashboards[new_page]['name'] + ' dashboard.', 'success');" +
                            "dashboards[page]['widgets'].splice(old_index, 1);" +
                            "$('#" + widget['id'] + "').remove();" +
                        "});"
                     "</script>";

        BootstrapDialog.alert({
            title: text,
            message: message + script
        });
    }

    /*****************************************************************************************************************
                                                        SIDEBAR
    ******************************************************************************************************************/

    var double_click_time = 0; // The time in ms to check whether the user clicks or doubleclicks the dashboard name item
    var threshold = 200; // The time in ms within the doubleclick to the dashboard name item is recognized

    /*
        Attaches the click and doubleclick listeners to the dashboard name item
    */
    function addEventsExistingDashboardItem() {
        $('.dashboard-page').click(function(){
            var element = this;
            var t0 = new Date();
            if (t0 - double_click_time > threshold) {
                setTimeout(function () {
                    if (t0 - double_click_time > threshold) {
                        doDashboardPageOnClick(element);
                    }
                },threshold);
            }
        });

        $('.dashboard-page').dblclick(function(e){
            onDashboardPageDoubleClick(this);
        });
    }

    /*
        Attaches the click listener to the new dashboard item
    */
    function addEventsNewDashboardItem() {
        $('.add').click(function(event){
            var id = Object.keys(dashboards).length + 1;
            $('<li id="page-' + id + '" class="dashboard-page"> New Dashboard Page </li>').insertBefore(this);
            dashboards['page-'+id] = {};
            dashboards['page-'+id]['name'] = 'New Dashboard Page';
            dashboards['page-'+id]['widgets'] = [];
            addEventsExistingDashboardItem();
            $.notify('You have inserted a dashboard page.', "success");
        });
    }

    /*
        Change the foreground dashboard which will be diplayed
        @element The clicked dashboard name item
    */
    function doDashboardPageOnClick(element) {
        if (!$('.input-dashboard-page').length) {
            dashboards[page]['widgets'].forEach(function(widget, windex){
                clearInterval(dashboards[page]['widgets'][windex]["refreshIntervalId"]);
            });
            $('.dashboard-page').removeClass('active');
            $(element).addClass('active');
            $(".page-content-wrap").empty();
            page = $(element).attr('id');
            if (page == 'page-0') {
                dashboards[page] = {
                    "name": "Create New Widget",
                    "widgets": [
                        {
                            "id": "widget-6656",
                            "title": "New widget",
                            "authors": ["carmen"],
                            "modified": "2018-01-12T00:00:00Z",
                            "sources": [],
                            "timeinterval": null,
                            "map": null,
                            "highmarkericon": [],
                            "refreshIntervalId": null,
                            "highmarker": [],
                            "data": []
                        }
                    ]
                }
            }
            $('#bread-item').html(dashboards[page]['name'] + '<span id="popup-dashboard" class="fa fa-link popup-dashboard"></span>');
            addEventsShareDashboard();
            displayWidgets(dashboards[$(element).attr('id')]['widgets']);
        }
    }

    /*
        Creates a text area in order to change the dashboard name
        @element The clicked dashboard name item
    */
    function onDashboardPageDoubleClick(element) {
        double_click_time = new Date();
        old = $(element).text().trim();
        $(element).html('<input class="input-dashboard-page" type="text" name="search" value="' + old + '"/>');
        $('.input-dashboard-page').keypress(function (e) {
           var key = e.which;
           var id = $(this).parent().attr('id');
           if(key == 13) {
                if($(this).val() == '') {
                    $(this).parent().remove();
                    delete dashboards[id];
                    $.notify('You have removed the dashboard page.', "success");
                    if(id == page) {
                        page = 'page-' + (Object.keys(dashboards).length - 1);
                        loadDashboard();
                    }
                }
                else {
                    $(this).parent().html($(this).val());
                    $.notify('You have changed the dashboard name.', "success");
                    dashboards[id]['name'] = $(this).val();
                    $('#bread-item').html(dashboards[page]['name'] + '<span id="popup-dashboard" class="fa fa-link popup-dashboard"></span>');
                }
           }
        });
    }

    addEventsExistingDashboardItem();
    addEventsNewDashboardItem();

    /*****************************************************************************************************************
                                                        UTILS
    ******************************************************************************************************************/

    /*
        Checks whether at least one source inside the widget needs to be displayed along time
        @sources The list of sources inside a widget
        @return Returns "dynamic" if at least one source needs to be displayed along time, otherwise "static"
    */
    function getType(sources) {
        var value = 'static';
        sources.forEach(function(source, index){
            if(source['granularity'] != 'cumulative') {
                value = 'dynamic';
            }
        });
        return value;
    }

    /*
        Creates a circle icon
        @id The id to assign to the icon
        @obsval The intensity value to assign to the icon
        @dataset The dataset from which getting the intensity color palette
        @return A circle icon colored on the basis of its intensity value
    */
    function getCircleIcon(id, obsval, dataset) {
        return L.vectorIcon({
                  className: 'circle-icon-' + id,
                  svgHeight: 12,
                  svgWidth: 12,
                  type: 'circle',
                  shape: {
                    r: '5',
                    cx: '6',
                    cy: '6'
                  },
                  style: {
                    fill: getIconColor(dataset, obsval),
                    stroke: '#000',
                    strokeWidth: 1
                  }
        });
    }

    /*
        Creates a rectangle icon
        @id The id to assign to the icon
        @widget The widget where the icon will be displayed
        @return A rectangle icon colored on the basis of the number of rectangle icons currently displayed
    */
    function getRectangleIcon(id, widget) {
        return L.vectorIcon({
                  className: 'circle-icon-' + id,
                  svgHeight: 16,
                  svgWidth: 16,
                  type: 'rect',
                  shape: {
                    x: '1',
                    y: '1',
                    width: '14',
                    height: '14'
                  },
                  style: {
                    fill: color_palette[widget['data'].length],
                    stroke: '#000',
                    strokeWidth: 1
                  }
                })
    }

    /*
        Returns an intensity color
        @dataset The dataset from which getting the intensity color palette
        @value The intensity value to assign to the color
        @return A color on the basis of the intensity value
    */
    function getIconColor(dataset, value) {
        var colors = dataset['colors'];
        var cuts = dataset['cuts'];
        var color = '#217C7E';

        cuts.forEach(function (cut, i) {
            if(cut < value) {
                color = colors[i];
            }
        });

        return color;
    }

    /*
        Returns an intensity color
        @feature The current geographical feature
        @dataset The dataset from which getting the intensity color palette
        @obs The set of observation to be displayed
        @return A style of a geographical area on the basis of the intensity value
    */
    function getAreaColor(feature, dataset, obs) {
        var bordercolor = 'rgba(0,0,0,0)';
        var fillcolor = 'rgba(0,0,0,0)';
        obs.forEach(function(element) {
            if(titleCase(feature.properties.neighbourhood) == titleCase(element.id)) {
                fillcolor = getIconColor(dataset, element.value);
                bordercolor = '#000';
            }
        });

        return {
          color: bordercolor,
          weight: 1,
          opacity: 1,
          fillColor: fillcolor,
          fillOpacity: 0.8
        }
    }

    function getPolygonColor(feature, dataset) {
        var bordercolor = 'rgba(0,0,0,0)';
        var fillcolor = getIconColor(dataset, feature.properties.value);

        return {
          color: bordercolor,
          weight: 1,
          opacity: 1,
          fillColor: fillcolor,
          fillOpacity: 0.8
        }
    }

    /*
        Transforms a text to camel case
        @str The string to be modified
        @return The string in camel case format
    */
    function titleCase(str) {
       var splitStr = str.toLowerCase().split(' ');
       for (var i = 0; i < splitStr.length; i++) {
           splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);
       }

       str = splitStr.join(' ');
       var splitStr = str.split('\'');
       for (var i = 0; i < splitStr.length; i++) {
           splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);
       }

       return splitStr.join('\'');
    }

    /*
        Returns an intensity color
        @feature The current geographical feature
        @dataset The dataset from which getting the intensity color palette
        @obs The set of observation to be displayed
        @return The observation associated to the current geographical feature
    */
    function getLabel(feature, dataset, obs) {
        var result = null;
        obs.forEach(function(element) {
            if(titleCase(feature.properties.neighbourhood) == titleCase(element.id)) {
                result = element;
            }
        });
        return result;
    }

    /*****************************************************************************************************************
                                                        WIDGETS
    ******************************************************************************************************************/

    /*
        Arranges the original retrieved data to be displayed
        @aggregation The geographical laggregation level for the current source
        @data The original data
        @return The arranged data
    */
    function getPreparedData(aggregation, data, windex, sindex) {
        if(aggregation != 'none') {
            filtered = {"records": [], "count": 0}
            data.records.forEach(function(record) {
                var filtered_records = {"_id": record._id, "doc": []};
                record.doc.forEach(function(element) {
                    var r = {};
                    var lat = 0.0;
                    var long = 0.0;
                    var num = 0
                    element.doc.forEach(function(h) {
                        if(h["point"][1] > 1) {
                            num += 1;
                        }
                        lat += h["point"][1];
                        long += h["point"][0];
                    });
                    if(num > 0) {
                        r["id"] = element["_id"][dashboards[page]['widgets'][windex]['sources'][sindex]['aggregation']];
                        r["point"] = [long / num, lat / num];
                        r["value"] = element["avg"];
                        r["count"] = element["count"];
                        r["avg"] = element["avg"];
                        r["sum"] = element["sum"];
                        filtered_records.doc.push(r);
                    }
                });
                if(filtered_records.doc.length > 0) {
                    filtered.records.push(filtered_records);
                }
            });
            filtered.count = filtered.records.length;
            data.records = filtered.records;
            data.count = filtered.count;
        }
        else {
            filtered = {"records": [], "count": 0}
            data.records.forEach(function(record) {
                var filtered_records = {"_id": record._id.timestamp, "doc": []};
                record.doc.forEach(function(element) {
                    if(element.point[0] > 1) {
                        filtered_records.doc.push(element);
                    }
                });
                if(filtered_records.doc.length > 0) {
                    filtered.records.push(filtered_records);
                }
            });
            filtered.count = filtered.records.length;
            data.records = filtered.records;
            data.count = filtered.count;
        }
        return data;
    }

    /*
        Shows the legend for the current source in the widget
        @widget The widget where the legend will be inserted
        @dataset The source dataset to which build the legend
    */
    function addLegend(widget, dataset) {
        if(dataset['colors'].length > 1) {
            var legend = L.control({position: 'bottomright'});
            legend.onAdd = function (map) {
                var div = L.DomUtil.create('div', 'info legend');
                var faultstatus = dataset['cuts'];
                div.innerHTML += '<strong> ' + dataset['labels'] + ' </strong> <br>';
                for (var i = faultstatus.length-1; i >= 0; i--) {
                    div.innerHTML += '<i class="circle" style="background:' + dataset['colors'][i] + '"></i> ' + (faultstatus[i+1] ? '' : '&ge; ') + (faultstatus[i]+(i == 0 ? 1 : 0)) + (faultstatus[i+1] ? ' - ' + (faultstatus[i+1]) : '') + '<br>';
                }
                return div;
            };
            legend.addTo(widget['map']);
        }
    }

    /*
        Adds a time slider for the current source in the widget
        @widget The widget where the slider will be inserted
        @windex The widget index in the current page
        @sindex The source index in the current widget
    */
    function addSlider(widget, windex, sindex) {
        $('#' + widget['id'] + '-slider').slider({
            range: "min",
            min: 1,
            max: widget['sources'][sindex]['dataset'].count,
            step: 1,
            slide: function(event, ui) {
                updateMap(windex, sindex);
            }
        });
        $("#" + widget['id'] + "-slider").slider('value', 0);
        $("#" + widget['id'] + "-slider-button").show();
    }

    /*
        Initializes a map for the current source within the widget
        @windex The widget index in the current page
        @sindex The source index in the current widget
    */
    function initMap(windex, sindex) {
        var map_current_coords = [41.390205, 2.154007];
        var map_current_zoom = 13;
        var map_max_zoom = 18;
        var widget = dashboards[page]['widgets'][windex];
        var dataset = datasets[widget['sources'][sindex]['id']];

        try {
            map = L.map(widget['id'] + '-map').setView(map_current_coords, map_current_zoom);
            L.tileLayer.grayscale('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: map_max_zoom,
                id: 'mapbox.streets',
                accessToken: 'pk.eyJ1IjoibW1hcnJhcyIsImEiOiJjamE3MnBpd2E3MjZ1MndwNzY5YjBrdDgxIn0.zO2nGOwmSGhb8YrzhWNdeQ'
            }).addTo(map);
            widget['map'] = map;
        }
        catch(error) {
            map = widget['map'];
        }

        loadMap(widget, dataset, windex, sindex);
    }

    /*
        Loads the data for the current source in the widget
        @widget The widget where the data will be loaded
        @dataset The source dataset to insert
        @windex The widget index in the current page
        @sindex The source index in the current widget
    */
    function loadMap(widget, dataset, windex, sindex) {
        var filters = (widget['sources'][sindex]['keyword'] != '') ? '$' + dataset['filter_field'] + '=[' + widget['sources'][sindex]['keyword'] + ']' : '';
        var parameters = 'fields=' + dataset['parameters'] + 'id@id,value@payload.' + dataset['targetvalue'] + ',point@location.point.coordinates' + '&';
        var aggregation = (widget['sources'][sindex]['aggregation'] != 'none') ? 'group=' + widget['sources'][sindex]['aggregation'] + '@' + 'location.' + widget['sources'][sindex]['aggregation'] + ',timestamp@timestamp' + '&' : 'group=timestamp@timestamp' + '&';
        var operators = (widget['sources'][sindex]['aggregation'] != 'none') ? 'aggregators=avg@payload.' + dataset['targetvalue'] + '&' : '';
        var sort = 'sort=a@timestamp' + '&';
        var is_observation = 'isObservation' + '&';
        var conditions = '$timestamp=gte@' + widget['sources'][sindex]['start'] + ',lt@' + widget['sources'][sindex]['end'] + '&';
        $('#' + widget['id'] + '-loader').show();
        console.log(url_api + dataset['name'] + '?' + operators  + aggregation + parameters + sort + is_observation + conditions + filters)
        $.ajax({
            url: url_api + dataset['name'] + '?' + operators  + aggregation + parameters + sort + is_observation + conditions + filters,
            success: function(data) {
                widget['sources'][sindex]['dataset'] = getPreparedData(widget['sources'][sindex]['aggregation'], data, windex, sindex);
                addSlider(widget, windex, sindex);
                addLegend(widget, dataset);
                updateMap(windex, sindex, 0);
                $("#" + widget['id'] + "-loader").hide();
            },
            error: function() {
            }
        });
    }

    /*
        Appends a record to the data array based on the visual model to be displayed
        @widget The widget where the data will be loaded
        @windex The widget index in the current page
        @sindex The source index in the current widget
        @dataset The source dataset to insert
        @data The current data array
        @element The element to be added in the data array
        @icon The icon associated to the new element
        @data The id associated to the new element
        @return The new data array
    */
    function pushData(widget, windex, sindex, dataset, data, element, icon, id) {
        var value = (widget['sources'][sindex]['aggregation'] == 'none') ? (typeof dataset['targetvalue'] === "string"? element[dataset['targetvalue']] : dataset['targetvalue']) : element[dataset['aggregator']];
        if(widget['sources'][sindex]['chart'] == 'heat-map'){
            data.push({lat: element["point"][1], lng: element["point"][0], value: value});
        }
        else if(widget['sources'][sindex]['chart'] == 'map-polygons'){
            data.push({ "type": "Feature", "properties": {"value": element['value']}, "geometry": element["polygon"] });
        }
        else if(widget['sources'][sindex]['chart'] == 'map-lines'){
            data.push(element["line"]);
        }
        else {
            data.push(getMarker(widget, windex, sindex, dataset, element, icon, id, value));
        }
        return data;
    }

    /*
        Creates the panel to be shown when a map marker is clicked
        @dataset The source dataset to insert
        @widget The widget where the data will be loaded
        @windex The widget index in the current page
        @sindex The source index in the current widget
        @markerid The wid of the panel
        @output The detailed records for the current data source items
    */
    function getMarkerPanel(dataset, widget, windex, sindex, markerid, output) {
        if(dataset['name'] == 'asia') {
            $("#" + windex + "-time-series-title").text("ASIA ID " + markerid);
            $.each(output.records, function(index, element) {
                if(widget['sources'][sindex]['aggregation'] == 'none') {
                     var categories = '';
                     for(var k in element.doc[0].categories) categories += element.doc[0].categories[k] + '; ';
                     $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Name:</span> ' + element.doc[0].name + '</div>');
                     $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Start Date:</span> ' + moment(element.doc[0].startdate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                     $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">End Date:</span> ' + moment(element.doc[0].enddate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                     $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Categories:</span> ' + categories + '</div>');
                }
                else {
                    $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Number of events:</span> ' + element.doc[0].count + '</div>');
                }
            });
        }

        if(dataset['name'] == 'pointsinterest') {
            $("#" + windex + "-time-series-title").text("POINT OF INTEREST ID " + markerid);
            $.each(output.records, function(index, element) {
                if(widget['sources'][sindex]['aggregation'] == 'none') {
                     $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Name:</span> ' + element.doc[0].name + '</div>');
                     $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Type:</span> ' + element.doc[0].type + '</div>');
                     $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Short Description:</span> ' + element.doc[0].shortdescription + '</div>');
                }
                else {
                    $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Number of PoIs:</span> ' + element.doc[0].count + '</div>');
                }
            });
        }

        if(dataset['name'] == 'pam_meeting') {
            $("#" + windex + "-time-series-title").text("MEETING ID " + markerid);
            $.each(output.records, function(index, element) {
                if(widget['sources'][sindex]['aggregation'] == 'none') {
                         $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Title:</span> ' + element.doc[0].title + '</div>');
                         $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Address:</span> ' + element.doc[0].address + '</div>');
                     $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Start Date:</span> ' + moment(element.doc[0].startTime).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                     $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">End Date:</span> ' + moment(element.doc[0].endTime).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                         $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Attendees:</span> ' + element.doc[0].attendeeCount + '</div>');                     
                         $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name">');
			 for (i = 0; i < element.doc[0].attachments.length; i++) { 
			     $("#" + widget['id'] + "-dashboard-line").append('<img vspace="1" hspace="1" width="150" src="' + element.doc[0].attachments[i] + '"/>');
                         }
                         $("#" + widget['id'] + "-dashboard-line").append('</div">');
                }
                else {
                }
            });
        }

        if(dataset['name'] == 'iris') {
            $("#" + windex + "-time-series-title").text("IRIS ID " + markerid);
            $.each(output.records, function(index, element) {
                if(dashboards[page]['widgets'][windex]['sources'][sindex]['aggregation'] == 'none') {
                         $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Type:</span> ' + element.doc[0].type + '</div>');
                         $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Area:</span> ' + element.doc[0].area + '</div>');
                         $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Element:</span> ' + element.doc[0].element + '</div>');
                         $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Detail:</span> ' + element.doc[0].detail + '</div>');
                         $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Support:</span> ' + element.doc[0].support + '</div>');
                         $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Channel:</span> ' + element.doc[0].channel + '</div>');
                         $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Opening Date:</span> ' + moment(element.doc[0].startdate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                         $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Closing Date:</span> ' + moment(element.doc[0].enddate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                }
                else {
                    $("#" + widget['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Number of iris:</span> ' + element.doc[0].count + '</div>');
                }
            });
        }

        if(dataset['name'] == 'smartcitizen' || dataset['name'] == 'bicing') {
            var flag = false;
            widget['data'].forEach(function(record, index){
                if(record['name'] == 'Sensor ' + markerid)
                    flag = true;
            });

            var sensordata = [];
            var x = [];
            var y = [];
            $.each(output.records, function(index, element) {
                var timestamp;
                if(widget['sources'][sindex]['aggregation'] != 'none') {timestamp = element["_id"]}
                else {timestamp = element["_id"]["timestamp"]}
                x.push(timestamp);
                y.push(Math.floor(element["doc"][0]["value"]));
            });

            var d3 = Plotly.d3;

            var WIDTH_IN_PERCENT_OF_PARENT = 100,
                HEIGHT_IN_PERCENT_OF_PARENT = 100;

            var gd3 = d3.select('#' + widget['id'] + '-dashboard-line')
                .append('div')
                .style({
                    width: WIDTH_IN_PERCENT_OF_PARENT + '%',
                    'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%'
                });

            var gd = gd3.node();

            if(flag == false) {
                widget['data'].push({name: 'Sensor ' + markerid, x: x, y: y, type: 'scatter', line: {color: color_palette[widget['data'].length], width: 1}});
            }

            Plotly.newPlot(gd, widget['data'], {
                  autosize: true,
                  height: 300,
                  margin: {
                    l: 35,
                    r: 50,
                    b: 35,
                    t: 15,
                    pad: 4
                  },
                  showlegend: true,
                  legend: {
                    x: 1,
                    y: 1
                  }
            });

            window.onresize = function() {
                Plotly.Plots.resize(gd);
            };

        }
        return;
    }

    /*
        Creates a marker to be shown on the current widget
        @widget The widget where the data will be loaded
        @windex The widget index in the current page
        @sindex The source index in the current widget
        @dataset The source dataset to insert
        @element The element to be added in the data array
        @icon The icon associated to the new element
        @id The id associated to the marker
        @obsval The intensity value associated to the marker
        @return A Leaflet marker
    */
    function getMarker(widget, windex, sindex, dataset, element, icon, id, obsval) {
        var marker = L.marker([element["point"][1], element["point"][0]], {icon: icon, title: 'Sensor ' + id.split('.')[0] + ': ' + dataset['labels'] + ' ' + obsval, markerid: id.split('.')[0]});

        marker.on('click', function(e){
            $("#" + widget['id']).css("width", "100%");
            var markerid = e.target.options.markerid;
            $("#" + windex + "-slider-date").removeClass('col-md-12').addClass('col-md-6');
            $("#" + windex + "-slider-date-graph").show();
            $("#" + windex + "-graph-loader").show();
            
            widget["highmarker"].push(e.target);
            widget["highmarkericon"].push(e.target.options.icon);

            $('.' + 'circle-icon-' + windex + '-' + sindex + '-' + markerid).empty();
            e.target.setIcon(getRectangleIcon(windex + '-' + sindex + '-' + markerid, widget));
            $('.' + 'circle-icon-' + windex + '-' + sindex + '-' + markerid).empty();
            e.target.setIcon(getRectangleIcon(windex + '-' + sindex + '-' + markerid, widget));

            var attr_id = (dataset['name'] == 'asia') ? "id": "payload.id";
            var val = $("#" + widget['id'] + "-slider").slider("option", "value");
            var aggregation = (widget['sources'][sindex]['aggregation'] != 'none') ? "group=" + widget['sources'][sindex]['aggregation'] + '@' + 'location.' + widget['sources'][sindex]['aggregation'] + ',' + "timestamp@timestamp" + '&' : "group=timestamp@timestamp" + '&';
            var operators = (widget['sources'][sindex]['aggregation'] != 'none') ? 'aggregators=avg@payload.' + dataset['targetvalue'] + '&' : '';
            var geo = (widget['sources'][sindex]['aggregation'] != 'none') ? "&$location." + widget['sources'][sindex]['aggregation'] + "=" + markerid : "&$" + attr_id + "=" + markerid;
            var agg = (widget['sources'][sindex]['aggregation'] != 'none') ? "avg" : 'value';
            var filters = (widget['sources'][sindex]['keyword'] != '') ? "$" + dataset['filter_field'] + "=[" + query + "]" : '';
            var parameters = "fields=" + dataset['details'] + "id@id,value@payload." + datasets[widget['sources'][sindex]['id']]['targetvalue'] + ",point@location.point.coordinates" + "&";
            var current = (widget['sources'][sindex]['aggregation'] != 'none' && (dataset['name'] == 'asia' || dataset['name'] == 'iris' || dataset['name'] == 'pointsinterest')) ? "&$timestamp=gte@" + moment(widget['sources'][sindex]['dataset'].records[(val-1)%(max)]["_id"].replace(' ', 'T') + 'Z').set({hour:0,minute:0,second:0,millisecond:0}).toISOString() + ",lt@" + moment(widget['sources'][sindex]['dataset'].records[(val-1)%(max)]["_id"].replace(' ', 'T') + 'Z').add(1, "days").set({hour:0,minute:0,second:0,millisecond:0}).toISOString() : "&$timestamp=gte@" + widget['sources'][sindex]['start'] + ",lt@" + widget['sources'][sindex]['end'] ;
            var sort = "sort=a@timestamp" + "&";
            var is_observation = "isObservation" + "&";
            console.log(url_api + dataset['name'] + '?' + operators + aggregation + parameters + sort + is_observation + geo + current + filters);
            $.ajax({
                url: url_api + dataset['name'] + '?' + operators + aggregation + parameters + sort + is_observation + geo + current + filters,
                success: function(output) {
                    try {
                        $("#" + widget['id'] + "-dashboard-line").empty();
                        getMarkerPanel(dataset, widget, windex, sindex, markerid, output);
                        $("#" + windex + "-graph-loader").hide();
                    }
                    catch(err) {
                    }
                },
                error: function() {
                }
            });
        });

        return marker;
    }

    /*
        Draws a visual model on the current widget
        @dataset The source dataset to insert
        @widget The widget where the data will be loaded
        @windex The widget index in the current page
        @sindex The source index in the current widget
        @data The data to be shown on the visual model
    */
    function drawLayer(dataset, widget, windex, sindex, data) {
        var layer;
        widget['sources'][sindex]['markers'] = new L.LayerGroup();
        widget['sources'][sindex]['markers'].clearLayers();
        if(widget['sources'][sindex]['chart'] == 'heat-map') {
            layer = new HeatmapOverlay({'radius': dataset['radius'], 'maxOpacity': .5, 'useLocalExtrema': true });
            layer.setData({max: 8, data: data});
            widget['sources'][sindex]['markers'].addLayer(layer);
        }
        else if(widget['sources'][sindex]['chart'] == 'map-lines') {
            layer = L.geoJSON(data, {
                style: {'color': '#003366', 'weight': 2, 'opacity': 0.65}
            });
            widget['sources'][sindex]['markers'].addLayer(layer);
        }
        else if(widget['sources'][sindex]['chart'] == 'map-polygons') {
            layer = L.geoJson(data, {
              style: function(feature) {
                return getPolygonColor(feature, dataset);
              },
              onEachFeature: function(feature, layer) {
                layer.bindTooltip(dataset['labels'] + ': ' + feature.properties.value);
              }
            });
            widget['sources'][sindex]['markers'].addLayer(layer);
        }
        else {
            data.forEach(function(record, index){
                widget['sources'][sindex]['markers'].addLayer(record);
            });
        }
        widget['map'].addLayer(widget['sources'][sindex]['markers']);
    }

    /*
        Draws polygon areas on the current widget
        @widget The widget where the data will be loaded
        @windex The widget index in the current page
        @sindex The source index in the current widget
        @dataset The source dataset to insert
        @obs The observation associated to all the geographical areas
    */

    function drawBoundaries(widget, windex, sindex, dataset, obs, output) {
        $.ajax({
            dataType: 'json',
            url: 'assets/geojson/' + widget['sources'][sindex]['aggregation'] + '.geojson',
            success: function(data) {
                geo_boundary = new L.geoJson(data, {
                      style: function(feature) {
                        return getAreaColor(feature, dataset, obs);
                      },
                      onEachFeature: function(feature, layer) {
                          var element = getLabel(feature, dataset, obs);
                          if(element) {
                              layer.bindTooltip(feature.properties.neighbourhood + ' ' + dataset['labels'] + ': ' + element.value);
                          }
                          layer.on('click', function (e) {
                            $("#" + widget['id'] + "-dashboard-line").empty();
                            $("#" + widget['id']).css("width", "100%");
                            $("#" + windex + "-slider-date").removeClass('col-md-12').addClass('col-md-6');
                            $("#" + windex + "-slider-date-graph").show();
                            $("#" + windex + "-graph-loader").show();
                            var flag = false;
                            widget['data'].forEach(function(record, index){
                                if(record['name'] == feature.properties.neighbourhood)
                                    flag = true;
                            });
                            var x = [];
                            var y = [];
                            $.each(output.records, function(index, element) {
                                var timestamp = element["_id"];
                                x.push(timestamp);
                                $.each(element.doc, function(cod_d, obs_d) {
                                    if(obs_d['id'] == feature.properties.neighbourhood)
                                        y.push(obs_d['value']);
                                });
                            });

                            var d3 = Plotly.d3;

                            var WIDTH_IN_PERCENT_OF_PARENT = 100,
                                HEIGHT_IN_PERCENT_OF_PARENT = 100;

                            var gd3 = d3.select('#' + widget['id'] + '-dashboard-line')
                                .append('div')
                                .style({
                                    width: WIDTH_IN_PERCENT_OF_PARENT + '%',
                                    'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%'
                                });

                            var gd = gd3.node();

                            if(flag == false)
                                widget['data'].push({name: feature.properties.neighbourhood, x: x, y: y, type: 'scatter', line: {color: color_palette[widget['data'].length+1], width: 1}});

                            Plotly.newPlot(gd, widget['data'], {
                                  autosize: true,
                                  height: 300,
                                  margin: {
                                    l: 35,
                                    r: 50,
                                    b: 35,
                                    t: 15,
                                    pad: 4
                                  },
                                  showlegend: true,
                                  legend: {
                                    x: 1,
                                    y: 1
                                  }
                            });

                            window.onresize = function() {
                                Plotly.Plots.resize(gd);
                            };
                            var centroid = turf.centroid(feature);
                            var lon = centroid.geometry.coordinates[0];
                            var lat = centroid.geometry.coordinates[1];
                            marker = L.marker([lat, lon], {icon: getRectangleIcon(windex + '-' + sindex + '-' + feature.properties.neighbourhood, widget)}).addTo(widget['map']);
                            widget["highmarker"].push(marker);
                            widget["highmarkericon"].push(marker.icon);
                            $("#" + windex + "-graph-loader").hide();
                          });
                      }
                });
                widget['sources'][sindex]['markers'] = new L.LayerGroup();
                widget['sources'][sindex]['markers'].clearLayers();
                widget['sources'][sindex]['markers'].addLayer(geo_boundary);
                widget['map'].addLayer(widget['sources'][sindex]['markers']);
            },
            error: function() {

            }
        });
    }

    /*
        Updates the current widget
        @windex The widget index in the current page
        @sindex The source index in the current widget
    */
    function updateMap(windex, sindex, dir=1) {
        var widget = dashboards[page]['widgets'][windex];
        var dataset = datasets[widget['sources'][sindex]['id']];
        var val = $("#" + widget['id'] + "-slider").slider("option", "value") + dir;
        var max = $("#" + widget['id'] + "-slider").slider("option", "max");

        $("#" + widget['id'] + "-slider").slider("value",(val)%(max+1));
        if (widget['sources'][sindex]['dataset'].records.length > 0) {
            $("#" + widget['id'] + "-slider-value").html("<span  class='tip'>" + moment(widget['sources'][sindex]['dataset'].records[(val-1)%(max)]["_id"]).format('dddd, MMMM Do YYYY, h:mm:ss a') + "</span>");
        }
        
        obs = [];
        if(widget['sources'][sindex]['granularity'] != "cumulative" && widget['sources'][sindex]['dataset'].records.length > 0) {
            obs = dashboards[page]['widgets'][windex]['sources'][sindex]['dataset'].records[(val-1)%(max)]["doc"];
        }
        else {
            widget['sources'][sindex]['dataset'].records.forEach(function(record, index){
                obs = obs.concat(record["doc"]);
            });
        }

        if(widget['sources'][sindex]['aggregation'] != 'none') {
            all = dashboards[page]['widgets'][windex]['sources'][sindex]['dataset'];
            drawBoundaries(widget, windex, sindex, dataset, obs, all);
        }
        else {
            var data = [];
            obs.forEach(function(element) {
                id = element['id'];
                value = parseInt(element['value']);
                icon = getCircleIcon(id, value, dataset);
                data = pushData(widget, windex, sindex, dataset, data, element, icon, id);
            });
            drawLayer(dataset, widget, windex, sindex, data);
        }
    }

    /*
        Draws the HTML widget
        @widget The widget where the data will be loaded
        @windex The widget index in the current page
    */
    function drawWidget(widget, windex) {
        authors = '';
        widget['authors'].forEach(function(author, sindex){
            authors += '<span class="high-name">' + author  + '</span>';
        });

        sources = '';
        widget['sources'].forEach(function(source, sindex){
            sources +=         '<div  id="' + windex + '-' + sindex + '-source-item" class="row source-item">' +
                                '<div class="high-name"><strong>' + datasets[source['id']]['description'] + '</strong></div> ' +
                                '<div class="high-name"> from <strong>' + moment(source['start']).format('MMMM Do YYYY') + '</strong></div>' +
                                '<div class="high-name"> to <strong>' + moment(source['end']).format('MMMM Do YYYY') + '</strong></div> ' +
                                (source['keyword'] != '' ? '<div class="high-name"> by keyword <strong>' +  source['keyword'] + '</strong></div> ' : '') +
                                (source['aggregation'] != 'none' ? '<div class="high-name"> by <strong>' +  source['aggregation'] + '</strong></div> ' : '') +
                                '<div class="high-name"> [' +
                                     '<span data-toggle="modal"  id="' + windex + '-' + sindex + '-modify" data-target="#' + widget['id'] + '-' + datasets[source['id']]['name'] + '-modal" class="modify">Edit</span>' +
                                     '<span id="widget-' + windex + '-source-' + sindex + '-remove" class="remove">Remove</span>]' +
                                '</div> ' +
                            '</div>';
            sources +=      '<div id="' + widget['id'] + '-' + datasets[source['id']]['name'] + '-modal" class="modal fade" role="dialog">' +
                            '<div class="modal-dialog">' +
                                '<div class="modal-content">' +
                                  '<div class="modal-header">' +
                                    '<button type="button" class="close" data-dismiss="modal">&times;</button>' +
                                    '<h4 class="modal-title">Edit "' + datasets[source['id']]['provider'] + '" data source</h4>' +
                                  '</div>' +
                                      '<div class="modal-body">' +
                                          '<div class="form-group">' +
                                          '<label for="dataset">Select dataset:</label>' +
                                          '<select class="form-control" id="' + windex + '-' + sindex + '-edit-dataset">';
            jQuery.each(datasets, function(sindex, dataset){
                  sources +=                   '<option value="' + sindex + '" >' + dataset['description'] + '</option>';
            });
            sources +=                       '</select>' +
                                          '<div id="' + windex + '-' + sindex + '-edit-info"></div><br/>' +
                                          '<label for="time_interval">Select time interval:</label><br/>' +
                                          '<div id="' + windex + '-' + sindex + '-edit-time-interval" class="dtrange">' +
                                                '<span></span><b class="caret"></b>' +
                                          '</div><br/><br/><br/>' +
                                          '<label for="type">Select time granularity:</label>' +
                                          '<select class="form-control" id="' + windex + '-' + sindex + '-edit-granularity">' +
                                            '<option value="cumulative">Cumulative</option>' +
                                            '<option value="dynamic">Dynamic</option>' +
                                          '</select><br/>' +
                                          '<label for="type">Select visualization type:</label>' +
                                          '<select class="form-control" id="' + windex + '-' + sindex + '-edit-type">';
            jQuery.each(datasets[source['id']]['allowed_visual_models'], function(vindex, model){
                  sources +=                '<option value="' + model + '" ' + (source['chart'] == model?'selected':'') + '>' + model + '</option>';
            });
            sources +=                    '</select><br/><br/>' +
                                          '<label for="aggregation"> Select geographical aggregation:</label>' +
                                          '<select class="form-control" id="' + windex + '-' + sindex + '-edit-aggregation">' +
                                            '<option value="none" ' + (source['aggregation'] == 'none'?'selected':'') + '>None</option>' +
                                            '<option value="neighbourhood" ' + (source['aggregation'] == 'neighbourhood'?'selected':'') + '>Neighbourhood</option>' +
                                            '<option value="district" ' + (source['aggregation'] == 'district'?'selected':'') + '>District</option>' +
                                          '</select><br/><br/>' +
                                          '<label for="keyword">Filter by keyword:</label><br/>' +
                                          '<input class="edit-keyword" type="text" id="' + windex + '-' + sindex + '-edit-keyword" value="' + source['keyword'] + '">' +
                                          '</div>' +
                                      '</div>' +
                                  '<div class="modal-footer">' +
                                    '<button id="' + windex + '-' + sindex + '-edit-close" type="button" class="edit-close btn btn-default" data-dismiss="modal">Edit</button>' +
                                    '<button class="btn btn-default" data-dismiss="modal">Close</button>' +
                                        '</div>' +
                                '</div>' +
                              '</div>' +
                            '</div>';
        });

        options = ''
        jQuery.each(datasets, function(sindex, dataset){
              options +=                           '<option value="' + sindex + '">' + dataset['description'] + '</option>';
        });


        html =  '<!-- START SENTILO BLOCK -->' +
                '<div class="panel panel-default" id="' + widget['id'] + '">' +
                    '<div class="panel-heading">' +
                        '<div class="panel-title-box">' +
                            '<h3 id="' + widget['id'] + '-title" class="widget-title">' + widget['title'] + '</h3>' +
                            '<span class="creator-authors"> created by ' +
                                authors +
                                ' and modified at <span id="' + windex + '-modified" class="high-name">' + widget['modified'] + '</span>' +
                            '</span>' +
                            '<span id="' + widget['id'] + '-source-list" class="' + widget['id'] + '-source-list">' +
                                sources +
                            '</span>' +
                        '</div>' +
                        '<ul class="panel-controls panel-controls-title">' +
                           '<li class="rounded">' +
                               '<span id="' + windex + '-add-source" class="add-source fa fa-plus" title="Add a source"></span>' +
                               '<div id="' + windex + '-modal" class="modal fade" role="dialog">' +
                                    '<div class="modal-dialog">' +
                                        '<div class="modal-content">' +
                                          '<div class="modal-header">' +
                                            '<button type="button" class="close" data-dismiss="modal">&times;</button>' +
                                            '<h4 class="modal-title">Insert new data source</h4>' +
                                          '</div>' +
                                              '<div class="modal-body">' +
                                                  '<div class="form-group">' +
                                                      '<label for="dataset">Select dataset:</label>' +
                                                      '<select class="form-control" id="' + windex + '-plus-dataset">' +
                                                        '<option value="none">None</option>' +
                                                        options +
                                                      '</select>' +
                                                      '<div id="' + windex + '-plus-info"></div><br/>' +
                                                      '<label for="time_interval">Select time interval:</label><br/>' +
                                                      '<div id="' + windex + '-plus-time-interval" class="dtrange">' +
                                                        '<span></span><b class="caret"></b>' +
                                                      '</div><br/><br/><br/>' +
                                                      '<label for="type">Select time granularity:</label>' +
                                                      '<select class="form-control" id="' + windex + '-plus-granularity">' +
                                                        '<option value="cumulative">Cumulative</option>' +
                                                        '<option value="dynamic">Dynamic</option>' +
                                                      '</select><br/>' +
                                                      '<label for="type">Select visualization type:</label>' +
                                                      '<select class="form-control" id="' + windex + '-plus-type">' +
                                                        '<option value="points-map">points-map</option>' +
                                                        '<option value="heat-map">heat-map</option>' +
                                                      '</select><br/>' +
                                                      '<label for="aggregation">Select geographical aggregation:</label>' +
                                                      '<select class="form-control" id="' + windex + '-plus-aggregation">' +
                                                        '<option value="none">None</option>' +
                                                        '<option value="neighbourhood">Neighbourhood</option>' +
                                                        '<option value="district">District</option>' +
                                                      '</select><br/>' +
                                                      '<label for="keyword">Filter by keyword:</label><br/>' +
                                                      '<input type="text" id="' + windex +'-plus-keyword" text="" class="plus-keyword">' +
                                                      '</div>' +
                                                  '</div>' +
                                                  '<div class="modal-footer">' +
                                                    '<button id="' + windex + '-btn-new-data-source" type="button" class="btn btn-default new-data-source">Insert</button>' +
                                                    '<button class="btn btn-default" data-dismiss="modal">Close</button>' +
                                        '</div>' +
                                    '</div>' +
                               '</div>' +
                           '</li>' +
                            '<li class="' + widget['id'] + '"><a id="' + windex + '-panel-share" href="#" class="panel-share rounded"><span title="Share this widget" class="fa fa-link popup"><span class="popuptext" id="' + widget['id'] + '-popup">Popup text...</span></span></a></li>' +
                            '<li><a href="#" id="' + widget['id'] + '-move-page" class="rounded move-page"><span id="' + windex + '-lizard" class="fa fa-arrows" title="Move this widget on the title of the dashboard where you would insert it."></span></a></li>' +
                            '<li><a href="#" id="' + widget['id'] + '-panel-fullscreen" class="panel-fullscreen rounded"><span title="Expand this widget" class="fa fa-expand"></span></a></li>' +
                            '<li><a href="#" id="' + widget['id'] + '-remove-page" class="rounded remove-page"><span title="Remove this widget" class="fa fa-remove remove-widget"></span></a></li>' +
                        '</ul>' +
                    '</div>' +
                    '<div class="panel-body">' +
                        '<div id="' + widget['id'] + '-loader" class="loader-container">' +
                            '<img src="img/loader.gif" width="50" height="50" class="loader">' +
                        '</div>' +
                        '<div id="' + widget['id'] + '-container" class="row stacked">' +
                            '<div id="' + windex + '-slider-date" class="col-md-12">' +
                                '<div id="' + widget['id'] + '-map" style="height: 330px;"></div>' +
                                '<div ' + (getType(widget['sources']) == 'static'? 'hidden': '') + ' class="row slider-date">' +
                                    '<div class="row">' +
                                        '<div id="' + widget['id'] + '-slider"></div>' +
                                    '</div>' +
                                    '<div class="col-md-12">' +
                                        '<div class="row">' +
                                            '<div class="col-md-3">' +
                                                '<span class="slider-date button-play"><span id="' + widget['id'] + '-slider-button" class="slider-button fa fa-play"></span></span>' +
                                                '<span class="slider-date button-back"><span id="' + widget['id'] + '-slider-button-back" class="slider-button-backward fa fa-step-backward"></span></span>' +
                                                '<span class="slider-date button-step"><span id="' + widget['id'] + '-slider-button-step" class="slider-button-step fa fa-step-forward"></span></span>' +
                                            '</div>' +
                                            '<div class="col-md-9 slider-value">' +
                                                '<span id="' + widget['id'] + '-slider-value"></span>' +
                                            '</div>' +
                                        '</div>' +
                                    '</div>' +
                                    '<div class="col-md-6">' +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                            '<div id="' + windex + '-slider-date-graph" class="col-md-6 slider-date-graph" style="display: none;">' +
                                '<div class="row">' +
                                    '<div class="col-md-10">' +
                                        '<div id="' + windex + '-time-series-title" class="time-series-title"></div>' +
                                    '</div>' +
                                    '<div class="col-md-2" style="text-align: right;">' +
                                        '<a id="' + windex + '-sub-widget" href="#" class="widget-control-right sub-widget-remove" data-toggle="tooltip" data-placement="top" title="" data-original-title="Remove Widget"><span class="fa fa-times"></span></a>' +
                                    '</div>' +
                                '</div>' +
                                '<div class="row">' +
                                    '<div id="' + windex + '-graph-loader" class="loader-container">' +
                                        '<img src="img/loader.gif" width="50" height="50" class="loader">' +
                                    '</div>' +
                                    '<div class="chart-holder" id="' + widget['id'] + '-dashboard-line" width="421" height="342"></div>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
                '<!-- END SENTILO BLOCK -->';
        return html;
    }

    /*
        Shows the current panel in fullscreen mode
        @panel The panel to show in fullscreen mode
    */
    function panelFullscreen(panel){
        if(panel.hasClass("panel-fullscreened")){
            panel.removeClass("panel-fullscreened").unwrap();
            panel.find(".panel-body,.chart-holder").css("height","");
            panel.find(".panel-fullscreen .fa").removeClass("fa-compress").addClass("fa-expand");

            $(window).resize();
        }else{
            var head    = panel.find(".panel-heading");
            var body    = panel.find(".panel-body");
            var footer  = panel.find(".panel-footer");
            var hplus   = 30;

            if(body.hasClass("panel-body-table") || body.hasClass("padding-0")){
                hplus = 0;
            }
            if(head.length > 0){
                hplus += head.height()+21;
            }
            if(footer.length > 0){
                hplus += footer.height()+21;
            }

            panel.find(".panel-body,.chart-holder").height($(window).height() - hplus);


            panel.addClass("panel-fullscreened").wrap('<div class="panel-fullscreen-wrap"></div>');
            panel.find(".panel-fullscreen .fa").removeClass("fa-expand").addClass("fa-compress");

            $(window).resize();
        }
    }

    /*
        Attaches all the listeners to the active element of a widget (buttons, etc.)
        @widget The widget where the data will be loaded
        @windex The widget index in the current page
    */
    function addWidgetActions(widget, windex) {
        // Plus widget open action
        $(".add-source").click(function(){
            var windex = $(this).attr('id').split('-')[0];
            $("#" + windex + "-modal").modal({
                backdrop: 'static',
                keyboard: false
            }).show();
        });

        // Plus new dataset select action
        $('#' + widget['id'] + ' #' + windex + '-plus-dataset').on('change', function () {
            var dataset = datasets[$(this).val()];
            $('#' + widget['id'] + ' #' + windex + '-plus-info').html(
                '<div class="option-value"> The data is available from ' + moment(dataset['start']).format('MMMM Do YYYY, h:mm:ss a') + ' to ' + (dataset['end']==null? 'two days ago': moment(dataset['end']).format('MMMM Do YYYY, h:mm:ss a')) + ' </div>' +
                '<div class="option-value"> The data is available in ' + dataset['language'] + '. </div>'
            );

            $("#"+ windex + "-plus-type").empty();
            jQuery.each(dataset['allowed_visual_models'], function(vindex, model){
                 $("#"+ windex + "-plus-type").append('<option value="' + model + '" >' + model + '</option>');
            });
        });

        // Plus new time interval select action
        $("#" + windex + "-plus-time-interval").daterangepicker({
            ranges: {
               'Today': [moment(), moment()],
               'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
               'Last 7 Days': [moment().subtract(6, 'days'), moment()],
               'Last 30 Days': [moment().subtract(29, 'days'), moment()],
               'This Month': [moment().startOf('month'), moment().endOf('month')],
               'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            },
            opens: 'left',
            buttonClasses: ['btn btn-default'],
            applyClass: 'btn-small btn-primary',
            cancelClass: 'btn-small',
            format: 'DD.MM.YYYY',
            separator: ' to ',
            startDate: moment().subtract('days', 6),
            endDate: moment()
          },function(start, end) {
            start_date = start.toISOString();
            end_date = end.toISOString();
            $("#" + windex + "-plus-time-interval span").html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        });
        $("#" + windex + "-plus-time-interval span").html(moment().subtract('days', 6).format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));

        // Plus widget insert action
        $("#" + windex + "-btn-new-data-source").click(function (e) {
            var windex = e.target.id.split('-')[0];
            var dataset = $('#' + widget['id'] + ' #' + windex + '-plus-dataset').val();
            if(dataset != 'none') {
                var windex = $(this).attr('id').split('-')[0];
                widget['sources'].push({
                    "id": $("#"+ windex + "-plus-dataset").val(),
                    "aggregation": $("#"+ windex + "-plus-aggregation").val(),
                    "granularity": $("#"+ windex + "-plus-granularity").val(),
                    "chart": $("#"+ windex + "-plus-type").val(),
                    "type": "points",
                    "keyword": $("#"+ windex + "-plus-keyword").val(),
                    "start": start_date,
                    "end": end_date,
                    "dataset": null,
                    "markers": null
                });
                $('#' + widget['id'] + '-source-list').empty();
                widget['sources'].forEach(function(source, sindex){
                    $('#' + widget['id'] + '-source-list').append(
                        '<div  id="' + windex + '-' + sindex + '-source-item" class="row source-item">' +
                            '<div class="high-name"><strong>' + datasets[source['id']]['description'] + '</strong></div> ' +
                            '<div class="high-name"> from <strong>' + moment(source['start']).format('MMMM Do YYYY') + '</strong></div>' +
                            '<div class="high-name"> to <strong>' + moment(source['end']).format('MMMM Do YYYY') + '</strong></div> ' +
                            (source['keyword'] != '' ? '<div class="high-name"> by keyword <strong>' +  source['keyword'] + '</strong></div> ' : '') +
                            (source['aggregation'] != 'none' ? ' <div class="high-name"> by <strong>' +  source['aggregation'] + '</strong></div> ' : '') +
                            '<div class="high-name"> [' +
                                     '<span data-toggle="modal"  id="' + windex + '-' + sindex + '-modify" data-target="#' + widget['id'] + '-' + datasets[source['id']]['name'] + '-modal" class="modify">Edit</span>' +
                                     '<span id="widget-' + windex + '-source-' + sindex + '-remove" class="remove">Remove</span>]' +
                            '</div>' +
                        '</div>'
                    );
                });
                $("#" + windex + "-modal").modal().hide();
                displayWidgets(dashboards[page]['widgets']);
                widget['modified'] = (new Date()).toISOString();
                $.notify('You have inserted a data source.', "success");
            }
            else {
                $("#" + windex + "-modal").modal().hide();
            }
        });

        // Share widget action
        $('#' + widget['id'] + ' #' + windex + '-panel-share').click(function(){
            addEventsShareWidget(this);
        });

        // Fullscreen widget action
        $('#' + widget['id'] + "-panel-fullscreen").on("click",function(){
            panelFullscreen($(this).parents(".panel"));
        });

        // Remove widget action
        $('#' + widget['id'] + ' #' + widget['id'] + '-remove-page').click(function(e) {
            var windex = $(this).attr('id').split('-')[0] + '-' + $(this).attr('id').split('-')[1];
            $('#' + windex).remove();
            $.notify('You have removed the widget "' + widget['title'] + '".', "success");
            dashboards[page]['widgets'].splice(windex, 1);
        });

        // Move widget to other dashboard
        $('#' + widget['id'] + ' #' + widget['id'] + '-move-page').click(function(e) {
            dragDropDifferentPage($(this).attr('id').split('-')[0] + '-' + $(this).attr('id').split('-')[1]);
        });

        // Single dataset widget actions
        widget['sources'].forEach(function(source, sindex){
            // Single dataset select action
            $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-dataset').on('change', function () {
                var dataset = datasets[$(this).val()];
                $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-info').html(
                    '<div class="option-value"> The data is available from ' + moment(dataset['start']).format('MMMM Do YYYY') + ' to ' + (dataset['end']==null? 'two days ago': moment(dataset['end']).format('MMMM Do YYYY')) + '. </div>' +
                    '<div class="option-value"> The data is available in ' + dataset['language'] + '. </div>');
            });

            // Single time interval select action
            $("#" + windex + "-" + sindex + "-edit-time-interval").daterangepicker({
                ranges: {
                   'Today': [moment(), moment()],
                   'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                   'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                   'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                   'This Month': [moment().startOf('month'), moment().endOf('month')],
                   'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                },
                opens: 'left',
                buttonClasses: ['btn btn-default'],
                applyClass: 'btn-small btn-primary',
                cancelClass: 'btn-small',
                format: 'DD.MM.YYYY',
                separator: ' to ',
                startDate: moment(widget['sources'][sindex]['start']),
                endDate: moment(widget['sources'][sindex]['end'])
              },function(start, end) {
                widget['sources'][sindex]['start'] = start.toISOString();
                widget['sources'][sindex]['end'] = end.toISOString();
                $("#" + windex + "-" + sindex + "-edit-time-interval span").html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
            });
            $("#" + windex + "-" + sindex + "-edit-time-interval span").html(moment(widget['sources'][sindex]['start']).format('MMMM D, YYYY') + ' - ' + moment(widget['sources'][sindex]['end']).format('MMMM D, YYYY'));

            // Single change open action
            $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-modify').click(function(e) {
                var windex = $(this).attr('id').split('-')[0];
                var sindex = $(this).attr('id').split('-')[1];
                var source = widget['sources'][sindex];
                var dataset = datasets[source['id']];
                $("#" + windex + "-" + sindex + "-edit-dataset").val(source['id']);
                $("#" + windex + "-" + sindex + "-edit-time-interval").val(source['date']);
                $("#" + windex + "-" + sindex + "-edit-type").val(source['chart']);
                $("#" + windex  + "-" + sindex+ "-edit-granularity").val(source['granularity']);
                $("#" + windex  + "-" + sindex+ "-edit-aggregation").val(source['aggregation']);
                $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-info').html(
                    '<div class="option-value"> The data is available from ' + moment(dataset['start']).format('MMMM Do YYYY, h:mm:ss a') + ' to ' + (dataset['end']==null? 'two days ago': moment(dataset['end']).format('MMMM Do YYYY, h:mm:ss a')) + '. </div>' +
                    '<div class="option-value"> The data is available in ' + dataset['language'] + '. </div>');
            });

            // Single change confirm action
            $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-close').click(function(e){
                var windex = $(this).attr('id').split('-')[0];
                var sindex = $(this).attr('id').split('-')[1];
                var source = dashboards[page]['widgets'][windex]['sources'][sindex];
                dashboards[page]['widgets'][windex]["highmarker"] = [];
                dashboards[page]['widgets'][windex]["highmarkericon"] = [];
                dashboards[page]['widgets'][windex]['modified'] = (new Date()).toISOString();
                dashboards[page]['widgets'][windex]['sources'][sindex]['id'] = $("#"+ windex + "-" + sindex + "-edit-dataset").val();
                dashboards[page]['widgets'][windex]['sources'][sindex]['chart'] = $("#"+ windex + "-" + sindex + "-edit-type").val();
                dashboards[page]['widgets'][windex]['sources'][sindex]['aggregation'] = $("#"+ windex + "-" + sindex + "-edit-aggregation").val();
                dashboards[page]['widgets'][windex]['sources'][sindex]['granularity'] = $("#"+ windex + "-" + sindex + "-edit-granularity").val();
                dashboards[page]['widgets'][windex]['sources'][sindex]['keyword'] = $("#" + windex + "-" + sindex + "-edit-keyword").val().toLowerCase();
                if(dashboards[page]['widgets'][windex]['sources'][sindex]['markers'] != null)
                    dashboards[page]['widgets'][windex]['sources'][sindex]['markers'].clearLayers();
                displayWidgets(dashboards[page]['widgets']);
            });

            // Remove source action
            $('#' + 'widget-' + windex + '-source-' + sindex + '-remove').click(function(e) {
                var windex = $(this).attr('id').split('-')[1];
                var sindex = $(this).attr('id').split('-')[3];
                $.notify('You have removed your source "' + datasets[widget['sources'][sindex]['id']]['provider'] + '" on the widget "' + widget['title'] + '".', "success");
                widget['sources'].splice(sindex, 1);
                $('#' + widget['id'] + ' #' + windex + '-' + sindex + "-source-item").remove();
                displayWidgets(dashboards[page]['widgets']);
            });
        });

        // Close right sidebar
        $("#" + windex + "-sub-widget").click(function(e) {
            $("#" + widget['id']).css("width", "49%");
            widget['data'] = [];
            $("#" + windex + "-slider-date").removeClass('col-md-6').addClass('col-md-12');
            $("#" + windex + "-slider-date-graph").hide()
            widget["highmarker"].forEach(function(highmarker, hindex){
                var flag = false;
                widget['sources'].forEach(function(source, sindex){
                    if(source['aggregation'] != 'none')
                        flag = true;
                });
                if(flag)
                    widget['map'].removeLayer(highmarker);
                $('.' + highmarker.options.icon.options.className).empty();
                $('.' + highmarker.options.icon.options.className).empty();
                highmarker.setIcon(dashboards[page]['widgets'][windex]["highmarkericon"][hindex]);
            });
            widget["highmarker"] = [];
            widget["highmarkericon"] = [];
            widget['data'] = [];
        });

        // Change widget name
        $('#' + widget['id'] + '-title').dblclick(function(){
            old = $(this).text();
            $(this).html('<input class="input-widget-title" type="text" name="search" value=""/>');
            $('.input-widget-title').keypress(function (e) {
               var key = e.which;
               var id = $(this);
               if(key == 13) {
                    if($(this).val() == '') {
                        $(this).parent().html('Blank title');
                        dashboards[page]['widgets'][windex]['title'] = $(this).val();
                    }
                    else {
                        $(this).parent().html($(this).val());
                        dashboards[page]['widgets'][windex]['title'] = $(this).val();
                    }
               }
            });
        });

        // Display widgets content
        if (widget['sources'].length > 0) {
            widget['sources'].forEach(function(source, sindex){
                // Populate map
                initMap(windex, sindex);

                // Single forward step action
                $("#" + widget['id'] + "-slider-button-step").click(function() {
                    dashboards[page]['widgets'][windex]["highmarker"] = [];
                    dashboards[page]['widgets'][windex]["highmarkericon"] = [];
                    $("#" + windex + "-slider-date").removeClass('col-md-8').addClass('col-md-12');
                    $("#" + windex + "-slider-date-graph").hide()
                    updateMap(windex, sindex, +1);
                });

                // Single backward step action
                $("#" + widget['id'] + "-slider-button-back").click(function() {
                    dashboards[page]['widgets'][windex]["highmarker"] = [];
                    dashboards[page]['widgets'][windex]["highmarkericon"] = [];
                    $("#" + windex + "-slider-date").removeClass('col-md-8').addClass('col-md-12');
                    $("#" + windex + "-slider-date-graph").hide()
                    updateMap(windex, sindex, -1);
                });

                // Single play step action
                $("#" + widget['id'] + "-slider-button").click(function() {
                    $("#" + widget['id'] + "-slider-button").toggleClass('fa-play fa-pause');
                    if($("#" + widget['id'] + "-slider-button").hasClass("fa-play")) {
                        clearInterval(dashboards[page]['widgets'][windex]["refreshIntervalId"]);
                    }
                    else {
                        dashboards[page]['widgets'][windex]["refreshIntervalId"] = setInterval(function() {
                        updateMap(windex, sindex) }, 1000);
                        dashboards[page]['widgets'][windex]["highmarker"] = [];
                        dashboards[page]['widgets'][windex]["highmarkericon"] = [];
                        $("#" + windex + "-slider-date").removeClass('col-md-6').addClass('col-md-12');
                        $("#" + windex + "-slider-date-graph").hide()
                    }
                });
            });
        }
        else {
            $("#" + widget['id'] + "-loader").hide();
            $("#" + widget['id'] + "-slider-button").show();
        }
    }

    /*
        Displays a set of widgets
        @widgets The widgets to be displayed
    */
    function displayWidgets(widgets) {
        $(".page-content-wrap").empty();
        widgets.forEach(function(widget, windex){
            $(".page-content-wrap").append(drawWidget(widget, windex));
            addWidgetActions(widget, windex);
        });
        $('.panel-body').click(function(e) {
            e.stopPropagation();
        });

        $("body").removeClass("modal-open");
    }

    /*
        Loads the current dashboard
    */
    function loadDashboard() {
        var new_shared_widget = decodeURIComponent(window.location.href).split('widget=')[1];
        var new_shared_dashboard = decodeURIComponent(window.location.href).split('widgets=')[1];

        if(typeof new_shared_widget != 'undefined' || typeof new_shared_dashboard != 'undefined') {
            var id = Object.keys(dashboards).length + 1;
            var default_dashboard_name = 'Shared Dashboard';
            page = 'page-' + id;
            dashboards[page] = {};
            dashboards[page]['name'] = default_dashboard_name;
            dashboards[page]['widgets'] = (typeof new_shared_dashboard == 'undefined') ? [JSON.parse(new_shared_widget)] : JSON.parse(new_shared_dashboard)['widgets'];
            $('<li id="' + page + '" class="dashboard-page"> ' + default_dashboard_name + ' </span> </li>').insertBefore('.add');
            addEventsExistingDashboardItem();
        }

        $('#bread-item').html(dashboards[page]['name'] + '<span id="popup-dashboard" class="fa fa-link popup-dashboard"></span>');
        $('#' + page).addClass('active');
        addEventsShareDashboard();
        displayWidgets(dashboards[page]['widgets']);
        dragDropSamePage();
    }

    loadDashboard();

});
