$(document).ready(function () {

    $('.item-info').click(function () {
        var itemID = $(this).data('id');
        // console.log(itemID);
        $.ajax({
            url: '/detail',
            type: 'POST',
            data: { itemID: itemID },
            success: function (data) {
                // console.log(data);
                $('.modal-body').html(data);
                // $('.modal-body').append(data);
                $('#itemModal').modal('show');
            }
        });
    });

    $('#add-item').click(function () {
        $.ajax({
            url: '/form',
            type: 'POST',
            success: function (data) {
                $('.modal-form-body').html(data);
                $('#modal-form').modal('show');
                $('#img-file').change(function () {
                    var reader = new FileReader();
                    const img = $('#img');
                    reader.onload = function(e) {
                        // console.log(e.target);
                        $('#img').attr('src', e.target.result)
                    };
                    reader.readAsDataURL(this.files[0])
                });
            }
        });
    });

    $('.upload-btn').click(function () {
        item_name = $('#item_name').val();
        price = $('#price').val();
        category = $('#category').val();
        discount = $('#discount').val();
        quantity = $('#quantity').val();
        description = $('#description').val();
        img = $('#img').attr('src');
        if (item_name !== '' && price !== '' && category !== '' && discount !== '' && quantity !== '' && description !== '' && img !== '') {
            $.ajax({
                url: '/upload',
                type: 'POST',
                data: { item_name, price, category, discount, quantity, description, img },
                success: function (data) {
                    console.log('Upload ', data);
                    window.location.reload();
                },
                error: function (e) {
                    console.log(e);
                }
            });
        } else {
            console.log('No Data')
        }
    });

    // $('#cart_btn').click(function () {
    //     $.ajax({
    //         url: '/cart',
    //         type: 'POST',
    //         success: function (data) {
    //             console.log('cart ', data);
    //         },
    //         error: function (e) {
    //             console.log(e);
    //         }
    //     });
    // });

    
});