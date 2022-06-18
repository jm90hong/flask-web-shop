$(document).ready(function(){
    initClickEvents();
});





function initClickEvents(){
    $(document).on('click','.x',function(){
       $('.can-login-box').remove();
    })

   
    //로그인 페이지 이동
    $('#login-btn').click(function(){
        alert('로그인 수행')
    });
}