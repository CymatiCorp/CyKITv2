/*
  CyKITv2 
  CyInterface.js 2017.11
  ========================
  Written by Warren
  
  CyKITv2 HTML back-end for controlling interface and handling data.
*/

cyHost = document.getElementById('cyHost').value;
cyPort = document.getElementById('cyPort').value;

if (cyHost == null) { cyHost = "127.0.0.1"; }
if (cyPort == null) { cyPort = "15525"; }

var client = new CySocketClient(cyHost, cyPort, "CyKITv2");

            
var cyCanvas = document.getElementById('cyCanvas');
var ctx = cyCanvas.getContext('2d');
var buffer = document.createElement('canvas');
var btx = buffer.getContext('2d');
buffer.width = (document.getElementById('canvasPane').offsetWidth);
buffer.height = (document.getElementById('canvasPane').offsetHeight);
ctx.imageSmoothingEnabled = false;
btx.imageSmoothingEnabled = false;

var img = document.getElementById('graphImage');
var graphPattern = btx.createPattern(img, "repeat");
btx.fillStyle = graphPattern;

var canvasWidth = cyCanvas.width;
var canvasHeight = cyCanvas.height;
var selected_model = 0;
var viewType = "16"; // Default::Data View. (32=Gyro)
var mems_x = 100;
var battery_check = 0;
var reset_baseline = true;
var init_baseline = true;
        
var sensorDATA_epoc = [3,4,1,2,5,6,7,8,9,10,13,14,11,12];
var sensorDATA_insight = [2,8,4,5,7];
var sensorDATA_epoc_plus = [7,9,3,5,15,11,13,19,21,23,29,31,25,27];
var sensorNAME_epoc = ["AF3","F7","F3","FC5","T7","P7","O1","O2","P8","T8","FC6","F4","F8","AF4"];
var sensorNAME_insight = ["AF3","T7","Pz", "T8", "AF4"]
var sensorDATA_color  = ["#ff0000","#ff8000", "#ffbf00", "#bfff00","#40ff00","#00ffbf","#00bfff",
                        "#0040ff","#4000ff", "#bf00ff", "#ff00bf","#ff0040","#ff0000","#ffff00"];        
var sensorGYRO_insight = [0,1,2,3,4,5,6,7,8,9,10,11,12,"MAG_Z","MAG_Y"];        
        

        
function openTab(tabName) {
    var i;
    var x = document.getElementsByClassName("tabs");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    document.getElementById(tabName).style.display = "block"; 
    
}
        
function viewChange(model) {
    var CyView = document.getElementById("CyView").value;
    
    if (CyView == "Data") {
        viewType = "16";
    }
    else {
        viewType = "32";
    }
   
    console.log(viewType);
}
            
