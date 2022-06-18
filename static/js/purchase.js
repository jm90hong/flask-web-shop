$(document).ready(function(){
    
    initClickEvents();
});





function initClickEvents(){
    $('#final-purchase-btn').click(function(){
        var count = $("#count").val();
        var itemId = $("#item-id").val();
        var test  = confirm('정말 구매하시겠습니까?');
        if(test){
            if(count.length>0){
                $.ajax({
                    url:'./addPurchase',
                    type:'get',
                    data:{
                        count:count,
                        itemid:itemId
                    },
                    success:function(data){
                        if(data=='ok'){
                            alert('구매완료');

                        }
                    },
                    error:function(err){

                    }
                })
            }else{
                alert('Please fill out this field');
            }
        }
       
    })
}