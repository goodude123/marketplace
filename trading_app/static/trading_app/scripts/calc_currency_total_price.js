window.onload = function(){
    addChangeEventToElementId('id_quantity');
    addChangeEventToElementId('id_currency_code');
};


function addChangeEventToElementId(id){
    var inputQuantityBox = document.getElementById(id);
    inputQuantityBox.addEventListener("change", getCodesAndRatesFromApiAndCalculatePrice);
}


function calculateAndPrintTotalPrice(rates, units){
    quantity = getQuantityFromElement('id_quantity');
    index = document.getElementById('id_currency_code').selectedIndex;
    rate = rates[index];
    unit = units[index];
    if (quantity > 0) {
        price = quantity * rate * unit;
        price = price.toFixed(4);
        response = 'Total Price: ' + price;
    } else {
        response = 'Invalid Value.';
    }
    insertTotalPriceIntoId('totalPrice', response);
}


function insertTotalPriceIntoId(id, response){
    elementToInsertPrice = document.getElementById(id);
    elementToInsertPrice.innerHTML = response;
}


function getCodesAndRatesFromApiAndCalculatePrice(){
    $.ajax({
        method: 'GET',
        // endpoint is declared in django template
        url: endpoint,
        success: function (data) {
            rates = apiGetRates(data);
            units = apiGetUnits(data);
            calculateAndPrintTotalPrice(rates, units);
        },
        error: function (error_data){
            console.log(error_data);
        }
    });
}


function getQuantityFromElement(elementId){
    var quantityField = document.getElementById(elementId);

    return quantityField.value;
}


function apiGetRates(data){
    rates = data.currencies.rates;

    return rates;
}


function apiGetUnits(data){
    units = data.currencies.units;

    return units;
}
