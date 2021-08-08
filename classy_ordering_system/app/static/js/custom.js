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
            
        },
        error:function(data){
            //do something on error
        }
      });
     
});
    

