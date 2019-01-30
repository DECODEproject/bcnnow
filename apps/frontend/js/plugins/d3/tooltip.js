d3.tooltip = function() {

    var frameOfReference,
        extent = new Array([[0,0],[960,500]]),
        tips = new Array([]),
        tipNames = new Array([]),
        tipFormats = new Array([]),
        margin = new Array([10,10]),
        padding = new Array([4,4]),
        translation = new Array([0,0]),
        tooltipDims =  new Array([0,0]),
        fontSize = 12;

    var tooltipGroup = d3.select(null),
        tooltipRect = d3.select(null),
        tooltipText = d3.select(null);
    
    var tooltip =  function(context) { 
 
        tooltipGroup.remove();

        frameOfReference = context.node()

        tooltipGroup = context.append("g")
            .classed("d3Tooltip",true)
            .style("display","none");

        tooltipRect = tooltipGroup.append("rect")
            .attr("width",100)
            .attr("height",100)
            .style("fill","black")
            .style("fill-opacity",.70)
            

        tooltipText = tooltipGroup.append("text")
            .style("fill", "white")
            .style("font-size",fontSize); 

    };

    function displayTooltip(d) {

        tooltipGroup.style("display",null);

        tooltipText.selectAll("tspan")
            .remove();

        tooltipText.attr("y", padding[1])
            .selectAll("tspan")
            .data(tips)
            .enter()
            .append("tspan")
            .attr("x",padding[0])
            .attr("dy",fontSize*.9)
            .text(function(e,i) { 
                var val;
                if (i==0) val = d.value;
                else val = d.count;
                /*if(typeof d[e] == 'undefined') {
                    // check the 'data' property too, for voronoi mouseover events
                    val = d.data[e];
                } else {
                    val = d[e];
                }
                if(tipFormats[i]) {
                    val = tipFormats[i](val);
                }*/
                return tipNames[i]  + val;
            });

        updateTooltipDims();

        tooltipRect.attr("width", tooltipDims[0])
            .attr("height", tooltipDims[1])

        updateTranslation();

        tooltipGroup.attr("transform","translate(" + translation[0] + "," + translation[1] + ")")
            
    }

    function hideTooltip() {

        tooltipGroup.style("display","none")

    }

    
    function moveTooltip() {

        updateTranslation();
        tooltipGroup.attr("transform","translate(" + translation[0] + "," + translation[1] + ")");
    }

    tooltip.events = function() {


        var me = d3.select(this).on("mouseenter") || function() {};
        var ml = d3.select(this).on("mouseleave") || function() {};
        var mm = d3.select(this).on("mousemove") || function() {};


        d3.select(this)
            .on("mouseenter", function(d,i) { me(d,i); displayTooltip(d,i);})
            .on("mouseleave", function(d,i) { ml(d,i); hideTooltip(d,i); })
            .on("mousemove", function(d,i) { mm(d,i); moveTooltip(d,i)});

    }

    tooltip.extent = function(_extent){

        extent = _extent || extent;
        return tooltip;

    }

    tooltip.fontSize  = function(_fontSize) {
        fontSize = _fontSize || fontSize;
        return tooltip;
    }


    tooltip.margin = function(_margin) {
        margin = _margin || margin;
        return tooltip;
    }

    tooltip.padding = function(_padding) {
        padding = _padding || padding;
        return tooltip;
    }

    tooltip.tips = function(_tips,_tipNames,_tipFormats) {

        tips = _tips || tips;
        tipNames = _tipNames || tips;
        tipFormats = _tipFormats || tips.map(function(d) { return null});
        return tooltip;

    }

    function updateTooltipDims() {
        var bb = tooltipText.node().getBBox();
        tooltipDims = [bb.width + padding[0]*2, bb.height + padding[1]*2];
    }

    function updateTranslation() {
        
        var mouseCoordinates = d3.mouse(frameOfReference);

        var quad = [0,0];
        
        if(mouseCoordinates[0] > (extent[1][0] - extent[0][0])/2) quad[0] = 1;
        if(mouseCoordinates[1] > (extent[1][1] - extent[0][1])/2) quad[1] = 1;

        if(quad[0] == 1) {
            translation[0] = mouseCoordinates[0] - tooltipDims[0] - margin[0];
        } else {
            translation[0] = mouseCoordinates[0] + margin[0];
        }

        if(quad[1] == 1) {
            translation[1] = mouseCoordinates[1] - tooltipDims[1] - margin[1];
        } else {
            translation[1] = mouseCoordinates[1] + margin[1];
        }
    }



    return tooltip; 
}
