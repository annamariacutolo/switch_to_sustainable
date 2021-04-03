function show_new_product_list(products) {
    const product_list_element = document.getElementById('products');

    if (products.length == 0) {
        product_list_element.innerHTML = '<p>No products found.</p>'
    } else {
        let product_list_items = '';
        products.forEach(function(product) {
            product_list_items += '<li>' + product.text + '</li>\n'
        })
        product_list_element.innerHTML = '<ul>\n' + product_list_items + '</ul>\n'
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
};