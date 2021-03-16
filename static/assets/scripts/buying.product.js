$(document).ready(function () {

    $('#id_product').change(function (e) {
        $.get(
            '/backoffice/product/partition/formula/',
            {'product_pk': $(this).val()},
            function(data, status) {
                $('<p></p>').text(`${data.message}`).insertAfter('#id_product')
            }
        )
    })

    $('#id_quantity').keyup(function (e) {
        
    })

})