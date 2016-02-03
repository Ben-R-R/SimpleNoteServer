function loadNote(id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            document.getElementById("Editor").innerHTML = xhttp.responseText;
        }
    };
    xhttp.open("POST", "/loadNote", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("id=" + encodeURIComponent(id));
}

function createNewNote() {
    var nodeName = document.getElementById('NewNodeName').value
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            document.getElementById("NodeList").innerHTML = xhttp.responseText;
        }
    };
    
    xhttp.open("POST", "/newNote", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("name=" + encodeURIComponent(nodeName));
}

function saveNote(id) {
    var nodeName = document.getElementById('Name').value;
    var nodeContent = document.getElementById('Content').value;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            document.getElementById("NodeList").innerHTML = xhttp.responseText;
        }
        //refreshNoteList()
    };

    xhttp.open("POST", "/saveNode", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("name=" + encodeURIComponent(nodeName) + "&content=" + encodeURIComponent(nodeContent) + "&id=" + encodeURIComponent(id));
}

function refreshNoteList() {
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            document.getElementById("NodeList").innerHTML = xhttp.responseText;
        }
    };

    xhttp.open("POST", "/refreshNoteList", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
}

function deleteNode(nodeId) {
 
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            document.getElementById("NodeList").innerHTML = xhttp.responseText;
        }
    };

    xhttp.open("POST", "/deleteNote", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("id=" + encodeURIComponent(nodeId));
}