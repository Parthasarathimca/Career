// Wait for the DOM to be ready
$(document).ready(function(){
  // Initialize form validation on the registration form.
  // It has the name attribute "registration"
  $("#create-partition-form").validate({
    // Specify validation rules
    rules: {
      // The key name on the left side is the name attribute
      // of an input field. Validation rules are defined
      // on the right side
      quantity: "required",
    },
    // // Specify validation error messages
    messages: {
      quantity: "Please enter your firstname",
     },
    // // Make sure the form is submitted to the destination defined
    // // in the "action" attribute of the form when valid
    submitHandler: function(form) {
      form.submit();
      console.log("Hewllo");
     }

  });
});
