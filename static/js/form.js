$(document).ready(function() {
    $('select').material_select();
    $("select[required]").css({position: "absolute", display: "inline", height: 0, padding: 0, width: 0});
    
    document.getElementById("add-ingredient-btn").onclick = function() {
      var container = document.getElementById("field-section");
      var section = document.getElementById("form-field");
      container.appendChild(section.cloneNode(true));
    }
});