document.addEventListener('click', function(e) {
    if (e.target.tagName == "BUTTON" && e.target.className == "update-cart") {
        if (user != 'AnonymousUser') {
            updateUserOrder(e.target.dataset.product, e.target.dataset.action)
        } else {
            alert('Please log in to add items to cart.')
        }
    }
    if (e.target.tagName == "BUTTON" | e.target.tagName == "I") {
        if (e.target.className == "quantity-up" | e.target.className == "fas fa-sort-up" | e.target.className == "quantity-down" | e.target.className == "fas fa-sort-down") {
            //console.log('global listener for buttons')
            updateUserOrder(e.target.dataset.product, e.target.dataset.action)
        }
    }
});


function updateUserOrder(productId, action) {
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
        console.log('data:', data.id);
        location.reload()
    })
}

