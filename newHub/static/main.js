var hostname = document.getElementById("hostname").innerHTML
var port = document.getElementById("port").innerHTML
console.log(`connecting to ws://${hostname}:${port}/`)
var ws = new WebSocket(`ws://${hostname}:${port}/`, 'rgbStrip');
console.log(ws)

function setRed(val) {
    document.getElementById("r").innerHTML = "Red: ".concat(val);
    // r = + val;
    changeColor();
}

function setGreen(val) {
    document.getElementById("g").innerHTML = "Green: ".concat(val);
    // g = + val;
    changeColor();
}

function setBlue(val) {
    document.getElementById("b").innerHTML = "Blue: ".concat(val);
    // b = + val;
    changeColor();
}

function setBrightness(val) {
    document.getElementById("brightness").innerHTML = "Brightness: ".concat(val);
    // console.log(val)
    ws.send(`brightness|${val}`)
}

function changeColor() {
    // make sure they will form a valid hex
    var rString = document.getElementById("r").innerHTML
    rString = parseInt(rString.slice(5)).toString(16).padStart(2, "0")
    var gString = document.getElementById("g").innerHTML
    gString = parseInt(gString.slice(7)).toString(16).padStart(2, "0")
    var bString = document.getElementById("b").innerHTML
    bString = parseInt(bString.slice(6)).toString(16).padStart(2, "0")

    // set background color
    var hexString = "#".concat(rString.concat(gString.concat(bString)));
    document.body.style.backgroundColor = hexString;

    // send to flask application "rgb|hexstring"
    ws.send(`rgb|${hexString}`)
}

function setHex(hexString) {
        // set numbers
        r = parseInt(hexString.substring(1,3), 16);
        g = parseInt(hexString.substring(3,5), 16);
        b = parseInt(hexString.substring(5,7), 16);

        document.getElementById("r").innerHTML = "Red: ".concat(r);
        document.getElementById("g").innerHTML = "Green: ".concat(g);
        document.getElementById("b").innerHTML = "Blue: ".concat(b);

        // set background color
        document.body.style.backgroundColor = hexString;
        
        // if needed, brighten text color to see it
        if ((r < 150) && (g < 115) && (b < 150)) {
            document.getElementById("error").innerHTML = hexString;
            document.getElementById("color").style.color = "#e4e4e4";
        }
        else {
            document.getElementById("color").style.color = "#000000";
        }
    
        // debug 
        document.getElementById("error").innerHTML = hexString;    
}

// allow for tabs
function openPage(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}


