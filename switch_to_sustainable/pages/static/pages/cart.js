document.addEventListener('click', function(e) {
    if (e.target.tagName == "BUTTON" && e.target.className == "update-cart") {
        //console.log(`target.id: ${e.target.dataset.product} action: ${e.target.dataset.action} `)


        if (user != 'AnonymousUser') {
            updateUserOrder(e.target.dataset.product, e.target.dataset.action)
        } else {
            alert('Please log in to add items to cart.')
        }

    }
});


function updateUserOrder(productId, action) {
    console.log('logged in');

    const url = '/update_item/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        })
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
            //location.reload()
    })
}