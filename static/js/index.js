function hits_book(book_id, user_id) {
    if (user_id) {
        // alert(book_id);
        $.ajax({
            url: hits_route,
            type: 'post',
            data: {'user_id': user_id,'book_id': book_id, csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()},
            dataType: 'json',
            success: function (data) {
                if (data.result) {
                    console.log('success')
                } else {
                    console.log('failed')
                }
            },
            error: function (data) {
                // console.log('操作失败，请重试！')
            // }
        })
    }
}