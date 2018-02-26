function initialize_map(windex, sindex) {
        $("#" + pages[page]['widgets'][windex]['id'] + "-loader").show();
        pages[page]['widgets'][windex]['sources'][sindex]['markers'] = new L.LayerGroup();
        try {
            map = L.map(pages[page]['widgets'][windex]['id'] + '-map').setView([41.390205,2.154007], 12);
            L.tileLayer.grayscale('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 18,
                id: 'mapbox.streets',
                accessToken: 'pk.eyJ1IjoibW1hcnJhcyIsImEiOiJjamE3MnBpd2E3MjZ1MndwNzY5YjBrdDgxIn0.zO2nGOwmSGhb8YrzhWNdeQ'
            }).addTo(map);
        }
        catch(err) {
            map = pages[page]['widgets'][windex]['map'];
        }
        c = datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'];
        pages[page]['widgets'][windex]['map'] = map;
        var query = pages[page]['widgets'][windex]['sources'][sindex]['keyword'];
        var qtxt = ''
        other_par = '';
        par_iris = 'element@payload.element,detail@payload.detail,area@payload.area,support@payload.support,channel@payload.channel,type@type,enddate@payload.enddate,startdate@payload.startdate,';
        par_asia = 'name@payload.name,enddate@payload.enddate,startdate@payload.startdate,categories@payload.categories,';
        if(c == 'iris') {
            other_par = par_iris;
            if (query != '') {
                qtxt = "&$payload.element=[" + query + "]";
            }
        }
        if(c == 'asia') {
            other_par = par_asia;
            if (query != '') {
                qtxt = "&$payload.name=[" + query + "]";
            }
        }
        var aggregation = '';
        var operators = '';
        if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none') {
            aggregation = pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + '@' + 'location.' + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + ',';
            operators = 'aggregators=avg@payload.' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + '&';
        }
        console.log(api_endopoint + "/api/v0/" + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] + "?" + operators + "group=" + aggregation + "timestamp@timestamp&fields=" + other_par + "id@payload.id,value@payload." + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + ",point@location.point.coordinates&sort=a@timestamp&isObservation&$timestamp=gte@" + pages[page]['widgets'][windex]['sources'][sindex]['start'] + ",lt@" + pages[page]['widgets'][windex]['sources'][sindex]['end'] + qtxt);
        $.ajax({
            url: api_endopoint + "/api/v0/" + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] + "?" + operators + "group=" + aggregation + "timestamp@timestamp&fields=" + other_par + "id@payload.id,value@payload." + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + ",point@location.point.coordinates&sort=a@timestamp&isObservation&$timestamp=gte@" + pages[page]['widgets'][windex]['sources'][sindex]['start'] + ",lt@" + pages[page]['widgets'][windex]['sources'][sindex]['end'] + qtxt,
            success: function(data) {
                try {
                    if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none') {
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
                                    r["id"] = element["_id"][pages[page]['widgets'][windex]['sources'][sindex]['aggregation']];
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

                    pages[page]['widgets'][windex]['sources'][sindex]['dataset'] = data;
                    $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider({
                        range: "min",
                        min: 1,
                        max: pages[page]['widgets'][windex]['sources'][sindex]['dataset'].count,
                        step: 1,
                        slide: function( event, ui ) {
                            update_map(windex, sindex);
                        }
                    });
                    $("#" + pages[page]['widgets'][windex]['id'] + "-slider-value").text('Click "Play" to see levels along time');
                    $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider('value', 0);

                    if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['colors'].length > 1) {
                        var legend = L.control({position: 'bottomright'});
                        legend.onAdd = function (map) {
                            var div = L.DomUtil.create('div', 'info legend');
                            var faultstatus = datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['cuts'];
                            div.innerHTML += '<strong> ' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['labels'] + ' </strong> <br>';
                            for (var i = faultstatus.length-1; i >= 0; i--) {
                                div.innerHTML += '<i class="circle" style="background:' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['colors'][i] + '"></i> ' + (faultstatus[i+1] ? '' : '&ge; ') + (faultstatus[i]+1) + (faultstatus[i+1] ? ' - ' + (faultstatus[i+1]) : '') + '<br>';
                            }
                            return div;
                        };
                        legend.addTo(pages[page]['widgets'][windex]['map']);
                    }
                    update_map(windex, sindex, 0);
                    $("#" + pages[page]['widgets'][windex]['id'] + "-loader").hide();
                    $("#" + pages[page]['widgets'][windex]['id'] + "-slider-button").show();
                }
                catch(err) {
                    console.log(err);
                }
            },
            error: function() {

            }
        });
    }

