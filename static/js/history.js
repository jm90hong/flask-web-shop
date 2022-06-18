$(document).ready(function(){

    init();

});





function init(){
    var username = $('#ss-username').val();
    $.ajax({
        url:ipAdress+'/getPuchaseListByUser',
        type:'get',
        data:{},
        success:function(list){
            $.each(list,function(i, item){
                var purchase_id=item[0];
                var name = item[7];
                var complete = item[5]
                var date = item[1];
                var count = item[4];
                completeHTML=''
                if(complete=='y'){
                    completeHTML='<span class="shipping-tag">shipping</span>';
                }

                $('#list-container').append(
                    '<div class="one-item-box-pc" style="height:94px;">'+
                        '<div style="display:flex;justify-content:space-between;padding-right:10px;">'+
                            
                            '<span>'+completeHTML+'purchased item : '+name+'</span>'+
                            '<span style="color:#999;">'+date+'</span>'+
                        '</div>'+
                        '<span>count : '+count+'</span>'+
                        '<span class="cancel-btn txt-btn" data-purchase-id='+purchase_id+'>Cancel</span>'+
                    '</div>'
                );
            })
        },
        error:function(err){

        }
    });

    $(document).on('click','.cancel-btn',function(){
        var test = confirm('정말 상품 구매를 취소 하시겠습니까?');
        if(test){
            var purchaseId = $(this).data('purchase-id');
            $.ajax({
                url:ipAdress+'/cancel/'+purchaseId,
                type:'get',
                data:{},
                success:function(data){
                    if(data=='ok'){
                        alert('주문 취소 완료');
                        location.reload();
                    }
                },
                error:function(err){
                    console.error(err);
                }

            })
        }
    });








}