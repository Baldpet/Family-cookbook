/*$('.filter').submit(function(){
    ingredient = $(this).attr("id");
    $('.recipe').addClass('display-none');
    $("." + ingredient).removeClass('display-none');
    $("." + mainIngredient).removeClass('display-none');
})*/

$('.filter').click(function(){
    let values = $('form').serializeArray()
    let mainIngredient = values[0].value
    let recipeName = values[1].value

    if (mainIngredient === 'none'){
        $('.recipe').removeClass('display-none');
    } else {
        $('.recipe').addClass('display-none');
        $("." + mainIngredient).parent().parent().parent().removeClass('display-none');
        
    }
    console.log(values)
    console.log(mainIngredient)
    console.log(recipeName)
})