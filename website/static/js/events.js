jQuery(function($) {
    $(document).ready(function() {
        // Search for lat-long coordinates of the given location
        $.ajax({
            url: location.protocol + "//nominatim.openstreetmap.org/search",
            dataType: "json",
            data: {
                "q": $('#occurrence-location').text(),
                "format": "json"
            },
            success: function(data) {
                if(data.length == 0) {
                    return 
                }

                $('#event-map').css({
                    display: "block"
                });

                // Show a map on the event detail page
                var map = L.map('event-map').setView([data[0].lat, data[0].lon],
                    15);
                L.tileLayer(location.protocol + '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                    maxZoom: 18
                }).addTo(map);

                var marker = L.marker([data[0].lat, data[0].lon]).addTo(map);
            },
        });
    });
});
        
