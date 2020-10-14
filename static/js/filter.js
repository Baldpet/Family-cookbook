/* Code taken from Stack Overflow */
/* Creates the new function icontains that is not case sensitive */
jQuery.expr[':'].icontains = function(a, i, m) {
  return jQuery(a).text().toUpperCase()
      .indexOf(m[3].toUpperCase()) >= 0;
};

/* End of code taken from Stack Overflow */

$('.filter').click(function(){
    let values = $('form').serializeArray();
    let mainIngredient = values[0].value;
    let recipeName = values[1].value;
    let search = "h5:icontains(" + recipeName + ")";
    if (mainIngredient === 'none' && recipeName == ""){
        $('.recipe').removeClass('display-none');
    } else if (mainIngredient === 'none'){
        $('.recipe').addClass('display-none');
        $(search).parent().parent().parent().parent().parent().removeClass('display-none');
    } else if (recipeName == ""){
        $('.recipe').addClass('display-none');
        $("." + mainIngredient).parent().parent().parent().removeClass('display-none');
    } else {
        $('.recipe').addClass('display-none');
        $(search).parent().parent().parent().parent().parent().addClass('visible');
        $("." + mainIngredient).parent().parent().parent().addClass('ingre-visible');
        $('.visible.ingre-visible').removeClass('display-none');
        
        $('.recipe').removeClass('visible');
        $('.recipe').removeClass('ingre-visible');
        $(search).parent().parent().parent().parent().parent().removeClass('visible');
    }
});