function clearData(){
    $("form input.form-control, form textarea").val("");        
    $('form select').val("0").trigger('change'); 
    $("form input").prop('checked', false);   
}

$(".clear-btn").click(function (e) {
    clearData();
    e.preventDefault();
});


function sweetAlert(msg) {
  Swal.fire({
      text: msg,
      customClass: {
          confirmButton: 'btn btn-primary'
      }
  });
}


$("#feed-btn").click(function(){  
    $(".feedback-card").toggleClass("open");
});

$("#feed-close").click(function(){
    
    $(".feedback-card").removeClass("open");
});


// $(document).on("click", "#sendFeedback", function(){
//     $(".feedback-card").removeClass("open");
//     Swal.fire({
//         icon: 'success',
//         title: 'Thank You!',
//         text: 'Your submission has been sent',        
//         customClass: {
//             confirmButton: 'btn btn-primary'
//         }
//       });

// })

$(".buttons-type-list button").click(function (e) {
    e.preventDefault();
    $(".buttons-type-list button").removeClass("active");
    $(this).addClass("active");   
})



$('body').on('click',"#sendFeedback",function(event) {
    event.preventDefault();
    url = $(this).data('action')
    post_data= $("#feedback_form").serializeArray()
    page=$(".breadcrumb-separatorless li:last").text();
    post_data.push({name:'page',value:page});
    $.ajax({
        type: "POST",
        url: url,
        data: post_data , // serializes the form's elements.
        success: function(data){
            data=JSON.parse(data)
            if(data['status']==201){
                $(".feedback-card").removeClass("open");
                Swal.fire({
                    icon: 'success',
                    title: 'Thank You!',
                    text: 'Your submission has been sent',        
                    customClass: {
                        confirmButton: 'btn btn-primary'
                    }
                  });

            }
        clearData();
        e.preventDefault();
            
        },
        error:function(data){
            //do something on error
            clearData();
            e.preventDefault();
        }
      });
     
});
$(".buttons-type-list button").click(function (e) {
    e.preventDefault();
    $(".buttons-type-list button").removeClass("active");
    $(this).addClass("active");   
})

$(".confirm-opn").click(function(e){
    $('.confirm-opn').addClass("btn-secondary");
    e.preventDefault();
    var getHref = $(this).attr("href");
    Swal.fire({           
        text: 'Are you sure you wish to Create a New inventory order?',         
        showCancelButton: true,       
        customClass: {
            confirmButton: 'btn btn-primary',
            cancelButton: 'btn btn-secondary'
        },
        confirmButtonText: 'YES',
        cancelButtonText: 'NO',
    }).then((result) => {
            if (result.isConfirmed) {
                $(this).removeClass("btn-secondary");
                $(this).addClass("btn-primary continue");
                $('#CreateJob_form .inventory-calender').removeClass("cal-disabled");
                // window.location = getHref
            }
          })
});

try{
// Inventory Datepicker
new Lightpick({
    field: document.getElementById('inventory-date'),
    inline: true,
    minDate: moment().startOf('today'),
    // disableDates:[moment().startOf(''), ['2018-06-23', '2018-06-30']],
    onSelect: function(date){
      //   document.getElementById('result-13').innerHTML = date.format('Do MMMM YYYY');
      $("#createJob").removeAttr("disabled");
    }
});
}
catch(err) {
    console.log(err)
}



$('#createJob').click(function(){
    var gethref = $('.continue').data("href");
    window.location.href = gethref;
});
    

