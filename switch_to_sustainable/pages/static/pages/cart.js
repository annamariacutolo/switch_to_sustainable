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
                //updateUserOrder(e.target.dataset.product, e.target.dataset.action)
        }
        if (e.target.className == "quantity-down" | e.target.className == "fas fa-sort-down") {
            console.log('global listener button down')
            console.log(`target.id: ${e.target.dataset.product} action: ${e.target.dataset.action} `)
                //updateUserOrder(e.target.dataset.product, e.target.dataset.action)
        }
    }

});


var upButtons = document.getElementsByClassName('quantity-up');
for (var i = 0; i < upButtons.length; i++) {
    upButtons[i].addEventListener('click', function() {
        console.log('hi')

    });
}

/*
var updateButtons = document.getElementsByClassName('update-cart');

        for (var i = 0; i < updateButtons.length; i++) {
            if (user === 'AnonymousUser') {
                // updateButtons[i].addEventListener('click', messages.warning('Please log in to purchase.'));
                updateButtons[i].addEventListener('click', alert('Please log in to purchase.'), true);
            } else {
                updateButtons[i].addEventListener('click', function() {
                    var productId = this.dataset.product;
                    var action = this.dataset.action;
                    updateUserOrder(productId, action);
                }, true);
            }
        }
*/


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
        if (data.stock == 0) {
            location.reload()
        }
    })
}