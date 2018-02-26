var new_shared_widget = decodeURIComponent(window.location.href).split('widget=')[1];
var new_shared_widgets = decodeURIComponent(window.location.href).split('widgets=')[1];

function shareDashboard() {
    $('#popup-dashboard').click(function(e){
        var page_id = page;
        var shared_widgets = {'widgets': []};
        pages[page_id]['widgets'].forEach(function(widget, windex){
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

function shareWidget(element) {
    var widget_id = pages[page]['widgets'][$(element).attr('id').split('-')[0]]['id'];
    var page_id = page;
    var shared_widget = {};
    pages[page_id]['widgets'].forEach(function(widget, windex){
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

if(typeof new_shared_widget == 'undefined' && typeof new_shared_widgets == 'undefined') {
    page = "page-3";
    $('#bread-item').html(pages[page]['name'] + '<span id="popup-dashboard" class="fa fa-link popup-dashboard"></span>');
    shareDashboard();
    $('#' + page).addClass('active');
    displayWidgets(pages[page]['widgets']);
}
else {
    var id = Object.keys(pages).length + 1;
    $('<li id="page-' + id + '" class="dashboard-page" ondrop="drop(event)" ondragover="allowDrop(event)"> Shared Dashboard Page </span> </li>').insertBefore('.add');
    pages['page-'+id] = {};
    pages['page-'+id]['name'] = 'New Dashboard Page';
    if(typeof new_shared_widgets == 'undefined') {
        pages['page-'+id]['widgets'] = [];
        pages['page-'+id]['widgets'].push(JSON.parse(new_shared_widget));
    }
    else {
        pages['page-'+id]['widgets'] = JSON.parse(new_shared_widgets)['widgets'];
    }

    $('.dashboard-page').dblclick(function(e){
        onDashboardPageDoubleClick(this);
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

    page = "page-" + id;
    $('#bread-item').html(pages[page]['name'] + '<span id="popup-dashboard" class="fa fa-link popup-dashboard"></span>');
    shareDashboard();
    $('#' + page).addClass('active');
    displayWidgets(pages[page]['widgets']);
}