function modelChange(model) {
    if (client == null) { return; }
        console.log(model[model.selectedIndex].id);
        selected_model = model[model.selectedIndex].id;
        client.sendData("CyKITv2:::setModel:::" + selected_model);
    }
            
    document.addEventListener("DOMContentLoaded", function(event) {
            
        window.addEventListener('resize', resizeCanvas, true);

        
        var check_Manual = document.querySelector('input[id=manualControl]');
        check_Manual.addEventListener('change', function (event) {
        
            var checkManual = document.getElementById("manualSelection");
            var cyManual = document.getElementById("cyManual");
        
            if (check_Manual.checked) {
                checkManual.style.display = 'none';
                cyManual.style.visibility = 'visible';
            }
            else {
                checkManual.style.display = 'inline';
                cyManual.style.visibility = 'hidden';
            }
        
        });
        var check_Mask = document.querySelector('input[id=setMask]');
        check_Mask.addEventListener('change', function (event) {
        
            var setMask = document.getElementById("maskView");
            var cyMask = document.getElementById("CyMask");
            var newMask = document.getElementById("newMask");
            var maskChange = document.getElementById("maskChange");
            
        
            if (check_Mask.checked) {
                setMask.style.display = 'inline';
                setMask.style.visibility = 'visible';
                cyMask.style.visibility = 'visible';
                newMask.style.visibility = 'visible';
                maskChange.style.visibility = 'visible';
            }
            else {
                setMask.style.display = 'none';
                setMask.style.visiblity = 'hidden';
                cyMask.style.visibility = 'hidden';
                newMask.style.visibility = 'hidden';
                maskChange.style.visibility = 'hidden';
            }
        
        });
        
        var scroll_checked = document.querySelector('input[id=CyScroll]');
        scroll_checked.addEventListener('change', function (event) {
            scroll_check = document.getElementById("CyScroll").checked;
            ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        });
        
        function resizeCanvas() {
            
            cyCanvas.width = (document.getElementById('canvasPane').offsetWidth);
            cyCanvas.height = (document.getElementById('canvasPane').offsetHeight);
            canvasWidth = cyCanvas.width;
            canvasHeight = cyCanvas.height;

            
            return; 
            // Replaced manual drawing of lines, with graph image. 
            var maxPoints = 16;
            var yInc = ((canvasHeight + 150) / maxPoints);
            var yPos = 0;
            for (var i = 0; i < maxPoints; i++) {
                yPos += (i ==0) ? 50 : yInc;
                drawLine(10, yPos, canvasWidth, yPos, '#000000', .5);
            }
                    
                    
        }

        var myContact = 1;
        var myAvg = 0;
        var myTotal = 0; 
        var listing;
        var myResult = 0;
                        
        var cy_x = 1;
        var cy_y = 10;
        var oldx = 0;
        var oldy = [];
        var baseline = [];
        var reset_counter = 0;
        var v = 0;    
        var scroll_check = document.getElementById("CyScroll").checked;
        
        resizeCanvas();
        console.log("Test");

        function drawLine(startX, startY, endX, endY, strokeStyle, lineWidth) {
            if (strokeStyle != null) { ctx.strokeStyle = strokeStyle; }
            if (lineWidth != null) { ctx.lineWidth = lineWidth; }
            
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(endX, endY);
            ctx.stroke();
            ctx.closePath();    
        }

        function scroll_screen() { 
          if (scroll_check) {
                v = v + 1;           
                if (v > 1) {
                    v = 0;

                    btx.drawImage(cyCanvas, 0, 0, canvasWidth, canvasHeight);
                    
                    
                    ctx.drawImage(buffer, -1, 0, canvasWidth, canvasHeight);
                    
                    btx.fillStyle = "#111111";
                    btx.fillRect(0, 0, buffer.width, buffer.height);
                    
                    //btx.drawImage(graphPattern, 0, 0, buffer.width, buffer.height);
                    
                    
                    
                    
                    
                    //btx.fillRect(0, 0, canvasWidth, canvasHeight);
                    
                    //buffer.getContext('2d').clearRect(0,0,canvasWidth,canvasHeight);
                    
                    
                    
                   //buffer.getContext('2d').drawImage(graphImage,0,0);
                }
            }

        }
        function drawdot(contact, offset, x, y, color) {


            ctx.beginPath();
            ctx.lineWidth=".8";
            ctx.strokeStyle=color; 
            ctx.moveTo(oldx, Math.abs(y) + Math.abs(offset));
            ctx.lineTo(x, oldy[contact]);
            ctx.stroke();
            oldy[contact] = Math.abs(y) + Math.abs(offset);

        }

        client.onCommand  = function(text) {
            var cyStatus = document.getElementById("CyStatus");
            var cyDevice = document.getElementById("CyDevice");
            var cySerial = document.getElementById("CySerial");
            var cyKeyModel = document.getElementById("CyKeyModel");
            var cyHeadset = document.getElementById("CyHeadset");
            var cyPicture = document.getElementById("CyKIT-picture");
            
            var selectINSIGHT = document.getElementById("select.Insight");
            var selectEPOC = document.getElementById("select.Epoc");
            
            newCmd = text.split(":::");
            console.log(newCmd[1]);
            
            if (newCmd[1] == "Connected") {
                cyStatus.innerHTML = "Connected.";
                cyPicture.style.backgroundImage = "url('./images/CyKITv2-bg-on.png')";
            }
            
            if (newCmd[1] == "Info") {
                if (newCmd[2] == "Device") {
                    cyDevice.innerHTML = newCmd[3];
                }
            }
            
            if (newCmd[2] == "Serial") {
                cySerial.innerHTML = newCmd[3];
            }

            // Key Detection.            
            if (newCmd[2] == "KeyModel") {
                cyKeyModel.innerHTML = newCmd[3];
                if (selected_model == parseInt(newCmd[3])) { return; }
                selected_model = parseInt(newCmd[3])
                
                // Epoc Detected.
                if (selected_model == 2 || selected_model == 1) {
                    selectINSIGHT.style.visibility = 'hidden';
                    selectEPOC.style.visibility = 'visible';
                    var sensorList = document.getElementById("CySelect");
                    var sensorOption = document.createElement("option");
                    var epocContacts = ["Counter","AF3","F7","F3","FC5","T7","P7","O1","O2","P8","T8","FC6","F4","F8","AF4","Gyro_X","Gyro_Y"];
                    
                    sensorOption.text = "Select Sensor";
                    sensorList.add(sensorOption);
                    
                    for (i = 0; i < 17; i++) {
                        var sensorOption = document.createElement("option");
                        sensorOption.text = epocContacts[i];
                        sensorOption.value = i;
                        sensorList.add(sensorOption);
                    }
                }
                
                // Insight Detected.
                if (selected_model == 4 || selected_model == 3) {
                    selectINSIGHT.style.visibility = 'visible';
                    selectEPOC.style.visibility = 'hidden';
                    
                    var sensorList = document.getElementById("CySelect");
                    var sensorOption = document.createElement("option");
                    
                    
                    sensorOption.text = "Select Sensor";
                    sensorList.add(sensorOption);
                    
                    for (i = 0; i < 33; i++) {
                        var sensorOption = document.createElement("option");
                        sensorOption.text = i;
                        sensorOption.value = i;
                        sensorList.add(sensorOption);
                    }
                
                }
                
                // Epoc+ Detected.
                if (selected_model == 6 || selected_model == 5) {
                    selectINSIGHT.style.visibility = 'hidden';
                    selectEPOC.style.visibility = 'visible';
                    var sensorList = document.getElementById("CySelect");
                    var sensorOption = document.createElement("option");
                    
                    //var epocContacts = ["Counter","AF3","F7","F3","FC5","T7","P7","O1","O2","P8","T8","FC6","F4","F8","AF4","Gyro_X","Gyro_Y"];
                    
                    sensorOption.text = "Select Sensor";
                    sensorList.add(sensorOption);
                    
                    for (i = 0; i < 33; i++) {
                        var sensorOption = document.createElement("option");
                        sensorOption.text = i;
                        sensorOption.value = i;
                        sensorList.add(sensorOption);
                    }
                }
                var modelTypes = ["None","Epoc-Research","Epoc","Insight (Research)","Insight","Epoc+ (Research)","Epoc+"];
                cyHeadset.innerHTML = modelTypes[selected_model];
            
            }
                
        }
    
    client.onData  = function(text) {
        scroll_screen();
        
        var div = document.createElement('div');
        contact = text.split(" ");
        var manualControl = document.getElementById("manualControl").checked;
        
        // Epoc     
        // ======    
        if (selected_model == 2) {
            
            oldx = cy_x;
                if (scroll_check) {
                    cy_x = canvasWidth -10; 
                }
                else {
                    cy_x = cy_x + .5;
                }
                
                if (cy_x > canvasWidth) { 
                    oldx = 0;
                    cy_x = 0; 
                    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
                }

                if (battery_check > 120) {
                    
                }
                if (battery_check == 127) {
                    var myBattery = document.getElementById("CyBattery");
                    var battery_percent = ((((parseInt(contact[0]) - 255) +31) *3.23));
                    myBattery.innerHTML = parseInt(battery_percent)  + "%";
                    
                    
                }
                reset_counter +=1 ;
                if (reset_counter > 500) {
                    reset_baseline = true;  
                    if (reset_counter > 600) {
                        reset_counter = 0;
                    }                
                } 
                
                battery_check = contact[0];
                
            if (baseline[1] == null || reset_baseline == true) {
                    for (i = 0; i < 33; i++) {
                        
                        if (init_baseline == false) {
                            baseline[i] = baseline[i] + Math.abs(contact[i]);
                            baseline[i] = parseInt((baseline[i] / 2));
                        }
                        else {
                            baseline[i] = Math.abs(contact[i]);
                        }
                    }
                    
                    console.log("Reset Baseline.");
                    reset_baseline = false;
                    init_baseline = false;
            }
                
            if (manualControl) {
                var myContact = document.getElementById("CySelect").value;
                var myValue = Math.abs(contact[myContact]);
                
                drawdot(myContact, 50, cy_x, ((eval(myValue) - baseline[myContact]) * .3)  + 10, "white");
            }
            else {
                var arr_element;
                for (arr_element in sensorNAME_epoc) {
                    var c = document.getElementById("e." + sensorNAME_epoc[arr_element]);
                    var myColor = sensorDATA_color[arr_element];
                    if (c.checked == true) {
                        var currentValue = Math.abs(eval(contact[eval(sensorDATA_epoc[arr_element])]));                    
                        offset = parseInt(((canvasHeight * .05) / sensorDATA_epoc.length));
                        drawdot(arr_element, (offset * (arr_element +1)), cy_x, (currentValue - baseline[arr_element]) * .55, myColor);
                    }
                }
            }
        }
        
        // Insight
        // =========
        if (selected_model == 4) {
            
            if (baseline[1] == null || reset_baseline == true) {
                for (i = 0; i < 33; i++) {
                    baseline[i] = contact[i];
                }
                reset_baseline = false;
            }
            oldx = cy_x;
            cy_x = cy_x + .5;
            
            if (battery_check == 127) {
                reset_baseline = true;
                var counter = parseInt(contact[0]);
                var myBattery = document.getElementById("CyBattery");
                var battery_percent = (((counter - 245) +26) *3.85);
                myBattery.innerHTML = parseInt(battery_percent) + "%";
            }
            
            battery_check = contact[0];

            if (cy_x > canvasWidth) { 
                oldx = 0;
                cy_x = 0; 
                ctx.clearRect(0, 0, canvasWidth, canvasHeight);
            }
            

            if (manualControl) {
                var myContact = document.getElementById("CySelect").value;
                var currentValue = eval(contact[myContact]) - 127;
                var myColor = "white";
                var subtract_by = 255;

                drawdot(myContact, 60, cy_x, (currentValue - baseline[myContact]) * .3, myColor);
            }
            else {
                var arr_element;
                for (arr_element in sensorNAME_insight) {
                    var c = document.getElementById("i." + sensorNAME_insight[arr_element]);
                    var myColor = sensorDATA_color[arr_element];
                    if (c.checked == true) {
                        var currentValue = eval(contact[eval(sensorDATA_insight[arr_element])]);
                        offset = (((canvasHeight + 22) / sensorNAME_insight.length) * (arr_element)) + 30;
                        drawdot(arr_element, offset, cy_x, (cy_y - baseline[arr_element]) * .3, myColor);
                    }
                }
            }
        }
        
        // Epoc+ 
        // =======
        if (selected_model == 6) {

            if (contact[0] == 255) {
                if (contact[1] == 16) {
                    var BatteryLevel = document.getElementById("CyBattery");
                    var battery_percent = (((parseInt(contact[16]) - 117) +26) *3.85);
                    BatteryLevel.innerHTML = parseInt(battery_percent) + "%";
                    reset_baseline = true;
                }
            }
            
            if (contact[1] == viewType) {
                
                oldx = cy_x;
                if (scroll_check) {
                    cy_x = canvasWidth -10; 
                }
                else {
                    cy_x += 1;
                    if (cy_x > canvasWidth) { 
                        oldx = 0;
                        cy_x = 0; 
                        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
                    }
                }
                
                 
                //Epoc+ Data   
                if (contact[1] == "16") {
                        if (baseline[1] == null || reset_baseline == true) {
                    for (i = 0; i < 33; i++) {
                        
                        if (init_baseline == false) {
                            baseline[i] = baseline[i] + Math.abs(contact[i]);
                            baseline[i] = parseInt((baseline[i] / 2));
                        }
                        else {
                            baseline[i] = Math.abs(contact[i]);
                        }
                    }
                    
                    console.log("Reset Baseline.");
                    reset_baseline = false;
                    init_baseline = false;
            }     
                    
                    if (manualControl) {                 
                        
                        var myContact = document.getElementById("CySelect").value;
                        var myValue = Math.abs(contact[myContact]);
                        
                        drawdot(myContact, 50, cy_x, ((eval(myValue) - baseline[myContact]) * .3)  + 10, "white");
                    }
                
                }
                // Epoc+ Gyro
                if (contact[1] == "32") {
                         if (baseline[1] == null || reset_baseline == true) {
                    for (i = 0; i < 33; i++) {
                        
                        if (init_baseline == false) {
                            baseline[i] = baseline[i] + Math.abs(contact[i]);
                            baseline[i] = parseInt((baseline[i] / 2));
                        }
                        else {
                            baseline[i] = Math.abs(contact[i]);
                        }
                    }
                    
                    console.log("Reset Baseline.");
                    reset_baseline = false;
                    init_baseline = false;
            }       
                    if (manualControl) {                 
                        var myContact = document.getElementById("CySelect").value;
                        var myValue = 127+ Math.abs(contact[myContact]);
                
                        drawdot(myContact, 50, cy_x, ((eval(myValue) - baseline[myContact]) * .3)  + 10, "white");

                    }
                }
            }
        }   
    }
});

// Connect Button
document.getElementById('cyConnect').onclick = function(e) {
    client.connect();
}

// Disconnect Button
document.getElementById('cyDisconnect').onclick = function(e) {
    var cyPicture = document.getElementById("CyKIT-picture");
    cyPicture.style.backgroundImage = "url('./images/CyKITv2-bg-off.png')";
    
    var selectEPOC = document.getElementById("select.Epoc");
    var selectINSIGHT = document.getElementById("select.Insight");
    
    selectEPOC.style.visibility = 'hidden';
    selectINSIGHT.style.visibility = 'hidden';
    client.close();
}

// Change Get_Level mask in eeg.py
document.getElementById('maskChange').onclick = function(e) {
    client.sendData("CyKITv2:::setMask:::" + document.getElementById('CyMask').value + ":::" + document.getElementById('newMask').value);
    reset_baseline = true;  
}

