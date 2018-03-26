$(document).ready(function () {
    for (var i = 1; i < 21; i++) {
        var option = $('<option></option>').attr('value', i).text(i);
        $('.quantity').append(option);
    }

    $('button').click(function (e) {
        // e.preventDefault();
        var quantity = $(this).closest('tr').find('select.quantity').val();

        $(this).parent().find('input.q').val(quantity);
    })
})