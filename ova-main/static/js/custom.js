$(".hideme").hide();
$(document).ready(function(){
  $(".switchToggle input").on("change", function(e) {
    const isOn = e.currentTarget.checked;
    
    if (isOn) {
      $(".hideme").show('slow');
     
    } else {
      $(".hideme").hide();
    }
  });
});
$(".hideme_apex").hide();
$(document).ready(function(){
  $(".switchToggle_apex input").on("change", function(e) {
    const isOn = e.currentTarget.checked;
    
    if (isOn) {
      $(".hideme_apex").show("slow");
     
    } else {
      $(".hideme_apex").hide();
    }
  });
});