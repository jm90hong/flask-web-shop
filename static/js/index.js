$(document).ready(function(){
   
    loadData();
    initClickEvents();
});



function loadData(){
    //리스트 불러오기
    $.ajax({
        url:'./getItemList',
        type:'get',
        data:{},
        success:function(list){
            
            $.each(list,function(i,item){
                $('#list-container').append(
                    '<div class="one-item-box">'+
                        '<span style="margin-right:10px">item name : </span>'+
                        '<span>'+item[1]+'</span>'+
                    '</div>'

                )
            })
        },
        error:function(err){
            console.error(err);
        }

    })
}

function initClickEvents(){
    $(document).on('click','.x',function(){
       location.replace('./');
    })

    //회원가입 이동
    $('#go-register-btn').click(function(){
        location.href='./register';
    });


    //로그인 페이지 이동
    $('#go-login-btn').click(function(){
        location.href='./login';
    });


}