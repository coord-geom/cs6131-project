$('.date').datepicker({
    multidate: true,
    format: 'yyyy-mm-dd'
});

function textAreaAdjust(element) {
    element.style.height = "1px";
    element.style.height = (25+element.scrollHeight)+"px";
}

function edit(element) {
    document.getElementById('cancelChanges').hidden = false;
    document.getElementById('details_mine').hidden = true;
    document.getElementById('updateForm').hidden = false;
    element.hidden = true;
}

function cancelChanges(element) {
    element.hidden = true;
    document.getElementById('details_mine').hidden = false;
    document.getElementById('editButton').hidden = false;
    document.getElementById('updateForm').hidden = true;
}