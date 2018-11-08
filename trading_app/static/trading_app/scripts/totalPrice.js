var TotalPrice = ( function() {
    var addChangeEventToElementId = function (id) {
        var inputQuantityBox = document.getElementById(id);
        inputQuantityBox.addEventListener("change", getCodesAndRatesFromApiAndCalculatePrice);
    };

    var getCodesAndRatesFromApiAndCalculatePrice = function () {
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
    };

    var apiGetRates = function (data) {
        rates = data.currencies.rates;
    
        return rates;
    };

    var apiGetUnits = function (data) {
        units = data.currencies.units;
    
        return units;
    };

    var getQuantityFromElement = function (elementId) {
        var quantityField = document.getElementById(elementId);

        return quantityField.value;
    };

    var removeTrailingZeros = function (number) {
        number = number * 1;
        number = number.toString();
        return number;
    };

    var insertTotalPriceIntoId = function (id, response) {
        elementToInsertPrice = document.getElementById(id);
        elementToInsertPrice.innerHTML = response;
    };
    

    return {
        addChangeEventToElementId: addChangeEventToElementId,
        getQuantityFromElement: getQuantityFromElement,
        removeTrailingZeros: removeTrailingZeros,
        insertTotalPriceIntoId: insertTotalPriceIntoId,
    };
})();
