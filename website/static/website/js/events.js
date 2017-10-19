jQuery(function($) {
    $(document).ready(function() {
        // Search for lat-long coordinates of the given location
        $.ajax({
            url: "https://maps.google.com/maps/api/geocode/json",
            dataType: "json",
            crossDomain: true,
            data: {
                "address": $('#occurrence-location').text(),
                "sensor": "false"
            },
            success: function(data) {
                if(data.length == 0) {
                    return;
                }

                if(data.results.length == 0) {
                    return;
                }

                $('#event-map').css({
                    display: "block"
                });

                // Show a map on the event detail page
                var map = L.map('event-map').setView(
                    [
                        data.results[0].geometry.location.lat,
                        data.results[0].geometry.location.lng
                    ],
                    15
                );

                L.tileLayer(location.protocol + '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                    maxZoom: 18
                }).addTo(map);

                var marker = L.marker([
                    data.results[0].geometry.location.lat, 
                    data.results[0].geometry.location.lng
                ]).addTo(map);
            },
        });
    });
});
        
