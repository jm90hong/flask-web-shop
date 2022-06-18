$(document).ready(function(){
    initClickEvents();
});





function initClickEvents(){
    $(document).on('click','.x',function(){
       $('.can-login-box').remove();
    })

   
    //로그인 페이지 이동
    $('#login-btn').click(function(){
        var name  = $('#name').val();
        var pw = $('#pw').val();


        if(name.length>0 && pw.length>0){   
            $.ajax({
                url:'./axlogin',
                tyep:'get',
                data:{
                    name:name,
                    pw:pw
                },
                success:function(data){
                    if(data=='ok'){
                        location.replace('./');
                    }else{
                        alert('계정정보가 일치 하지 않습니다.')
                    }
                },
                error:function(err){

                }
            })

        }else{
            alert('username, password를 입력하세요.')
        }
    });
}