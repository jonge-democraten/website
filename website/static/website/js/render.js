// Test for SVG-support
console.log('ready');

var afdColors = {
    "Amsterdam": "#faa61a",
    "Leiden-Haaglanden": "#cddc38",
    "Rotterdam": "#5f7e8c",
    "Utrecht": "#009789",
    "Brabant": "#ef4481",
    "Arnhem-Nijmegen": "#98c93c",
    "Limburg": "#37a5dd",
    "Overijssel": "#903f98",
    "Groningen": "#4555a5",
    "Friesland": "#f05355"
};


function drawMap() {

    $("#afdelingskaart svg").remove();

    if (!document.createElementNS || !document.createElementNS('http://www.w3.org/2000/svg', 'svg').createSVGRect) {
        var err = '<strong>Je browser bevat helaas geen ondersteuning voor SVG, dat is vereist voor weergave van de kaart. Probeer je browser te upgraden, of gebruik een andere (nieuwere) webbrowser.</strong>';
        document.getElementById('afdelingskaart').innerHTML = err;
        return;
    }

    var r = 1.28;

    var width = d3.select('#afdelingskaart').style('width').split('px')[0];
    var height = Math.ceil(width * r);
    if (width < 600)
        d3.select('#afdelingskaart').style('padding-top','95px');
    scale = Math.floor(width * 25.16);



    var projection = d3.geo.albers()
        .center([5.25, 52.2])
        .rotate([0, 0])
        .parallels([50, 60])
        .scale(scale)
        .translate([width/2, height/2]);

    var mappath = d3.geo.path()
        .projection(projection);
    var graticule = d3.geo.graticule();

    var svg = d3.select("#afdelingskaart").append("svg")
        .attr("width", width)
        .attr("height", height);

    svg.append("path")
        .datum(graticule)
        .attr("class", "graticule")
        .attr("d", mappath);

    svg.append("path")
        .datum(graticule.outline)
        .attr("class", "graticule outline")
        .attr("d", mappath);

    queue()
        .defer(d3.json, "/static/website/json/gemeenten_2013.topo.json")
        .defer(d3.json, "/static/website/json/afdelingen.json")
        .await(ready);

    function ready(error, nl, afdelingen) {
        var afdById = {};

        for(var afd in afdelingen) {
            afdelingen[afd].forEach(function(d) {
                afdById[d] = afd;
            });
        }

        var getAfdeling = function(gm_code) {
            var gid = parseInt(gm_code.split('GM')[1],10);
            var a = afdById[gid];
            if (typeof a == 'undefined')
                return '';
            return a;
        };

        var gemeentes = topojson.object(nl, nl.objects.gemeenten_2013).geometries;

        svg.selectAll(".gemeente")
            .data(gemeentes)
            .enter().insert("path", ".graticule")
                .attr("class", "gemeente")
                .attr("d", mappath)
                .attr("id", function(d) { return d.id; })
                .on("mouseover", function(d, i) {
                    d3.select("#selected-gemeente").text(d.properties.name);
                    var a = getAfdeling(d.id);
                    if (a != '') {
                        d3.select(".infobox h2").text(a);
                        d3.select(".infobox").style('background', afdColors[a]);
                    } else {
                        d3.select(".infobox h2").html('<i>Niet ingedeeld</i>');
                        d3.select(".infobox").style('background', null);
                    }
                })
                .on("click", function(d, i) {
                    var a = getAfdeling(d.id);
                    if (a != '')
                        window.location.href = a;
                })
                .style("fill", function(d, i) {
                    var a = getAfdeling(d.id);
                    if (a != '')
                        return afdColors[a];
                });

        //drawMarker({'latitude':52.633,'longitude':7.042});
    }
}


$(window).resize(function() {
    drawMap();
});

drawMarker = function (message) {
    var latitude = message.latitude,
        longitude = message.longitude,
        text = message.title,
        city = message.city,
        x, y;

    var mapCoords = this.geoCoordsToMapCoords(latitude, longitude);
        x = mapCoords.x;
        y = mapCoords.y;

	svg.append('svg:circle')
        	.attr("r", 2)
	        .style("fill", "steelblue")
        	.attr("cx", x)
	        .attr("cy", y);
}

geoCoordsToMapCoords = function (latitude, longitude) {
        latitude = parseFloat(latitude);
        longitude = parseFloat(longitude);

        var mapWidth = width,
            mapHeight = height,
            x, y, mapOffsetX, mapOffsetY;

        x = (mapWidth * (180 + longitude) / 360) % mapWidth;

        latitude = latitude * Math.PI / 180;
        y = Math.log(Math.tan((latitude / 2) + (Math.PI / 4)));
        y = (mapHeight / 2) - (mapWidth * y / (2 * Math.PI));

        mapOffsetX = mapWidth * 0.082;
        mapOffsetY = mapHeight * 0.078;

        return {
            x: (x - mapOffsetX),
            y: (y + mapOffsetY),
            xRaw: x,
            yRaw: y
        };
}
