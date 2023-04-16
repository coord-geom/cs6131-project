window.addEventListener('DOMContentLoaded', () => {
    date = document.getElementById('depdate');
    if(!Date.parse(date.valueAsDate)) date.valueAsDate = new Date();
    var today = new Date().toISOString().split('T')[0];
    document.getElementById('depdate').setAttribute('min',today);
});

function showFilters(element){
    var filters = document.getElementById('filters');
    if(element.innerHTML === "Show more") {
        element.innerHTML = "Show less";
        filters.style.display = "block";
    } else {
        element.innerHTML = "Show more";
        filters.style.display = "none";
    }

    changeRating(document.getElementById('rating'));
    changeCapacity(document.getElementById('cap'));
    changeCost(document.getElementById('cost'));
}

function changeRating(element) {
    document.getElementById('rating-text').innerHTML = "Rating >= " + element.value;
}

function changeCapacity(element) {
    document.getElementById('cap-text').innerHTML = "Max Group Size <= " + element.value;
}

function changeCost(element) {
    document.getElementById('cost-text').innerHTML = "Adult Cost <= $" + element.value;
}