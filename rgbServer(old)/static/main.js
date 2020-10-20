function setRed(val) {
    document.getElementById("r").innerHTML = "Red: ".concat(val);
    r = + val;
    changeColor();
}

function setGreen(val) {
    document.getElementById("g").innerHTML = "Green: ".concat(val);
    g = + val;
    changeColor();
}

function setBlue(val) {
    document.getElementById("b").innerHTML = "Blue: ".concat(val);
    b = + val;
    changeColor();
}

function setBrightness(val) {
    document.getElementById("brightness").innerHTML = "Brightness: ".concat(val);
}

function changeColor() {
    // make sure they will form a valid hex
    var rString = r.toString(16)
    while (rString.length < 2) {
        rString = '0'.concat(rString)
    }
    var gString = g.toString(16)
    while (gString.length < 2) {
        gString = '0'.concat(gString)
    }
    var bString = b.toString(16)
    while (bString.length < 2) {
        bString = '0'.concat(bString)
    }
    // set background color
    var hexString = "#".concat(rString.concat(gString.concat(bString)));
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

function toggleSliders() {
    var x = document.getElementById("sliders");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  } 