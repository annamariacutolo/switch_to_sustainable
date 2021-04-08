document.addEventListener('click', function(e) {
    if (e.target.tagName == "BUTTON" && e.target.className == "update-cart") {
        //console.log(`target.id: ${e.target.dataset.product} action: ${e.target.dataset.action} `)

        if (user != 'AnonymousUser') {
            updateUserOrder(e.target.dataset.product, e.target.dataset.action)
        } else {
            alert('Please log in to add items to cart.')
        }

    }
    // I added lines 14 to 26 for up and down buttons and info for cart.html for the i variables
    // The update user if uncommented should work for the backend too, but does not fix the reload problem
    if (e.target.tagName == "BUTTON" | e.target.tagName == "I") {

        if (e.target.className == "quantity-up" | e.target.className == "fas fa-sort-up") {
            console.log('global listener button up')
            console.log(`target.id: ${e.target.dataset.product} action: ${e.target.dataset.action} `)
            updateUserOrder(e.target.dataset.product, e.target.dataset.action)
                //location.reload()
        }
        if (e.target.className == "quantity-down" | e.target.className == "fas fa-sort-down") {
            console.log('global listener button down')
            console.log(`target.id: ${e.target.dataset.product} action: ${e.target.dataset.action} `)
            updateUserOrder(e.target.dataset.product, e.target.dataset.action)
                //location.reload()
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
        console.log('data:', data.id);
        location.reload()
    })
}

function processOrder(form) {
    console.log('order_complete');

    const url = '/process_order/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'form': form
        })
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data);
        alert('Transaction completed')
        window.location.href = "{% url '/' %}"
    })
}