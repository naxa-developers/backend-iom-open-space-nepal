
    $(document).ready(function() {
        console.log(group)
        console.log(mun_id)
        var getUrl = window.location;
        var baseUrl = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[0];

        if(group == 'super_admin' ){

        var url = baseUrl+'api/v1/municipality_geo_json?'+mun_id;
        var url_open = baseUrl+'api/v1/open_space_geo_json';

        }else{

        var url = baseUrl+'api/v1/municipality_geo_json?id=354';
        var url_open = baseUrl+'api/v1/single_open_geo_json?mun='+mun_id;


        }


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
                    dashArray: '5'
            });

            var style_open = ({
                    fillColor: "#66fc03",
                    fillOpacity: 0.9,
                    weight: 3,
                    opacity: 0.4,
                    color: 'black',
                    dashArray: ''
            });

//             var url = baseUrl+'api/v1/municipality_geo_json?id=354';
                     var municipality = new L.geoJson.ajax(url, {

                        onEachFeature: function (feature, layer) {

                        }

                    });
                    municipality.on('data:loaded',function(){
                    map.addLayer(municipality)
                    municipality.setStyle(style);
//                    map.fitBounds(municipality.getBounds(),{padding:[-50,-50]})
                    })

//                    var url_open = baseUrl+'api/v1/single_open_geo_json?mun=354';
                     var open_space = new L.geoJson.ajax(url_open, {

                        onEachFeature: function (feature, layer) {

                        }

                    });
                    open_space.on('data:loaded',function(){
                    map.addLayer(open_space)
                    open_space.setStyle(style_open);
                    map.fitBounds(open_space.getBounds(),{padding:[-50,-50]})
                    })

                    console.log(open_space)


    });//document end


