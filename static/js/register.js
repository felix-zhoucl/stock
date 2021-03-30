$(function(){
     var usernameChecked=false;
     var emailChecked=false;
     var passwordChecked=false;
     var passwordChecked2=false;
     var agreementChecked=false;

//    用户名校验
     $('#id_username').blur(function(){
            var temp = $('#id_username').val();
            if(temp==''){
                $('#id_username').attr({class:"form-control input is-danger"});
                $('#id_username_error').text('用户名不能为空');
                $('#icon_username').attr({class:"fas fa-exclamation-triangle"});
            }
            else{
                $.ajax({
                    url:'/user/checkUsername',
                    type:'POST',
                    data:{username:temp},
                    success:function(arg){
    //                    var obj = arg
    //                    console.log(typeof arg)
                        var obj = jQuery.parseJSON(arg)
    //                    console.log(typeof obj)
                        if(obj.statuscode == 0){
                            $('#id_username').attr({class:"form-control input is-danger"});
                            $('#id_username_error').text('此用户名已存在');
                            $('#icon_username').attr({class:"fas fa-exclamation-triangle"});
                            usernameChecked=false;
                        }else{
                            $('#id_username').attr({class:"form-control input is-success"});
                            $('#id_username_error').text('');
                            $('#icon_username').attr({class:"fas fa-check"});
                            usernameChecked=true;
                        }
                    },
                    error:function(){
                        console.log('check username failed')
                    }
                });
            }
            checksubmitButton();
     });
//     邮箱地址合法性校验
     $('#id_email').blur(function(){
            var temp = $('#id_email').val();
            $.ajax({
                url:'/user/checkEmail',
                type:'POST',
                data:{email:temp},
                success:function(arg){
                    var obj = jQuery.parseJSON(arg)
                    if(obj.statuscode == 0){
                        $('#id_email').attr({class:"form-control input is-danger"})
                        $('#id_email_error').text('邮箱地址不合法');
                        $('#icon_email').attr({class:"fas fa-exclamation-triangle"});
                        emailChecked=false;
                    }else{
                        $('#id_email').attr({class:"form-control input is-success"});
                        $('#id_email_error').text('');
                        $('#icon_email').attr({class:"fas fa-check"})
                        emailChecked=true;
                    }
                },
                error:function(){
                    console.log('check email failed')
                }
            });
            checksubmitButton();
     });
//     密码规则校验
     $('#id_password1').blur(function(){
         var pass=$('#id_password1').val();
         var username = $('#id_username').val();
         $.ajax({
                url:'/user/checkPass',
                type:'POST',
                data:{pwd:pass,user:username},
                success:function(arg){
                    var obj = jQuery.parseJSON(arg)
                    if(obj.statuscode == 0){
                        $('#id_password1').attr({class:"form-control input is-danger"})
                        $('#id_password1_error').text(obj.errors.replace(/[\'\[\]\,]/g,''));
                        $('#icon_pass1').attr({class:"fas fa-exclamation-triangle"});
                        passwordChecked=false;
                    }else{
                        $('#id_password1').attr({class:"form-control input is-success"});
                        $('#id_password1_error').text('');
                        $('#icon_pass1').attr({class:"fas fa-check"})
                        passwordChecked=true;
                    }
                },
                error:function(){
                    console.log('check pass failed')
                }

            });
            checksubmitButton();
     });
//     确认密码
     $('#id_password2').blur(function(){
        var pass1=$('#id_password1').val();
        var pass2=$('#id_password2').val();
        if(pass1!=pass2)
		{
			$('#id_password2_error').text('两次输入的密码不一致');
			$('#id_password2').attr({class:"form-control input is-danger"})
			$('#icon_pass2').attr({class:"fas fa-exclamation-triangle"});
			passwordChecked2 = false;
		}
		else
		{
			$('#id_password2_error').text('');
			 $('#id_password2').attr({class:"form-control input is-success"});
			$('#icon_pass2').attr({class:"fas fa-check"})
			passwordChecked2 = true;
		}
		checksubmitButton();
     });
//     用户条款
     $('#agreement').click(function(){
        agreementChecked=$('#agreement').prop('checked');
        checksubmitButton();
        console.log('用户条款',agreementChecked);
     });

    function checksubmitButton(){
     if(usernameChecked == true && emailChecked == true && passwordChecked == true && passwordChecked2 == true && agreementChecked == true)
		{
			$('#submitButton').attr("disabled",false);
		}
	else
		{
			$('#submitButton').attr("disabled",true);
		}
     }

})
