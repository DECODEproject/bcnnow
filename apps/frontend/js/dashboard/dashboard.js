$(document).ready(function() {
    var api_endpoint = 'http://2a64aef5.ngrok.io';
    var start_date = moment().subtract('days', 6).toISOString();
    var end_date = moment().toISOString();
    var options = { weekday: "long", year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" };
    var doubleClickTime = 0;
    var threshold = 200;
    var lineColors = ['#4D9DE0', '#E15554', '#E1BC29', '#3BB273', '#7768AE'];

    function doDashboardPageOnClick(element) {
        if (!$('.input-dashboard-page').length) {
            pages[page]['widgets'].forEach(function(widget, windex){
                clearInterval(pages[page]['widgets'][windex]["refreshIntervalId"]);
            });
            $('.dashboard-page').removeClass('active');
            $(element).addClass('active');
            $(".page-content-wrap").empty();
            page = $(element).attr('id');
            if (page == 'page-0') {
                pages[page] = {
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
            $('#bread-item').html(pages[page]['name'] + '<span id="popup-dashboard" class="fa fa-link popup-dashboard"></span>');
            shareDashboard();
            displayWidgets(pages[$(element).attr('id')]['widgets']);
            windowHeight = $(window).innerHeight();
            $('.page-content').css('min-height', windowHeight);
        }
    }

    function onDashboardPageDoubleClick(element) {
        doubleClickTime = new Date();
        old = $(element).text().trim();
        $(element).html('<input class="input-dashboard-page" type="text" name="search" value="' + old + '"/>');
        $('.input-dashboard-page').keypress(function (e) {
           var key = e.which;
           var id = $(this).parent().attr('id');
           if(key == 13) {
                if($(this).val() == '') {
                    $.notify('You have removed the dashboard page.', "success");
                    $(this).parent().remove();
                    delete pages[id];
                }
                else {
                    $(this).parent().html($(this).val());
                    $.notify('You have changed the dashboard name.', "success");
                    pages[id]['name'] = $(this).val();
                    $('#bread-item').html(pages[page]['name'] + '<span id="popup-dashboard" class="fa fa-link popup-dashboard"></span>');
                }
           }
        });
    }

    function displayWidgets(widgets) {
        $(".page-content-wrap").empty();
        html= '';
        widgets.forEach(function(widget, windex){
            html =  '<!-- START SENTILO BLOCK -->' +
                    '<div class="panel panel-default" ondragstart="drag(event)" draggable="true" id="' + widget['id'] + '">' +
                        '<div class="panel-heading">' +
                            '<div class="panel-title-box">' +
                                '<h3 id="id-' + widget['id'] + '" class="widget-title">' + widget['title'] + '</h3> <span class="creator-authors"> created by ';
                                widget['authors'].forEach(function(author, sindex){
                                    html +=        '<span class="high-name">' + author  + '</span>';
                                });
                                html += ' and modified at <span id="' + windex + '-modified" class="high-name">' + widget['modified'] + '</span></span>';

            html += '<span class="' + windex + '-source-list">';
            html +=         '<div class="row">' +
                                '<div class="high-name header-column col-md-2">' + 'Data' + '</div> ' +
                                '<div class="high-name header-column col-md-2">' + 'Source' + '</div> ' +
                                '<div class="high-name header-column col-md-2">' + 'From' + '</div>' +
                                '<div class="high-name header-column col-md-2">' + 'To' + '</div> ' +
                                '<div class="high-name header-column col-md-2">' + 'Filtered by' + '</div> ' +
                                '<div class="high-name header-column col-md-2">' + 'Aggregated by' + '</div> ' +
                                '<div class="high-name header-column col-md-1"> ' + 'Commands' +  '</div> ' +
                            '</div>';
            widget['sources'].forEach(function(source, sindex){
                html +=         '<div  id="' + windex + '-' + sindex + '-source-item" class="row source-item">' +
                                    '<div class="high-name col-md-2">' + datasets[source['id']]['description'] + '</div> ' +
                                    '<div class="high-name col-md-2">' + datasets[source['id']]['provider'] + '</div> ' +
                                    '<div class="high-name col-md-2">' + moment(source['start']).format('MMMM Do YYYY') + '</div>' +
                                    '<div class="high-name col-md-2">' + moment(source['end']).format('MMMM Do YYYY') + '</div> ' +
                                    '<div class="high-name col-md-2">' + (source['keyword'] != '' ? source['keyword']: '-')  + '</div> ' +
                                    '<div class="high-name col-md-2">' + (source['aggregation'] != 'none' ? source['aggregation']: '-')  + '</div> ' +
                                    '<div class="high-name col-md-1"> ' +
                                         '<span data-toggle="modal"  id="' + windex + '-' + sindex + '-modify" data-target="#' + widget['id'] + '-' + datasets[source['id']]['name'] + '-modal" class="modify">Edit</span>' +
                                         '<span id="widget-' + windex + '-source-' + sindex + '-remove" class="remove">Remove</span>' +
                                    '</div> ' +
                                '</div>';
                html +=         '<div id="' + widget['id'] + '-' + datasets[source['id']]['name'] + '-modal" class="modal fade" role="dialog">' +
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
                      html +=                   '<option value="' + sindex + '" >' + dataset['description'] + '</option>';
                });
                html +=                       '</select>' +
                                              '<div id="' + windex + '-' + sindex + '-edit-info"></div><br/>' +
                                              '<label for="time_interval">Select time interval:</label><br/>' +
                                              '<div id="' + windex + '-' + sindex + '-edit-time-interval" class="dtrange">' +
                                                    '<span></span><b class="caret"></b>' +
                                              '</div><br/><br/><br/>' +
                                              '<label for="type">Select time granularity:</label>' +
                                              '<select class="form-control" id="' + windex + '-' + sindex + '-edit-granularity">' +
                                                '<option value="cumulative">Cumulative</option>' +
                                                '<option value="minutes">Minutes</option>' +
                                                '<option value="hours">Hours</option>' +
                                                '<option value="days">Days</option>' +
                                                '<option value="weeks">Weeks</option>' +
                                                '<option value="months">Months</option>' +
                                              '</select><br/>' +
                                              '<label for="type">Select visualization type:</label>' +
                                              '<select class="form-control" id="' + windex + '-' + sindex + '-edit-type">' +
                                                '<option value="points-map" ' + (source['chart'] == 'points-map'?'selected':'') + '>Markers map</option>' +
                                                '<option value="heat-map" ' + (source['chart'] == 'heat-map'?'selected':'') + '>Heat map</option>' +
                                              '</select><br/>' +
                                              '<label for="aggregation"> Select geographical aggregation:</label>' +
                                              '<select class="form-control" id="' + windex + '-' + sindex + '-edit-aggregation">' +
                                                '<option value="none" ' + (source['aggregation'] == 'none'?'selected':'') + '>None</option>' +
                                                '<option value="neighbourhood" ' + (source['aggregation'] == 'neighbourhood'?'selected':'') + '>Neighbourhood</option>' +
                                                '<option value="district" ' + (source['aggregation'] == 'district'?'selected':'') + '>District</option>' +
                                              '</select><br/>' +
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

            html +=         '</span></div>' +
                            '<ul class="panel-controls panel-controls-title">' +
                               '<li class="rounded"><span id="' + windex + '-add-source" class="add-source fa fa-plus" title="Add a source"></span>' +

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
                                                    '<option value="none">None</option>';
            jQuery.each(datasets, function(sindex, dataset){
                  html +=                           '<option value="' + sindex + '">' + dataset['description'] + '</option>';
            });
            html +=                              '</select>' +
                                                 '<div id="' + windex + '-plus-info"></div><br/>' +
                                                  '<label for="time_interval">Select time interval:</label><br/>' +
                                                  '<div id="' + windex + '-plus-time-interval" class="dtrange">' +
                                                        '<span></span><b class="caret"></b>' +
                                                  '</div><br/><br/><br/>' +
                                                  '<label for="type">Select time granularity:</label>' +
                                                  '<select class="form-control" id="' + windex + '-plus-granularity">' +
                                                    '<option value="cumulative">Cumulative</option>' +
                                                    '<option value="minutes">Minutes</option>' +
                                                    '<option value="hours">Hours</option>' +
                                                    '<option value="days">Days</option>' +
                                                    '<option value="weeks">Weeks</option>' +
                                                    '<option value="months">Months</option>' +
                                                  '</select><br/>' +
                                                  '<label for="type">Select visualization type:</label>' +
                                                  '<select class="form-control" id="' + windex + '-plus-type">' +
                                                    '<option value="points-map">Markers map</option>' +
                                                    '<option value="heat-map">Heat map</option>' +
                                                  '</select><br/>' +
                                                  '<label for="aggregation">Select geographical aggregation:</label>' +
                                                  '<select class="form-control" id="' + windex + '-plus-aggregation">' +
                                                    '<option value="none">None</option>' +
                                                    '<option value="lneighbourhood">Neighbourhood</option>' +
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
                                '<li><a href="#" class="rounded move-page"><span id="' + windex + '-lizard" class="fa fa-arrows" ondragstart="drag(event)" draggable="true" title="Move this widget on the title of the dashboard where you would insert it."></span></a></li>' +
                                '<li><a href="#" class="panel-fullscreen rounded"><span title="Expand this widget" class="fa fa-expand"></span></a></li>' +
                                '<li><a href="#" id="' + windex + '-remove-page" class="rounded remove-page"><span title="Remove this widget" class="fa fa-remove remove-widget"></span></a></li>' +
                            '</ul>' +
                        '</div>' +
                        '<div class="panel-body">' +
                            '<div id="' + widget['id'] + '-loader" class="loader-container">' +
                                '<img src="img/loader.gif" width="50" height="50" class="loader">' +
                            '</div>' +
                            '<div id="' + widget['id'] + '-container" class="row stacked">' +
                                '<div id="' + windex + '-slider-date" class="col-md-12">' +
                                    '<div id="' + widget['id'] + '-map" style="height: 330px;"></div>' +
                                    '<div ' + (getType(pages[page]['widgets'][windex]['sources']) == 'static'? 'hidden': '') + ' class="row slider-date">' +
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
                                '<div id="' + windex + '-slider-date-graph" class="col-md-4 slider-date-graph" style="display: none;">' +
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

            $(".page-content-wrap").append(html);

            $('#' + widget['id'] + ' #' + windex + '-plus-dataset').on('change', function () {
                var sindex = $(this).val();
                $('#' + widget['id'] + ' #' + windex + '-plus-info').html('<div class="option-value"> The data is available from <span class="high-name"> ' + moment(datasets[sindex]['start']).format('MMMM Do YYYY, h:mm:ss a') + ' </span> to <span class="high-name">  ' + (datasets[sindex]['end']==null? 'now': moment(datasets[sindex]['end']).format('MMMM Do YYYY, h:mm:ss a')) + '</span>. </div>' +
                                                    '<div class="option-value"> The data is available in <span class="high-name"> ' + datasets[sindex]['language'] + '</span>. </div>');
            });

            $('#' + widget['id'] + ' #' + windex + '-panel-share').click(function(){
                shareWidget(this);
            });

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

            $(".add-source").click(function(){
                var windex = $(this).attr('id').split('-')[0];
                $("#" + windex + "-modal").modal({
                    backdrop: 'static',
                    keyboard: false
                }).show();
            });

            $('.remove').click(function(e) {
                var windex = $(this).attr('id').split('-')[1];
                var sindex = $(this).attr('id').split('-')[3];
                $.notify('You have removed your source "' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['provider'] + '" on the widget "' + pages[page]['widgets'][windex]['title'] + '".', "success");
                pages[page]['widgets'][windex]['sources'].splice(sindex, 1);
                $('#' + widget['id'] + ' #' + windex + '-' + sindex + "-source-item").remove();
                displayWidgets(pages[page]['widgets']);
            });

            $('#' + widget['id'] + ' #' + windex + '-remove-page').click(function(e) {
                var windex = $(this).attr('id').split('-')[0];
                $('#' + pages[page]['widgets'][windex]['id']).remove();
                $.notify('You have removed the widget "' + pages[page]['widgets'][windex]['title'] + '".', "success");
                pages[page]['widgets'].splice(windex, 1);
                windowHeight = $(window).innerHeight();
                $('.page-content').css('min-height', windowHeight);
            });

            function panel_fullscreen(panel){

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

            $(".panel-fullscreen").on("click",function(){
                panel_fullscreen($(this).parents(".panel"));
                return false;
            });

            $("#" + windex + "-btn-new-data-source").click(function (e) {
                var windex = e.target.id.split('-')[0];
                var dataset = $('#' + widget['id'] + ' #' + windex + '-plus-dataset').val();
                if(dataset != 'none') {
                    var windex = $(this).attr('id').split('-')[0];
                    pages[page]['widgets'][windex]['sources'].push(
                        {
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
                    $('.' + windex + '-source-list').empty();
                    $('.' + windex + '-source-list').append('<div class="row">' +
                                        '<div class="high-name header-column col-md-2">' + 'Data' + '</div> ' +
                                        '<div class="high-name header-column col-md-2">' + 'Source' + '</div> ' +
                                        '<div class="high-name header-column col-md-2">' + 'From' + '</div>' +
                                        '<div class="high-name header-column col-md-2">' + 'To' + '</div> ' +
                                        '<div class="high-name header-column col-md-2">' + 'Filtered by' + '</div> ' +
                                        '<div class="high-name header-column col-md-1"> ' + 'Commands' +  '</div> ' +
                                    '</div>');
                    pages[page]['widgets'][windex]['sources'].forEach(function(source, sindex){
                        $('.' + windex + '-source-list').append(
                            '<div  id="' + windex + '-' + sindex + '-source-item" class="row source-item">' +
                                '<div class="high-name col-md-2">' + datasets[source['id']]['description'] + '</div> ' +
                                '<div class="high-name col-md-2">' + datasets[source['id']]['provider'] + '</div> ' +
                                '<div class="high-name col-md-2">' + moment(source['start']).format('MMMM Do YYYY') + '</div>' +
                                '<div class="high-name col-md-2">' + moment(source['end']).format('MMMM Do YYYY') + '</div> ' +
                                '<div class="high-name col-md-2">' + (source['keyword'] != '' ? source['keyword']: '-')  + '</div> ' +
                                '<div class="high-name col-md-1"> ' +
                                         '<span data-toggle="modal"  id="' + windex + '-' + sindex + '-modify" data-target="#' + widget['id'] + '-' + datasets[source['id']]['name'] + '-modal" class="modify">Edit</span>' +
                                         '<span id="widget-' + windex + '-source-' + sindex + '-remove" class="remove">Remove</span>' +
                                '</div> ' +
                            '</div>'
                        );
                    });
                    $("#" + windex + "-modal").modal().hide();
                    displayWidgets(pages[page]['widgets']);
                    pages[page]['widgets'][windex]['modified'] = (new Date()).toISOString();
                    $('#' + widget['id'] + ' #' + windex + '-modified').html(pages[page]['widgets'][windex]['modified']);
                    $.notify('You have inserted a data source.', "success");
                }
                else {
                    $("#" + windex + "-modal").modal().hide();
                }
            });

            widget['sources'].forEach(function(source, sindex){

                $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-dataset').on('change', function () {
                    var optionindex = $(this).val();
                    $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-info').html('<div class="option-value"> The data is available from <span class="high-name"> ' + moment(datasets[optionindex]['start']).format('MMMM Do YYYY, h:mm:ss a') + ' </span> to <span class="high-name">  ' + (datasets[optionindex]['end']==null? 'now': moment(datasets[optionindex]['end']).format('MMMM Do YYYY, h:mm:ss a')) + '</span>. </div>' +
                                                        '<div class="option-value"> The data is available in <span class="high-name"> ' + datasets[optionindex]['language'] + '</span>. </div>');
                });

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
                    startDate: moment().subtract('days', 6),
                    endDate: moment()
                  },function(start, end) {
                    pages[page]['widgets'][windex]['sources'][sindex]['start'] = start.toISOString();
                    pages[page]['widgets'][windex]['sources'][sindex]['end'] = end.toISOString();
                    $("#" + windex + "-" + sindex + "-edit-time-interval span").html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
                });
                $("#" + windex + "-" + sindex + "-edit-time-interval span").html(moment(pages[page]['widgets'][windex]['sources'][sindex]['start']).format('MMMM D, YYYY') + ' - ' + moment(pages[page]['widgets'][windex]['sources'][sindex]['end']).format('MMMM D, YYYY'));

                $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-modify').click(function(e) {
                    var windex = $(this).attr('id').split('-')[0];
                    var sindex = $(this).attr('id').split('-')[1];
                    var source = pages[page]['widgets'][windex]['sources'][sindex];
                    $("#" + windex + "-" + sindex + "-edit-dataset").val(source['id']);
                    $("#" + windex + "-" + sindex + "-edit-time-interval").val(source['date']);
                    $("#" + windex + "-" + sindex + "-edit-type").val(source['chart']);
                    $("#" + windex  + "-" + sindex+ "-edit-granularity").val(source['granularity']);
                    $("#" + windex  + "-" + sindex+ "-edit-aggregation").val(source['aggregation']);
                    $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-info').html('<div class="option-value"> The data is available from <span class="high-name"> ' + moment(datasets[source['id']]['start']).format('MMMM Do YYYY, h:mm:ss a') + ' </span> to <span class="high-name">  ' + (datasets[source['id']]['end']==null? 'now': moment(datasets[source['id']]['end']).format('MMMM Do YYYY, h:mm:ss a')) + '</span>. </div>' +
                                                        '<div class="option-value"> The data is available in <span class="high-name"> ' + datasets[source['id']]['language'] + '</span>. </div>');
                });
            });

            $("#" + windex + "-sub-widget").click(function(e) {
                $("#" + windex + "-slider-date").removeClass('col-md-8').addClass('col-md-12');
                $("#" + windex + "-slider-date-graph").hide()
                pages[page]['widgets'][windex]["highmarker"].forEach(function(highmarker, hindex){
                    highmarker.setIcon(pages[page]['widgets'][windex]["highmarkericon"][hindex]);
                    pages[page]['widgets'][windex]["highmarker"] = [];
                    pages[page]['widgets'][windex]["highmarkericon"] = [];
                    pages[page]['widgets'][windex]['data'] = [];
                });
            });


            $('.widget-title').dblclick(function(){
                old = $(this).text();
                $(this).html('<input class="input-widget-title" type="text" name="search" value=""/>');
                $('.input-widget-title').keypress(function (e) {
                   var key = e.which;
                   var id = $(this);
                   if(key == 13) {
                        if($(this).val() == '') {
                            $(this).parent().html('Blank title');
                            pages[id]['name'] = $(this).val();
                        }
                        else {
                            $(this).parent().html($(this).val());
                            pages[id]['name'] = $(this).val();
                        }
                   }
                });
            });

            if (widget['sources'].length > 0) {
                widget['sources'].forEach(function(source, sindex){
                   initialize_map(windex, sindex);
                    $("#" + widget['id'] + "-slider-button-step").click(function() {
                        pages[page]['widgets'][windex]["highmarker"] = [];
                        pages[page]['widgets'][windex]["highmarkericon"] = [];
                        $("#" + windex + "-slider-date").removeClass('col-md-8').addClass('col-md-12');
                        $("#" + windex + "-slider-date-graph").hide()
                        update_map(windex, sindex, +1);
                    });
                    $("#" + widget['id'] + "-slider-button-back").click(function() {
                        pages[page]['widgets'][windex]["highmarker"] = [];
                        pages[page]['widgets'][windex]["highmarkericon"] = [];
                        $("#" + windex + "-slider-date").removeClass('col-md-8').addClass('col-md-12');
                        $("#" + windex + "-slider-date-graph").hide()
                        update_map(windex, sindex, -1);
                    });
                    $("#" + widget['id'] + "-slider-button").click(function() {
                        $("#" + widget['id'] + "-slider-button").toggleClass('fa-play fa-pause');
                        if($("#" + widget['id'] + "-slider-button").hasClass("fa-play")) {
                            clearInterval(pages[page]['widgets'][windex]["refreshIntervalId"]);
                        }
                        else {
                            pages[page]['widgets'][windex]["refreshIntervalId"] = setInterval(function() { update_map(windex, sindex) }, 1000);
                            pages[page]['widgets'][windex]["highmarker"] = [];
                            pages[page]['widgets'][windex]["highmarkericon"] = [];
                            $("#" + windex + "-slider-date").removeClass('col-md-8').addClass('col-md-12');
                            $("#" + windex + "-slider-date-graph").hide()
                        }
                    });



                    widget['sources'].forEach(function(source, sindex){
                        if($("#" + windex + "-" + sindex + "-edit-time-interval").length > 0){
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
                                startDate: moment().subtract('days', 6),
                                endDate: moment()
                              },function(start, end) {
                                $("#" + windex + "-" + sindex + "-edit-time-interval span").html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
                                pages[page]['widgets'][windex]['sources'][sindex]['start'] = start.toISOString();
                                pages[page]['widgets'][windex]['sources'][sindex]['end'] = end.toISOString();
                            });
                        }
                        $("#" + windex + "-" + sindex + "-edit-time-interval span").html(moment(pages[page]['widgets'][windex]['sources'][sindex]['start']).format('MMMM D, YYYY') + ' - ' + moment(pages[page]['widgets'][windex]['sources'][sindex]['end']).format('MMMM D, YYYY'));
                     });

                    $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-close').click(function(e){
                        var windex = $(this).attr('id').split('-')[0];
                        var sindex = $(this).attr('id').split('-')[1];
                        var source = pages[page]['widgets'][windex]['sources'][sindex];
                        pages[page]['widgets'][windex]["highmarker"] = [];
                        pages[page]['widgets'][windex]["highmarkericon"] = [];
                        pages[page]['widgets'][windex]['sources'][sindex]['name'] = $("#"+ windex + "-" + sindex + "-edit-dataset").val();
                        pages[page]['widgets'][windex]['sources'][sindex]['chart'] = $("#"+ windex + "-" + sindex + "-edit-type").val();
                        pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] = $("#"+ windex + "-" + sindex + "-edit-aggregation").val();
                        pages[page]['widgets'][windex]['sources'][sindex]['granularity'] = $("#"+ windex + "-" + sindex + "-edit-granularity").val();
                        pages[page]['widgets'][windex]['sources'][sindex]['keyword'] = $("#" + windex + "-" + sindex + "-edit-keyword").val().toLowerCase();
                        pages[page]['widgets'][windex]['sources'][sindex]['markers'].clearLayers();

                        $('.' + windex + '-source-list').empty();
                        pages[page]['widgets'][windex]['sources'].forEach(function(source, sindex){
                            $('.' + windex + '-source-list').append(
                                '<div  id="' + windex + '-' + sindex + '-source-item" class="row source-item">' +
                                    '<div class="high-name col-md-2">' + datasets[source['id']]['description'] + '</div> ' +
                                    '<div class="high-name col-md-2">' + datasets[source['id']]['provider'] + '</div> ' +
                                    '<div class="high-name col-md-2">' + moment(source['start']).format('MMMM Do YYYY') + '</div>' +
                                    '<div class="high-name col-md-2">' + moment(source['end']).format('MMMM Do YYYY') + '</div> ' +
                                    '<div class="high-name col-md-2">' + (source['keyword'] != '' ? source['keyword']: '-')  + '</div> ' +
                                    '<div class="high-name col-md-1"> ' +
                                         '<span data-toggle="modal"  id="' + windex + '-' + sindex + '-modify" data-target="#' + widget['id'] + '-' + datasets[source['id']]['name'] + '-modal" class="modify">Edit</span>' +
                                         '<span id="widget-' + windex + '-source-' + sindex + '-remove" class="remove">Remove</span>' +
                                    '</div> ' +
                                '</div>'
                            );
                        });


                        $('.remove').click(function(e) {
                            var windex = $(this).attr('id').split('-')[1];
                            var sindex = $(this).attr('id').split('-')[3];
                            pages[page]['widgets'][windex]['sources'].splice(sindex, 1);
                            $('#' + widget['id'] + ' #' + windex + '-' + sindex + "-source-item").remove();
                            displayWidgets(pages[page]['widgets']);
                        });

                        widget['sources'].forEach(function(source, sindex){
                            if($("#" + windex + "-" + sindex + "-edit-time-interval").length > 0){
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
                                    startDate: moment().subtract('days', 6),
                                    endDate: moment()
                                  },function(start, end) {
                                    pages[page]['widgets'][windex]['sources'][sindex]['start'] = start.toISOString();
                                    pages[page]['widgets'][windex]['sources'][sindex]['end'] = end.toISOString();
                                    $("#" + windex + "-" + sindex + "-edit-time-interval span").html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
                                });
                                $("#" + windex + "-" + sindex + "-edit-time-interval span").html(moment(pages[page]['widgets'][windex]['sources'][sindex]['start']).format('MMMM D, YYYY') + ' - ' + moment(pages[page]['widgets'][windex]['sources'][sindex]['end']).format('MMMM D, YYYY'));

                            }


                            $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-modify').click(function(e) {
                                var windex = $(this).attr('id').split('-')[0];
                                var sindex = $(this).attr('id').split('-')[1];
                                var source = pages[page]['widgets'][windex]['sources'][sindex];
                                $("#" + windex + "-" + sindex + "-edit-dataset").val(source['id']);
                                $("#" + windex + "-" + sindex + "-edit-time-interval").val(source['date']);
                                $("#" + windex + "-" + sindex + "-edit-type").val(source['chart']);
                                $("#" + windex  + "-" + sindex+ "-edit-aggregation").val(source['aggregation']);
                                $("#" + windex  + "-" + sindex+ "-edit-granularity").val(source['granularity']);
                                $('#' + widget['id'] + ' #' + windex + '-' + sindex + '-edit-info').html('<div class="option-value"> The data is available from <span class="high-name"> ' + moment(datasets[source['id']]['start']).format('MMMM Do YYYY, h:mm:ss a') + ' </span> to <span class="high-name">  ' + (datasets[source['id']]['end']==null? 'now': moment(datasets[source['id']]['end']).format('MMMM Do YYYY, h:mm:ss a')) + '</span>. </div>' +
                                                                    '<div class="option-value"> The data is available in <span class="high-name"> ' + datasets[source['id']]['language'] + '</span>. </div>');
                            });
                        });

                        pages[page]['widgets'][windex]['modified'] = (new Date()).toISOString();
                        $('#' + widget['id'] + ' #' + windex + '-modified').html(pages[page]['widgets'][windex]['modified']);
                        displayWidgets(pages[page]['widgets']);
                    });
                });
            }
            else {
                $("#" + pages[page]['widgets'][windex]['id'] + "-loader").hide();
                $("#" + pages[page]['widgets'][windex]['id'] + "-slider-button").show();
            }
        });
    }

    $(".x-navigation-minimize").on("click",function(){
        setTimeout(function(){
            rdc_resize();
        },200);
    });

    $('.dashboard-page').click(function(){
        var element = this;
        var t0 = new Date();
        if (t0 - doubleClickTime > threshold) {
            setTimeout(function () {
                if (t0 - doubleClickTime > threshold) {
                    doDashboardPageOnClick(element);
                }
            },threshold);
        }
    });

    $('.dashboard-page').dblclick(function(e){
        onDashboardPageDoubleClick(this);

    });

    $('.add').click(function(event){
        var id = Object.keys(pages).length + 1;
        $('<li id="page-' + id + '" class="dashboard-page" ondrop="drop(event)" ondragover="allowDrop(event)"> New Dashboard Page </li>').insertBefore(this);
        pages['page-'+id] = {};
        pages['page-'+id]['name'] = 'New Dashboard Page';
        pages['page-'+id]['widgets'] = [];


        $('.dashboard-page').click(function(){
            var element = this;
            var t0 = new Date();
            if (t0 - doubleClickTime > threshold) {
                setTimeout(function () {
                    if (t0 - doubleClickTime > threshold) {
                        doDashboardPageOnClick(element);
                    }
                },threshold);
            }
        });

        $('.dashboard-page').dblclick(function(e){
            onDashboardPageDoubleClick(this);
        });

        $.notify('You have inserted a dashboard page.', "success");
    });
});