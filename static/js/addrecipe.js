$(".remove").click(function(){
        $(this).parent().parent().remove()
        Materialize.Toast.removeAll();
    })

/* Allows the buttons to add another ingredient line and remove one if needed */
$("#addingredient").click(function(){
    $("#break1").before('<div><div class="input-field col s10 m8 l6 offset-m1 offset-l2"><input name="ingredients" type="text" class="validate required"></div><div class="col center-align s2"><a class="btn-floating btn-small waves-effect waves-light red remove"><i class="material-icons">remove</i></a></div></div>');
    $(".remove").click(function(){
        $(this).parent().parent().remove()
    })
    $(document).ready(function(){
    $('.tooltipped').tooltip({delay: 50});
  });
});

/* Allows the buttons to add another method line and remove one if needed */
$("#addmethod").click(function () {
    $("#break2").before('<div><div class="input-field col s10 m8 l6 offset-m1 offset-l2"><textarea name="method" type="text" class="materialize-textarea" required></textarea></div><div class="center-align col s2"><a class="btn-floating btn-small waves-effect waves-light red remove"><i class="material-icons">remove</i></a></div></div>');
    $(".remove").click(function(){
        $(this).parent().parent().remove()
    })
    $(document).ready(function(){
    $('.tooltipped').tooltip({delay: 50});
  });
});