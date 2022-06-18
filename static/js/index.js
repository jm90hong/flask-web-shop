$(document).ready(function(){
   
    loadData();
    initClickEvents();
});



function loadData(){
    //리스트 불러오기
    var auth = $('#ss-auth').val()
    if(auth=='c'){
        $.ajax({
            url:'./getItemList',
            type:'get',
            data:{},
            success:function(list){
                
                $.each(list,function(i,item){
                    $('#list-container').append(
                        '<div class="one-item-box-pc">'+
                        
                            '<div><span style="margin-right:10px">item name : </span>'+
                            '<span>'+item[1]+'</span></div>'+
                            '<span class="purchase-btn txt-btn" data-item-id='+item[0]+'>Puchase</span>'+
                        '</div>'
    
                    )
                })
            },
            error:function(err){
                console.error(err);
            }
    
        })
    }else if(auth=='a'){
        $.ajax({
            url:'./getItemList',
            type:'get',
            data:{},
            success:function(list){
                
                $.each(list,function(i,item){
                    $('#list-container').append(
                        '<div class="one-item-box-pc">'+
                        
                            '<div>'+
                                '<span style="margin-right:10px">item name : </span>'+
                                '<span>'+item[1]+'</span>'+
                            '</div>'+
                            '<div>'+
                                '<span class="remove-btn txt-btn" data-item-id='+item[0]+'>Remove</span>'+
                                ' | '+
                                '<span class="complete-btn txt-btn" data-item-id='+item[0]+'>Complete</span>'+
                            '</div>'+
                        '</div>'
    
                    )
                })
            },
            error:function(err){
                console.error(err);
            }
    
        })
    }else {
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
   
}

function initClickEvents(){
    $(document).on('click','.x',function(){
       location.replace('./');
    })

    //상품 삭제
    $(document).on('click','.remove-btn',function(){
        var test =confirm('해당 상품을 삭제 하시겠습니까?');
        if(test){
            var item_id = $(this).data('item-id');
            $.ajax({
                url:'./remove/'+item_id,
                type:'get',
                data:{},
                success:function(data){
                    if(data=='ok'){
                        alert('상품 삭제 완료');
                        location.reload();
                    }
                },
                error:function(err){
                    console.error(err);
                }
            })
        }
    });


    //배송 완료 처리
    $(document).on('click','.complete-btn',function(){
        var test =confirm('해당 상품을 배송 처리 하시겠습니까?');
        if(test){
            var item_id = $(this).data('item-id');
            $.ajax({
                url:'./complete/'+item_id,
                type:'get',
                data:{},
                success:function(data){
                    if(data=='ok'){
                        alert('상품 배송 처리완료');
                        location.reload();
                    }else if(data=='fail'){
                        alert('주문한 상품이 없습니다.');
                    }
                },
                error:function(err){
                    console.error(err);
                }
            })
        }
    });


    $('#add-item-btn').click(function(){
        var itemName = $('#item-name').val();
        if(itemName.length>0){
            $.ajax({
                url:'./add',
                type:'get',
                data:{
                    name:itemName
                },
                success:function(data){
                    if(data=='ok'){
                        alert('상품 추가 완료');
                        location.reload();
                    }
                },
                error:function(err){
    
                }
            })
        }else{
            alert('item name must be filled')
        }
        
    });


    $(document).on('click','.purchase-btn',function(){
        var test = confirm('구매하시겠습니까?');
        var itemId = $(this).data('item-id');
        if(test){
            location.href='./purchase/'+itemId;

        }
    });

    //회원가입 이동
    $('#go-register-btn').click(function(){
        location.href='./register';
    });


    //로그인 페이지 이동
    $('#go-login-btn').click(function(){
        location.href='./login';
    });


}