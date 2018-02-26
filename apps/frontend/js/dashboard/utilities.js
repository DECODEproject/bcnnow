function getType(sources) {
        var value = 'static';
        sources.forEach(function(source, index){
            if(source['granularity'] != 'cumulative') {
                value = 'dynamic';
            }
        });
        return value;
    }

function getIcon(dataset, value) {
    var colors = dataset['colors'];
    var cuts = dataset['cuts'];
    var color = '#000000';

    cuts.forEach(function (cut, i) {
        if(cut < value) {
            color = colors[i];
        }
    });

    return L.vectorIcon({
              className: 'circle-icon',
              svgHeight: 32,
              svgWidth: 32,
              type: 'circle',
              shape: {
                r: '5',
                cx: '16',
                cy: '16'
              },
              style: {
                fill: color,
                stroke: color,
                strokeWidth: 1
              }
    });
}

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

function getArea(feature, dataset, obs) {
    var bordercolor = 'rgba(0,0,0,0)';
    var fillcolor = 'rgba(0,0,0,0)';
    obs.forEach(function(element) {
        if(titleCase(feature.properties.neighbourhood) == titleCase(element.id)) {
            fillcolor = getIcon(dataset, element.value);
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

function getLabel(feature, dataset, obs) {
        var result = null;
        obs.forEach(function(element) {
            if(titleCase(feature.properties.neighbourhood) == titleCase(element.id)) {
                result = element;
            }
        });
        return result;
    }