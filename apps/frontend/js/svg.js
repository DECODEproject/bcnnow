/*
 * L.VectorIcon is a lightweight SVG-based icon class (as opposed to the image-based L.Icon)
 * to use with L.Marker
 * for you who love svg graphics :-)
 */

L.VectorIcon = L.Icon.extend({
	options: {
		iconSize: [12, 12], // also can be set through CSS
	  className: 'leaflet-vector-icon',
	  svgHeight: 64,
	  svgWidth: 64,
		viewBox: '0 0 64 64',
	  type: 'path', // 'path' | 'circle' | 'rect'
	  shape: {
	    d: 'M23.963,20.834L17.5,9.64c-0.825-1.429-2.175-1.429-3,0L8.037,20.834c-0.825,1.429-0.15,2.598,1.5,2.598h12.926C24.113,23.432,24.788,22.263,23.963,20.834z' // default path command
	  },
		style: {
			fill: '#333',
			stroke: '#000',
			strokeWidth: 1
		},
		text: ''
	},

	createIcon: function (oldIcon) {
		var div = (oldIcon && oldIcon.tagName === 'DIV') ? oldIcon : document.createElement('div'),
				svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg'),
				g = document.createElementNS('http://www.w3.org/2000/svg', 'g'),
				options = this.options,
				figure;

		svg.setAttributeNS(null, 'version', '1.1')
		svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
		svg.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");
		svg.setAttribute('height', options.svgHeight + '');
		svg.setAttribute('width', options.svgWidth + '');

		svg.style.marginTop = (options.svgHeight/2 - 6) * -1 + 'px';
		svg.style.marginLeft = (options.svgWidth/2 - 6) * -1 + 'px';

		if(options.type === 'path') {
			figure = document.createElementNS('http://www.w3.org/2000/svg', 'path');
			figure.setAttributeNS(null, 'd', options.shape.d);
		}
		else if(options.type === 'circle') {
			figure = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
			figure.setAttributeNS(null, 'cx', options.shape.cx);
			figure.setAttributeNS(null, 'cy', options.shape.cy);
			figure.setAttributeNS(null, 'r', options.shape.r);
		}
		else if(options.type === 'rect') {
			figure = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
			figure.setAttributeNS(null, 'x', options.shape.x);
			figure.setAttributeNS(null, 'y', options.shape.y);
			figure.setAttributeNS(null, 'width', options.shape.width);
			figure.setAttributeNS(null, 'height', options.shape.height);
		}
		else if(options.type === 'text') {
			figure = document.createElementNS('http://www.w3.org/2000/svg', 'text');
			figure.setAttributeNS(null, 'x', options.shape.x);
			figure.setAttributeNS(null, 'y', options.shape.y);
			figure.setAttributeNS(null, 'font-family', options.style.fontFamily || 'Arial');
			figure.setAttributeNS(null, 'font-style', options.style.fontStyle || 'normal');
			figure.setAttributeNS(null, 'font-variant', options.style.fontVariant || 'normal');
			figure.setAttributeNS(null, 'font-weight', options.style.fontWeight || 'normal');
			figure.setAttributeNS(null, 'font-size', options.style.fontSize || '12');
			figure.setAttributeNS(null, 'text-anchor', options.style.textAnchor || 'middle');
			figure.setAttributeNS(null, 'text-decoration', options.style.textDecoration || 'none');
			figure.setAttributeNS(null, 'text-rendering', options.style.textRendering || 'auto');
			figure.innerHTML = options.text;
		}
		else {
			console.log('Error: defined type of svg shape is invalid.');
		}

		figure.setAttributeNS(null, 'stroke', options.style.stroke || 'none');
		figure.setAttributeNS(null, 'stroke-width', options.style.strokeWidth);
		figure.setAttributeNS(null, 'fill', options.style.fill || 'none');

		g.appendChild(figure);
		svg.appendChild(g);
		div.appendChild(svg);

		if (options.bgPos) {
			var bgPos = L.point(options.bgPos);
			div.style.backgroundPosition = (-bgPos.x) + 'px ' + (-bgPos.y) + 'px';
		}
		this._setIconStyles(div, 'icon');

		return div;
	},

	createShadow: function () {
		return null;
	}
});

L.vectorIcon = function (options) {
	return new L.VectorIcon(options);
};