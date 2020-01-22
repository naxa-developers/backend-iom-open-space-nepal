 $(document).ready(function() {
    var getUrl = window.location;
    var baseUrl = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[0];
    console.log('custom')
    //ajax request for district
$('.province_class').on('change',function(){
prov_id = $(this).val()
$.ajax({
    url: baseUrl+'api/v1/district_api?province_id='+prov_id,
//    headers: {
//        'Authorization': "Token 8933c5dd02de389ab5ee69c17a9af49f3d83b938",
//    },
    method: 'GET',
    success: function(result){

    console.log(result)
    var district = result.data
    $('.district_class').html("");
    for(var i = 0 ; i<district.length;i++){
    var prov_div="<option value="+district[i].id+">"+district[i].name+"</option>"
    $('.district_class').append(prov_div);
    }

    }});
    }); // end

//ajax request for mun
$('#id_district_id').on('change',function(){
dist_id = $(this).val()
$.ajax({
    url: baseUrl+'api/v1/core/gapanapa/?district_id='+dist_id,
//    headers: {
//        'Authorization': "Token 8933c5dd02de389ab5ee69c17a9af49f3d83b938",
//    },
    method: 'GET',
    success: function(result){



    $('#id_municipality_id').html("");
    var mun = result.results
    for(var i = 0 ; i<mun.length;i++){
    var prov_div="<option value="+mun[i].id+">"+mun[i].name+"</option>"
    $('#id_municipality_id').append(prov_div);
    }

    }});
    }); // end


    });