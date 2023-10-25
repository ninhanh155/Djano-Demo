var updateBtns = document.getElementsByClassName('update-cart')
for (i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('productID', productID, 'action', action)
        console.log('user :', user)
        if(user == "AnonymousUser")
        {
           console.log('chua dang nhap')
        }else{
            updateUserOrder(productID,action)

        }
    })
}


function updateUserOrder(productID, action){
    console.log ('Ban da dang nhap, success add')
    var url = '/update_item/'
    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrftoken ,
        },
        body: JSON.stringify({'productID':productID,'action':action})
    })
    .then((response) =>{ 
        return response.json()
    })
    .then((data) =>{ 
        console.log('data',data)
        location.reload()
    })

}
$('.plus-wishlist').click(function(){
    console.log('heloo')
    var id = $(this).attr('pid').toString();
    $.ajax({
        type : "GET",
        url : '/pluswishlist',
        data:{
            prod_id : id
        },
        success:function(data){
            console.log('data : ', data)
            location.reload()
        }
    })
})

$('.minus-wishlist').click(function(){
    var id = $(this).attr('pid').toString();
    $.ajax({
        type : "GET",
        url : '/minuswishlist',
        data:{
            prod_id : id
        },
        success:function(data){
            console.log('data : ', data)
            location.reload()
        }
    })
})