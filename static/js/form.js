$(document).ready(function() {
    // Show validation message on material select dropdown
    $('select').material_select();
    $("select[required]").css({
        position: "absolute",
        display: "inline",
        height: 0,
        padding: 0,
        width: 0
    });

    // Add Ingredient Button
    $("#add-ingredient-btn").click(function() {
        $("#form-field:last").append(getHtml());
    });

    function getHtml() {
        return '<div class="input-field">\
        <input type="text" class="validate" id="ingredient" name="ingredient" required />\
        <label for="ingredient">Ingredient (e.g. 100g Flour)</label>\
        </div>';
    }
    
    // RemoveIngredient Button
    $("#remove-ingredient-btn").click(function(){
      $("#form-field").children("div:last").remove()
    }) 
});