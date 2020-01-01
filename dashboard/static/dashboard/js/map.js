
    $(document).ready(function() {


        var map = L.map('map', {
                center: [28.3973623, 84.12576],
                zoom: 6,

            });

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

           var style = ({
                    fillColor: "red",
                    fillOpacity: 0.5,
                    weight: 2,
                    opacity: 0.2,
                    color: 'black',
                    dashArray: ''
            });

             var url = 'http://localhost:8003/api/v1/municipality_geo_json?id=2';
                     var municipality = new L.geoJson.ajax(url, {

                        onEachFeature: function (feature, layer) {

                        }

                    });
                    municipality.on('data:loaded',function(){
                    map.addLayer(municipality)
                    municipality.setStyle(style);
                    map.fitBounds(municipality.getBounds(),{padding:[-50,-50]})
                    })

                    var url = 'http://localhost:8003/api/v1/municipality_geo_json?id=2';
                     var municipality = new L.geoJson.ajax(url, {

                        onEachFeature: function (feature, layer) {

                        }

                    });
                    municipality.on('data:loaded',function(){
                    map.addLayer(municipality)
                    municipality.setStyle(style);
                    map.fitBounds(municipality.getBounds(),{padding:[-50,-50]})
                    })


    });//document end


