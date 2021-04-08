function show_new_product_list(products) {
    const product_list_element = document.getElementById('products');

    if (products.length == 0) {
        product_list_element.innerHTML = '<p>No products found.</p>'
    } else {
        let product_list_items = '';
        products.forEach(function(product) {
            product_list_items += '<li>' + product.name +
                '<ul> ' +
                '<li>' + product.description + '</li>' +
                '<li>£' + (product.price).toFixed(2) + '</li>' + '<br>' +
                '<button type="submit" class="update-cart" data-product="' +
                product.id + '" data-action="add">Add to cart</button>' +
                '</ul>' +
                '</li>'

        });
        product_list_element.innerHTML = '<ul>\n' + product_list_items + '</ul>\n'
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
    }
}


function update_product_list(item_id) {
    if (item_id < 0) {
        show_new_product_list([])
    } else {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/api/product?item_id=" + item_id.toString());

        xhr.onload = function(evt) {
            if (this.status == 200) {
                var products = JSON.parse(this.responseText);
                show_new_product_list(products);
            } else {
                show_new_product_list([])
            }
        }

        xhr.send();
    }
}


window.onload = (event) => {
    const dropdown = document.getElementById('item_id');
    dropdown.onchange = function() {
        const item_id = dropdown.options[dropdown.selectedIndex].value;
        update_product_list(item_id);
    }
}