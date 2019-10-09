/*
    Get cookie value
*/
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function getDashboards() {
    // if logged call server for available dasboards for user
    // in other case return defaults as is

    cookieValue = getCookie("session-token");
    if (cookieValue == null) {
        cookieValue = getCookie("session-id");
    }

    if (cookieValue != null) {
        // get dasboards from server
        var ret = $.ajax({
            async: false,
            url: url_root + "api/v0/get_public_dashboards",
            beforeSend: function (xhr) {
                // authenticate the call 
                xhr.setRequestHeader ("Authorization", "Bearer " + cookieValue);
            },
            success: function(data) {
                // var returnValue = jQuery.extend(true, {}, data);
                return data;
            },
            error: function() {
            }
        });

        if (ret['status'] == 200) {

            responseText = ret['responseText'];
            responseJson = JSON.parse(responseText);
            return responseJson;
        }
    }

    return null;

}

function getPrivateDashboards() {
    // if logged call server for available dasboards for user
    // in other case return defaults as is

    cookieValue = getCookie("session-token");
    if (cookieValue == null) {
        cookieValue = getCookie("session-id");
    }

    if (cookieValue != null) {
        // get dasboards from server
        var ret = $.ajax({
            async: false,
            url: url_root + "api/v0/get_private_dashboards",
            beforeSend: function (xhr) {
                // authenticate the call 
                xhr.setRequestHeader ("Authorization", "Bearer " + cookieValue);
            },
            success: function(data) {
console.log(JSON.stringify(data));
                // var returnValue = jQuery.extend(true, {}, data);
                return data;
            },
            error: function() {
            }
        });

        if (ret['status'] == 200) {

            responseText = ret['responseText'];
            responseJson = JSON.parse(responseText);
            return responseJson;
        }
    }

    return null;

}
