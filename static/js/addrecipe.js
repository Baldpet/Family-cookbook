
/* Allows the buttons to add another ingredient line and remove one if needed */
$("#addingredient").click(function(){
    $("#break1").before('<div><div class="input-field col s10"><input name="ingredients" type="text" class="validate required"></div><div class=" col s2"><a class="btn-floating btn-small waves-effect waves-light red remove"><i class="material-icons">remove</i></a></div></div>');
    $(".remove").click(function(){
        $(this).parent().parent().remove()
    })
});

/* Allows the buttons to add another method line and remove one if needed */
$("#addmethod").click(function () {
    $("#break2").before('<div><div class="input-field col s10"><textarea name="method" type="text" class="materialize-textarea" required></textarea></div><div class=" col s2"><a class="btn-floating btn-small waves-effect waves-light red remove"><i class="material-icons">remove</i></a></div></div>');
    $(".remove").click(function(){
        $(this).parent().parent().remove()
    })
});