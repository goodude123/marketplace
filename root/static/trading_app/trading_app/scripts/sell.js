function calculateAndPrintTotalPrice(rates, units){
    quantity = TotalPrice.getQuantityFromElement('id_quantity');
    index = document.getElementById('id_currencies').value;
    rate = rates[index] - 0.004;
    unit = units[index];
    if (quantity > 0) {
        price = quantity * rate * unit;
        price = price.toFixed(5);
        price = TotalPrice.removeTrailingZeros(price);
        response = 'Total Price: ' + price;
    } else {
        response = 'Invalid Value.';
    }
    TotalPrice.insertTotalPriceIntoId('totalPrice', response);
}


window.onload = function(){
    TotalPrice.addChangeEventToElementId('id_quantity');
    TotalPrice.addChangeEventToElementId('id_currencies');
};
