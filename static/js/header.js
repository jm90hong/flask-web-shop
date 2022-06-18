const ipAdress='http://127.0.0.1:5000';

$(document).ready(function(){
    $('.go-main').click(function(){
        location.href=ipAdress
    }); 


    $('.go-history').click(function(){
        var username = $('#ss-username').val();
        location.href=ipAdress+'/users/'+username;
    });

    
    $('#logout-btn').click(function(){
        var test = confirm('정말 로그아웃 하시겠습니까?1');
        if(test){
            $.ajax({
                url:ipAdress+'/auth/logout',
                type:'get',
                data:{},
                success:function(data){
                    if(data=='ok'){
                        location.replace(ipAdress);
                    }
                },
                error:function(err){

                }
            })
        }
    });

})