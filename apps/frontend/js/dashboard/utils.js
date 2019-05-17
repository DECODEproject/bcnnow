    /*****************************************************************************************************************
                                                        UTILS
    ******************************************************************************************************************/


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

/*
    Generate UUID 
*/
function create_UUID(){
    var dt = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (dt + Math.random()*16)%16 | 0;
        dt = Math.floor(dt/16);
        return (c=='x' ? r :(r&0x3|0x8)).toString(16);
    });
    return uuid;
}

/*
    Checks whether at least one source inside the widget needs to be displayed along time
    @sources The list of sources inside a widget
    @return Returns "dynamic" if at least one source needs to be displayed along time, otherwise "static"
*/
function getType(sources) {
    var value = 'static';
    sources.forEach(function(source, index) {
        if (source['granularity'] != 'cumulative') {
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

    cuts.forEach(function(cut, i) {
        if (cut < value) {
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
        if (titleCase(feature.properties.neighbourhood) == titleCase(element.id)) {
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
        if (titleCase(feature.properties.neighbourhood) == titleCase(element.id)) {
            result = element;
        }
    });
    return result;
}
