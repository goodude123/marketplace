function calculateAndPrintTotalPrice(rates, units){
    quantity = getQuantityFromElement('id_quantity');
    index = document.getElementById('id_currencies').value;
    console.log(rates);
    rate = rates[index] - 0.004;
    unit = units[index];
    if (quantity > 0) {
        price = quantity * rate * unit;
        price = price.toFixed(5);
        price = removeTrailingZeros(price);
        response = 'Total Price: ' + price;
    } else {
        response = 'Invalid Value.';
    }
    insertTotalPriceIntoId('totalPrice', response);
}


window.onload = function(){
    addChangeEventToElementId('id_quantity');
    addChangeEventToElementId('id_currencies');
};