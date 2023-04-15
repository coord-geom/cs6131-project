function textAreaAdjust(element, i) {
    element.style.height = "1px";
    element.style.height = (25+element.scrollHeight)+"px";
}


function edit(element, i) {
    document.getElementById('cancelChanges'+i).hidden = false;
    document.getElementById('details_mine'+i).hidden = true;
    document.getElementById('updateForm'+i).hidden = false;
    element.hidden = true;
}

function cancelChanges(element, i) {
    element.hidden = true;
    document.getElementById('details_mine'+i).hidden = false;
    document.getElementById('editButton'+i).hidden = false;
    document.getElementById('updateForm'+i).hidden = true;
}

    