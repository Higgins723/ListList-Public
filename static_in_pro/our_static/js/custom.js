function showFlashMessage(message){
  var template = "<div class='container container-alert-flash'><div class='col-sm-3 col-sm-offset-8'><div class='alert alert-success alert-dismissible' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>" + message + "</div></div></div>";
  $("body").append(template);
  $(".container-alert-flash").fadeIn();
  setTimeout(function(){
    $(".container-alert-flash").fadeOut();
  }, 1000);
}

//function to add comas to numbers
$.fn.digits = function(){
  return this.each(function(){
    $(this).text( $(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") );
  })
}
//apply function to all instances with class of numbers
$(document).ready(function() {
  $(".numbers").each(function() {
    $(this).digits();
  });
});
