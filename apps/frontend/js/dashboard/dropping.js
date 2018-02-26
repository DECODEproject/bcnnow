function allowDrop(ev) {
    ev.preventDefault();

}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);

}

function drop(ev) {
    ev.preventDefault();
    var widget_id = pages[page]['widgets'][ev.dataTransfer.getData("text").split('-')[0]]['id'];
    var target_page_id = ev.target.id;
    var previous_page_id = page;
    var moved_widget = {};
    var index = -1;
    if(target_page_id != '') {
        $('#' + widget_id).remove();
        pages[previous_page_id]['widgets'].forEach(function(widget, windex){
            if(widget['id'] == widget_id) {
                moved_widget = widget;
                index = windex;
            }
        });
        pages[previous_page_id]['widgets'].splice(index, 1);
        pages[target_page_id]['widgets'].push(moved_widget);
        $.notify('You have moved your widget "' + moved_widget['title'] + '" on the dashboard page "' + pages[target_page_id]['name'] + '".', "success");
    }
}