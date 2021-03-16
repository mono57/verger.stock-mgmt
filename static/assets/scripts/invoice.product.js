$(document).ready(function () {
    $('#id_drinks').change(function (e) {
        $.get(
            '/backoffice/drink/room/price/',
            {
                'drink_pk': $(this).val(),
                'room': $('#id_room').val()
            },
            function (data, status) {
                console.log(data)
                $('#id_price').val(data.price)
            }
        )
    });

    $('#id_dishs').change(function (e) {
        $.get(
            '/backoffice/dish/room/price/',
            {
                'dish_pk': $(this).val(),
                'room': $('#id_room').val()
            },
            function (data, status) {
                console.log(data.price)
                $('#id_price').val(data.price)
            }
        )
    })
});