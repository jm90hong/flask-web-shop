$(document).ready(function(){
    initClickEvents();
});


function showPwWarn(flag){
    if(flag){
        $('.title-pw2').addClass('cred');
        $('.pw2-warn').show();
        $('#pw2').css('border','1px solid red');
    }else{
        $('.title-pw2').removeClass('cred');
        $('.pw2-warn').hide();
        $('#pw2').css('border','1px solid #dedede');
    }
}


function showUsernameWarn(flag){
    if(flag){
        $('.title-username').addClass('cred');
        $('.username-warn').show();
        $('#username').css('border','1px solid red');
    }else{

        $('.title-username').removeClass('cred');
        $('.username-warn').hide();
        $('#username').css('border','1px solid #dedede');


    }
}



function initClickEvents(){



    $('.pw2').on('keyup',function(){
        console.log('keyup');
        var pw1 = $('#pw1').val();
        var pw2 = $('#pw2').val();
        if(pw1==pw2){
            showPwWarn(false);
        }else{
            showPwWarn(true);
        }
    });




    //회원가입 버튼 클릭
    $('#submit-btn').click(function(){
        var name = $('#name').val();
        var pw1 = $('#pw1').val();
        var pw2 = $('#pw2').val();


        console.log(name);
        console.log(pw1);
        console.log(pw2);

        if(name.length>0 && pw1.length>1 && pw2.length>1){
            if(pw1==pw2){
                //회원가입 수행
                $.ajax({
                    url:'./addUser',
                    type:'get',
                    data:{
                        name:name,
                        pw:pw1
                    },
                    success:function(data){
                        if(data=='ok'){
                            showUsernameWarn(false);
                            alert('회원가입 완료. 홈에서 로그인해주세요.');
                            location.replace('./?canLogin=y');
                        }else if(data=='ex'){
                            showUsernameWarn(true);
                        }
                    },
                    error:function(err){

                    }
                })
            }else{
                alert('비밀번호가 일치하지 않습니다.')
            }
        }else{
            alert('모든 내용을 입력하세요');
        }

    });


}