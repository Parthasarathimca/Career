var custom_door_porion ;
var standard_door_porion ;
$("#custom_partition").click(function() {
       if (! standard_door_porion){
        standard_door_porion =$("#standard_door_content").detach();
       }
       $('#custom_door_content_parent').append(custom_door_porion);
   
       $(".custom_partition_section").removeClass("d-none");
       $(".standard_partition-block").addClass("d-none");
   });
   $("#standard_partition").click(function() {
       if(! custom_door_porion ){
       custom_door_porion =$("#custom_door_content").detach();
   }
       $('#standard_door_contnt_parent').append(standard_door_porion);
       $(".custom_partition_section").addClass("d-none");
       $(".standard_partition-block").removeClass("d-none");
   });

   $(".clear-btn").click(function(e) {
    $("input").val("");
    $("select").select2('val', "all");
    e.preventDefault();
});
$(document).ready(function() {
   $('#custom_door_content_parent').on('click', '.custom_door', function(){
       if ($(this).prop("checked") == true) {
           $(".colored_mirror").removeClass("d-none");
           $(".notes").removeClass("d-none");
       }
       else if ($(this).prop("checked") == false) {
           $(".colored_mirror").addClass("d-none");
           $(".notes").addClass("d-none");
       }
   });
   updateSetups();
     $('.custom_partition_radio').change(function() {
        if ($(this).prop("checked") == true) {
            if ($(this).val() == 1) {
                $(".custom_text").removeClass("d-none");
                $(".custom_standard").addClass("d-none");
            } else {
                $(".custom_standard").removeClass("d-none");
                $(".custom_text").addClass("d-none");

            }
        }
    });
   $("#room_"+default_room).attr("checked", "checked");
   
    custom_door_porion =$("#custom_door_content").detach();

});
clickCustom= ()=>{
   
   $("#custom_partition").trigger("click")
   if (isGlassDoor){
   $(".custom_door").trigger("click")
   }
}

updateSetups =() => {
   
   if(window.location.search.indexOf('room_item')==1){
      $("#submit_door").text('Update')
      $("#clear_door").text('cancel')
      if(partCategory =='STANDARD'){
      $("#opening_size_select").trigger("change");
      }
      else if (partCategory=='CUSTOM'){
         setTimeout(clickCustom, 20)
      }
   }
}

function sweetAlert(msg) {
    Swal.fire({
        text: msg,
        customClass: {
            confirmButton: 'btn btn-primary'
        }
    });
}

deleteDoorItem=(url,door_item_id)=>{
$.ajax({                       
         url: url,                  
         data: {},
         success: function (data) {
             Swal.fire({
                  title:    'Deleted!',
                  text: 'Your data has been deleted.',
                  icon:  'success',
                  customClass: {
                  confirmButton: 'btn btn-primary',            
                   },
                  }) 
         }
     });
}

$(document).on("click", ".del-data", function (e) {
let url=$(this).data('delete_url')
 Swal.fire({
     title: 'Are you sure?',
     text: "You won't be able to revert this!",
     icon: 'warning',
     showCancelButton: true,       
     customClass: {
         confirmButton: 'btn btn-primary',
         cancelButton: 'btn btn-secondary'
       },
     confirmButtonText: 'Yes, delete it!'
   }).then((result) => {
     if (result.isConfirmed) {
      deleteDoorItem(url)
     }
   })
 e.preventDefault();
});


// $(document).ready(function () {
//    $('.custom_door_2').click(function () {
//           $("#custom_door_2").prop("checked", true);
//            $(".door_tbody").addClass("d-none");
//            $(".custom_door_tbody").removeClass("d-none");
//            $(".room_section").addClass("d-none");
//            $(".custom_section ").removeClass("d-none");

//            $(".custom_section").removeClass("d-none");
//            $(".submit-button").attr("id", "submit_custom_door");
//            displayThead(false);
//        });
//        $('.standard_door2').click(function () {
//            $(".door_tbody").removeClass("d-none");
//            $(".custom_door_tbody").addClass("d-none");
//            $(".submit-button").attr("id", "submit_door");
//            $(".custom_section").addClass("d-none");
//            $(".custom_door_2").prop("checked", false);
//            $(".room_section").removeClass("d-none");
//            displayThead(true);
//        });
     
// });
function sweetAlert(msg) {
   Swal.fire({
       text: msg,
       customClass: {
           confirmButton: 'btn btn-primary'
       }
   });
}
// for dynamic lable based on room size selection 
$('#opening_size_select').on('change', function (e) {
var opening_size_option  = $("option:selected", this).data('vals');
alert(opening_size_option)
$("#door_opening_height_width").html(opening_size_option+"' Openings")
const url ="/classy/room/load_room_openigs/"+window.location.search
     const opening_size_id = $(this).val();

     $.ajax({                       
         url: url,                  
         data: {
             'opening_size_id': opening_size_id
         },
         success: function (data) { 
             $("#door_opening_height_width_select").html(data).trigger("change"); 
             
         }
     });


});

