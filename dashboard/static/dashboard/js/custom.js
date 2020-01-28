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

//    console.log(result)
    var district = result.data
    $('.district_class').html("");
    for(var i = 0 ; i<district.length;i++){
    var prov_div="<option value="+district[i].id+">"+district[i].name+"</option>"
    $('.district_class').append(prov_div);
    }

    }});
    }); // end

//ajax request for mun
$('.district_class').on('change',function(){
dist_id = $(this).val()
$.ajax({
    url: baseUrl+'api/v1/municipality_api?district_id='+dist_id,
//    headers: {
//        'Authorization': "Token 8933c5dd02de389ab5ee69c17a9af49f3d83b938",
//    },
    method: 'GET',
    success: function(result){


//    console.log(result)
    $('.mun_class').html("");
    var mun = result.data
    for(var i = 0 ; i<mun.length;i++){
    var prov_div="<option value="+mun[i].id+">"+mun[i].name+"</option>"
    $('.mun_class').append(prov_div);
    }

    }});
    }); // end


form_num = 1;
 $('#add_form').on('click', function () {
    var gallery_form = "";
    gallery_form += '<div id="gallery_form'+form_num+'" class="card gallery_image_form">'+
                    '<div class="card-body">'+
                    '<a href="javascript:void(0);" id="remove_form" data-id="'+form_num+'" style="margin-left: 568px;" ><button type="button" class=" btn-outline-danger">Remove <i class="la la-minus-circle"></i></button></a>'+
                    '<div class="form-group">'+
                        '<label for="id_type">Type</label>'+
                       '<div class="select-option">'+
                            '<select class="custom-select show-tick ms select2" name="type" id="id_type">'+


                                    '<option value="map">Map</option>'+

                                    '<option value="image">Image</option>'+


                            '</select>'+
                        '</div>'+
                    '</div>'+

                  '<p><label for="id_image">Image:</label>'+
                    '<input class="form-control" id="id_image" name="image" type="file">'+
                     '</div>'+
                    '</div>';

                    console.log(gallery_form);
                    form_num++
                    $('#gallery_image_div').append(gallery_form)






    });

    $('#gallery_image_div').on('click', '#remove_form', function () {
        id=$(this).attr("data-id")
        $( '#gallery_form'+id ).remove();


 })


    });// document end