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
        console.log('data:', data)
            //location.reload()
    })
}