// 验证是否已注册
$('#inputEmail3').focusout(function () {
    var email = document.getElementById('inputEmail3').value;

    if (email) {
        $.ajax({
            url: url_regit_sign,
            type: 'post',
            data: {'email': email, csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()},
            dataType: 'json',
            success: function (data) {
                // {#已存在#}
                if (data.result) {
                    var form = document.getElementsByClassName('form-horizontal');
                    $('<div>').appendTo(form).addClass('alert alert-warning text-center')
                        .html('此邮箱已被注册！').show().delay(3000).fadeOut();
                }
            },
            error: function (data) {
                console.log('操作失败，请重试！')
            }
        })
    }
});
// // 去注册
// $('#submit_btn').click(function () {
//     var email = document.getElementById('inputEmail3').value;
//     var name = document.getElementById('inputname3').value;
//     var password = document.getElementById('inputpassword').value;
//     var password2 = document.getElementById('inputpassword2').value;
//     var $form = $('#myform');
//
//     $.ajax({
//         url: register,
//         type: 'post',
//         data: {
//             'email': email, name: name, password: password, password2: password2,
//             csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
//         },
//         dataType: 'json',
//         success: function (data) {
//             // 注册成功
//             if (data.result) {
//                 // console.log(data.result);
//                 // window.location.href = login_route
//                 $form.attr('action',data.login_route);
//                 console.log($form.attr('action'));
//                 $form.submit()
//             } else {
//                 var form = document.getElementsByClassName('form-horizontal');
//                 $('<div>').appendTo(form).addClass('alert alert-warning text-center')
//                     .html('操作错误，请重试！').show().delay(5000).fadeOut();
//             }
//         },
//         error: function (data) {
//             console.log('操作失败，请重试！')
//         }
//     })
// });

// 验证两次密码
function confirm_password(){
    var p1 = document.getElementById('inputpassword').value;
    var p2 = document.getElementById('inputpassword2').value;
    if (p1 !== p2) {
        var form = document.getElementsByClassName('form-horizontal');
        $('<div>').appendTo(form).addClass('alert alert-warning text-center')
                    .html('两次输入密码不一致！').show().delay(5000).fadeOut();
    }
}
// # 去登录
$('#submit_login').click(function () {
    var email = document.getElementById('inputEmail').value;
    var password = document.getElementById('inputPassword').value;
    $.ajax({
        url: login_route,
        type: 'post',
        data: {
            'email': email, password: password, csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
        },
        dataType: 'json',
        async:false,
        success: function (result) {
            // 注册成功
            if (result.code === 1) {
                window.location.href = index_route
            } else {
                var form = document.getElementsByClassName('form-signin');
                $('<div>').appendTo(form).addClass('alert alert-warning text-center')
                    .html('邮箱或密码错误！').show().delay(5000).fadeOut();
            }
        },
        error: function (data) {
            console.log('操作失败，请重试！')
        }
    })
});