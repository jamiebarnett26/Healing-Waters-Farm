
'use strict';

let request = null;
function getFamilyResults() {
    function handleResponse(families) {
        let html = convertToHtml(families);
        $('#listOfButtons').html(html)
    }

    function convertToHtml(families) {
        let template = `
        {{#families}}
            <<p>{{family_name}}</p>>
        {{/families}}
        `;
        let map = {families: families};
        let html = Mustache.render(template, map);
        return html
    }

    let familyId = $('#familyInput').val();
    let encodedFamilyId = encodeURIComponent(familyId);

    let url = '/selectFamily?family=' + encodedFamilyId;

    if (request !== null) {
        request.abort();
    }

    let requestData = {
        type: 'GET',
        url: url,
        success: handleResponse, 
        error: handleError
    };

    request = $.ajax(requestData);
}


let timer = null;
function debouncedGetResults() {
    clearTimeout(timer);
    timer = window.setTimeout(getFamilyResults, 500)
}

function setup() {
    $('#familyInput').on('input', debouncedGetResults);
    getFamilyResults();

}

$('document').ready(setup);