function update_map(windex, sindex, dir=1) {
        var val = $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider("option", "value") + dir;
        var max = $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider("option", "max");
        var markers_layer = new L.LayerGroup();
        pages[page]['widgets'][windex]['sources'][sindex]['markers'].clearLayers();
        $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider("value", (val)%(max+1) );
        footprint = moment(pages[page]['widgets'][windex]['sources'][sindex]['dataset'].records[(val-1)%(max)]["_id"]).format('dddd, MMMM Do YYYY, h:mm:ss a');
        $("#" + pages[page]['widgets'][windex]['id'] + "-slider-value").html("<span  class='tip'>" + footprint + "</span>");
        if(pages[page]['widgets'][windex]['sources'][sindex]['granularity'] != "cumulative") {
            obs = pages[page]['widgets'][windex]['sources'][sindex]['dataset'].records[(val-1)%(max)]["doc"];
        }
        else {
            obs = [];
            pages[page]['widgets'][windex]['sources'][sindex]['dataset'].records.forEach(function(record, index){
                obs = obs.concat(record["doc"]);
            });

        }
        console.log(obs);
        var heatmapdata = [];

        if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != "none") {
            $.ajax({
                dataType: "json",
                url: "assets/geojson/" + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + ".geojson",
                success: function(data) {
                    iris_boundary = new L.geoJson(data, {
                          style: function(feature) {
                            return getArea(feature, datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']], obs);
                          },
                          onEachFeature: function(feature, layer) {
                              var element = getLabel(feature, datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']], obs);
                              if(element) {
                                  layer.on({click: function(e){
                                        var commonid = 'Ciao';
                                        $("#" + windex + "-slider-date").removeClass('col-md-12').addClass('col-md-8');
                                        $("#" + windex + "-slider-date-graph").show();
                                        $("#" + windex + "-graph-loader").show();
                                        var aggregation = '';
                                        var operators = '';
                                        var geo = '';
                                        var agg = '';
                                        if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none') {
                                            aggregation = pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + '@' + 'location.' + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + ',';
                                            operators = 'aggregators=avg@payload.' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + '&';
                                            geo = "&$location." + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + "=" + commonid
                                            agg = "avg";
                                        }
                                        else {
                                            geo = "&$payload.id=" + commonid
                                            agg = 'value';
                                        }

                                        var val = $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider("option", "value");
                                        var current = '';
                                        if (pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none' && (datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'asia' || datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'iris')) {
                                            var val = pages[page]['widgets'][windex]['sources'][sindex]['dataset'].records[(val-1)%(max)]["_id"].replace(' ', 'T') + 'Z';
                                            var val0 = moment(val).set({hour:0,minute:0,second:0,millisecond:0}).toISOString();
                                            var val1 = moment(val).add(1, "days").set({hour:0,minute:0,second:0,millisecond:0}).toISOString();
                                            current = "&$timestamp=gte@" + val0 + ",lt@" + val1;
                                        }
                                        else {
                                            current = "&$timestamp=gte@" + pages[page]['widgets'][windex]['sources'][sindex]['start'] + ",lt@" + pages[page]['widgets'][windex]['sources'][sindex]['end'];
                                        }

                                        c = datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'];
                                        var query = pages[page]['widgets'][windex]['sources'][sindex]['keyword'];
                                        var qtxt = ''
                                        other_par = '';
                                        par_iris = 'element@payload.element,detail@payload.detail,area@payload.area,support@payload.support,channel@payload.channel,type@type,enddate@payload.enddate,startdate@payload.startdate,';
                                        par_asia = 'name@payload.name,enddate@payload.enddate,startdate@payload.startdate,categories@payload.categories,';
                                        if(c == 'iris') {
                                            other_par = par_iris;
                                            if (query != '') {
                                                qtxt = "&$payload.element=[" + query + "]";
                                            }
                                        }
                                        if(c == 'asia') {
                                            other_par = par_asia;
                                            if (query != '') {
                                                qtxt = "&$payload.name=[" + query + "]";
                                            }
                                        }

                                        $.ajax({
                                            url: api_endopoint + "/api/v0/" + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] + "?" + operators + "group=" + aggregation + "timestamp@timestamp&fields=" + other_par + "id@payload.id,value@payload." + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + ",point@location.point.coordinates&sort=a@timestamp&isObservation" + geo + current + qtxt,
                                            success: function(output) {
                                                try {
                                                    $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").empty();
                                                    if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'asia') {
                                                        $("#" + windex + "-time-series-title").text("ASIA ID " + commonid);
                                                        $.each(output.records, function(index, element) {
                                                            if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] == 'none') {
                                                                 var categories = '';
                                                                 for(var k in element.doc[0].categories) categories += element.doc[0].categories[k] + '; ';
                                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Name:</span> ' + element.doc[0].name + '</div>');
                                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Start Date:</span> ' + moment(element.doc[0].startdate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">End Date:</span> ' + moment(element.doc[0].enddate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Categories:</span> ' + categories + '</div>');
                                                            }
                                                            else {
                                                                $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Number of events:</span> ' + element.doc[0].count + '</div>');
                                                            }
                                                        });
                                                    }


                                                    if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'iris') {
                                                        $("#" + windex + "-time-series-title").text("IRIS ID " + commonid);
                                                        $.each(output.records, function(index, element) {
                                                            if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] == 'none') {
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Type:</span> ' + element.doc[0].type + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Area:</span> ' + element.doc[0].area + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Element:</span> ' + element.doc[0].element + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Detail:</span> ' + element.doc[0].detail + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Support:</span> ' + element.doc[0].support + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Channel:</span> ' + element.doc[0].channel + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Opening Date:</span> ' + moment(element.doc[0].startdate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                                                     $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Closing Date:</span> ' + moment(element.doc[0].enddate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                                            }
                                                            else {
                                                                $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Number of iris:</span> ' + element.doc[0].count + '</div>');
                                                            }
                                                        });
                                                    }

                                                    if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'smartcitizen' || datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'bicing') {
                                                        var sensordata = [];
                                                        var x = [];
                                                        var y = [];
                                                        $.each(output.records, function(index, element) {
                                                            var timestamp;
                                                            if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none') {timestamp = element["_id"]}
                                                            else {timestamp = element["_id"]["timestamp"]}
                                                            x.push(timestamp);
                                                            y.push(Math.floor(element["doc"][0][agg]));
                                                        });
                                                     }
                                                    $("#" + windex + "-graph-loader").hide();
                                                }
                                                catch(err) {
                                                    console.log(err);
                                                }
                                            },
                                            error: function() {
                                            }
                                        });
                                  }});
                                  layer.bindTooltip(feature.properties.neighbourhood + ' ' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['labels'] + ': ' + element.value);
                              }
                          }
                    });
                    pages[page]['widgets'][windex]['sources'][sindex]['markers'].addLayer(iris_boundary);
                    pages[page]['widgets'][windex]['map'].addLayer(pages[page]['widgets'][windex]['sources'][sindex]['markers']);
                },
                error: function() {

                }
            });
        }
        else {
            obs.forEach(function(element) {
                var value = (pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] == 'none')? (typeof datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] === "string"? element[datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue']]:datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue']) : element[datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['aggregator']];
                heatmapdata.push({lat: element["point"][1], lng: element["point"][0], value: value});
                id = element["id"];
                obsval = parseInt(element["value"]);
                icon = L.vectorIcon({
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
                            fill: getIcon(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']], obsval),
                            stroke: '#000',
                            strokeWidth: 1
                          }
                });

                var aggregation = '';
                if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != "none") {
                    aggregation = "&location." + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + "=" + id;
                }

                var marker = L.marker([element["point"][1],element["point"][0]], {icon: icon, title: 'Sensor ' + id + ': ' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['labels'] + ' ' + obsval, sentiloid: id});

                marker.on('click', function(e){
                    var commonid = e.target.options.sentiloid;
                    console.log(pages[page]);
                    pages[page]['widgets'][windex]["highmarker"].push(e.target);
                    pages[page]['widgets'][windex]["highmarkericon"].push(e.target.options.icon);
                    $('.' + 'circle-icon-' + windex + '-' + sindex + '-' + commonid).empty();
                    e.target.setIcon(L.vectorIcon({
                      className: 'circle-icon-' + windex + '-' + sindex + '-' + commonid,
                      svgHeight: 16,
                      svgWidth: 16,
                      type: 'path',
                      shape: {
                        x: '1',
                        y: '1',
                        width: '14',
                        height: '14'
                      },
                      style: {
                        fill: lineColors[pages[page]['widgets'][windex]['data'].length],
                        stroke: '#000',
                        strokeWidth: 1
                      }
                    }));
                    $('.' + 'circle-icon-' + windex + '-' + sindex + '-' + commonid).empty();
                    e.target.setIcon(L.vectorIcon({
                      className: 'circle-icon-' + windex + '-' + sindex + '-' + commonid,
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
                        fill: lineColors[pages[page]['widgets'][windex]['data'].length],
                        stroke: '#000',
                        strokeWidth: 1
                      }
                    }));
                    $("#" + windex + "-slider-date").removeClass('col-md-12').addClass('col-md-8');
                    $("#" + windex + "-slider-date-graph").show();
                    $("#" + windex + "-graph-loader").show();
                    var aggregation = '';
                    var operators = '';
                    var geo = '';
                    var agg = '';
                    if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none') {
                        aggregation = pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + '@' + 'location.' + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + ',';
                        operators = 'aggregators=avg@payload.' + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + '&';
                        geo = "&$location." + pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] + "=" + commonid
                        agg = "avg";
                    }
                    else {
                        geo = "&$payload.id=" + commonid
                        agg = 'value';
                    }

                    var val = $("#" + pages[page]['widgets'][windex]['id'] + "-slider").slider("option", "value");
                    var current = '';
                    if (pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none' && (datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'asia' || datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'iris')) {
                        var val = pages[page]['widgets'][windex]['sources'][sindex]['dataset'].records[(val-1)%(max)]["_id"].replace(' ', 'T') + 'Z';
                        var val0 = moment(val).set({hour:0,minute:0,second:0,millisecond:0}).toISOString();
                        var val1 = moment(val).add(1, "days").set({hour:0,minute:0,second:0,millisecond:0}).toISOString();
                        current = "&$timestamp=gte@" + val0 + ",lt@" + val1;
                    }
                    else {
                        current = "&$timestamp=gte@" + pages[page]['widgets'][windex]['sources'][sindex]['start'] + ",lt@" + pages[page]['widgets'][windex]['sources'][sindex]['end'];
                    }

                    c = datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'];
                    var query = pages[page]['widgets'][windex]['sources'][sindex]['keyword'];
                    var qtxt = ''
                    other_par = '';
                    par_iris = 'element@payload.element,detail@payload.detail,area@payload.area,support@payload.support,channel@payload.channel,type@type,enddate@payload.enddate,startdate@payload.startdate,';
                    par_asia = 'name@payload.name,enddate@payload.enddate,startdate@payload.startdate,categories@payload.categories,';
                    if(c == 'iris') {
                        other_par = par_iris;
                        if (query != '') {
                            qtxt = "&$payload.element=[" + query + "]";
                        }
                    }
                    if(c == 'asia') {
                        other_par = par_asia;
                        if (query != '') {
                            qtxt = "&$payload.name=[" + query + "]";
                        }
                    }

                    $.ajax({
                        url: api_endopoint + "/api/v0/" + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] + "?" + operators + "group=" + aggregation + "timestamp@timestamp&fields=" + other_par + "id@payload.id,value@payload." + datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['targetvalue'] + ",point@location.point.coordinates&sort=a@timestamp&isObservation" + geo + current + qtxt,
                        success: function(output) {
                            try {
                                $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").empty();
                                if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'asia') {
                                    $("#" + windex + "-time-series-title").text("ASIA ID " + commonid);
                                    $.each(output.records, function(index, element) {
                                        if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] == 'none') {
                                             var categories = '';
                                             for(var k in element.doc[0].categories) categories += element.doc[0].categories[k] + '; ';
                                             $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Name:</span> ' + element.doc[0].name + '</div>');
                                             $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Start Date:</span> ' + moment(element.doc[0].startdate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                             $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">End Date:</span> ' + moment(element.doc[0].enddate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                             $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Categories:</span> ' + categories + '</div>');
                                        }
                                        else {
                                            $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Number of events:</span> ' + element.doc[0].count + '</div>');
                                        }
                                    });
                                }


                                if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'iris') {
                                    $("#" + windex + "-time-series-title").text("IRIS ID " + commonid);
                                    $.each(output.records, function(index, element) {
                                        if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] == 'none') {
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Type:</span> ' + element.doc[0].type + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Area:</span> ' + element.doc[0].area + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Element:</span> ' + element.doc[0].element + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Detail:</span> ' + element.doc[0].detail + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Support:</span> ' + element.doc[0].support + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Channel:</span> ' + element.doc[0].channel + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Opening Date:</span> ' + moment(element.doc[0].startdate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                                 $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Closing Date:</span> ' + moment(element.doc[0].enddate).format('dddd, MMMM Do YYYY, h:mm:ss a') + '</div>');
                                        }
                                        else {
                                            $("#" + pages[page]['widgets'][windex]['id'] + "-dashboard-line").append('<div class="event-name"> <span class="event-bold">Number of iris:</span> ' + element.doc[0].count + '</div>');
                                        }
                                    });
                                }

                                if(datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'smartcitizen' || datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['name'] == 'bicing') {
                                    var sensordata = [];
                                    var x = [];
                                    var y = [];
                                    $.each(output.records, function(index, element) {
                                        var timestamp;
                                        if(pages[page]['widgets'][windex]['sources'][sindex]['aggregation'] != 'none') {timestamp = element["_id"]}
                                        else {timestamp = element["_id"]["timestamp"]}
                                        x.push(timestamp);
                                        y.push(Math.floor(element["doc"][0][agg]));
                                    });

                                    var d3 = Plotly.d3;

                                    var WIDTH_IN_PERCENT_OF_PARENT = 100,
                                        HEIGHT_IN_PERCENT_OF_PARENT = 100;

                                    var gd3 = d3.select('#' + pages[page]['widgets'][windex]['id'] + '-dashboard-line')
                                        .append('div')
                                        .style({
                                            width: WIDTH_IN_PERCENT_OF_PARENT + '%',
                                            'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%'
                                        });

                                    var gd = gd3.node();

                                    pages[page]['widgets'][windex]['data'].push({name: 'Sensor ' + commonid, x: x, y: y, type: 'scatter', line: {color: lineColors[pages[page]['widgets'][windex]['data'].length], width: 1}});
                                    Plotly.newPlot(gd, pages[page]['widgets'][windex]['data'], {
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
                                $("#" + windex + "-graph-loader").hide();
                            }
                            catch(err) {
                                console.log(err);
                            }
                        },
                        error: function() {
                        }
                    });
                });
                markers_layer.addLayer(marker);
            });
            var testData = {
              max: 8,
              data: heatmapdata
            };
            var cfg = {
              "radius": datasets[pages[page]['widgets'][windex]['sources'][sindex]['id']]['radius'],
              "maxOpacity": .5,
              "useLocalExtrema": true
            };
            var heatmapLayer = new HeatmapOverlay(cfg);
            heatmapLayer.setData(testData);
            if(pages[page]['widgets'][windex]['sources'][sindex]['chart'] == 'heat-map') {
                pages[page]['widgets'][windex]['sources'][sindex]['markers'].addLayer(heatmapLayer);
            }
            else {
                pages[page]['widgets'][windex]['sources'][sindex]['markers'].addLayer(markers_layer);
            }
            pages[page]['widgets'][windex]['map'].addLayer(pages[page]['widgets'][windex]['sources'][sindex]['markers']);
        }
    }