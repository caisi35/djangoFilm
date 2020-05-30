// function hits_book(book_id, user_id=null) {
//     if (user_id) {
//         // alert(book_id);
//         $.ajax({
//             url: hits_route,
//             type: 'post',
//             data: {
//                 'user_id': user_id,
//                 'book_id': book_id,
//                 csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
//             },
//             dataType: 'json',
//             success: function (data) {
//                 if (data.result) {
//                     $.ajax({
//                         url:detail_route,
//                         type: 'get',
//                         data: {'book_id': book_id},
//                         dataType: 'json',
//                         success: function (data) {
//                             alert(data.book)
//                         },
//                         error:function (data) {
//                             console.log('detail failed')
//                         }
//                     })
//                     // console.log('success')
//                 } else {
//                     console.log('hits failed')
//                 }
//             },
//             error: function (data) {
//                 console.log('操作失败，请重试！')
//                 }
//             })
//     }else {
//         // 没有用户id，去登录
//         window.location.href = login_route
//     }
// }


function hits_book(book_id, user_id=null) {
    if (user_id) {
        // alert(book_id);
        $.ajax({
            url: book_info,
            type: 'post',
            data: {
                'user_id': user_id,
                'book_id': book_id,
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
            },
            dataType: 'json',
            success: function (data) {
                if (data.result) {
                    console.log('success')
                } else {
                    console.log('hits failed')
                }
            },
            error: function (data) {
                console.log('操作失败，请重试！')
                }
            })
    }else {
        // 没有用户id，去登录
        window.location.href = login_route
    }
}