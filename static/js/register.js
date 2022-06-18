$(document).ready(function(){
    initClickEvents();
});



function initClickEvents(){

    //회원가입 버튼 클릭
    $('#submit-btn').click(function(){
        var name = $('#name').val();
        var pw1 = $('#pw1').val();
        var pw2 = $('#pw2').val();

        if(name.length>0 && pw1.length>2 && pw2.length>2){
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
                            alert('회원가입 완. 홈에서 로그인해주세요.');
                            location.replace('./?canLogin=y');
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