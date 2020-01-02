
    $(document).ready(function() {


        var map = L.map('map', {
                center: [28.3973623, 84.12576],
                zoom: 6,

            });

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

           var style = ({
                    fillColor: "green",
                    fillOpacity: 0.7,
                    weight: 2,
                    opacity: 0.2,
                    color: 'black',
                    dashArray: '5'
            });

            var style_open = ({
                    fillColor: "red",
                    fillOpacity: 0.8,
                    weight: 2,
                    opacity: 0.2,
                    color: 'black',
                    dashArray: ''
            });

             var url = 'http://localhost:8003/api/v1/municipality_geo_json?id=354';
                     var municipality = new L.geoJson.ajax(url, {

                        onEachFeature: function (feature, layer) {

                        }

                    });
                    municipality.on('data:loaded',function(){
                    map.addLayer(municipality)
                    municipality.setStyle(style);
                    map.fitBounds(municipality.getBounds(),{padding:[-50,-50]})
                    })

                    var url_open = 'http://localhost:8003/api/v1/single_open_geo_json?mun=354';
                     var open_space = new L.geoJson.ajax(url_open, {

                        onEachFeature: function (feature, layer) {

                        }

                    });
                    open_space.on('data:loaded',function(){
                    map.addLayer(open_space)
                    open_space.setStyle(style_open);
//                    map.fitBounds(municipality.getBounds(),{padding:[-50,-50]})
                    })

                    console.log(open_space)


    });//document end


