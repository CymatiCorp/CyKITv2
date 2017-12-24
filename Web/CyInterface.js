/*
  CyKITv2 
  CyInterface.js 2017.12
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
var viewType = "16";     // Default:: (16 = Data)           (32 = Gyro)
var formatType = 0; //  Default:: (0  = Floating Point) (1  = Raw Data)
var mems_x = 100;
var battery_check = 0;
var reset_baseline = true;
var init_baseline = true;

var modelTypes = ['None','Epoc-Research','Epoc','Insight (Research)','Insight','Epoc+ (Research)','Epoc+'];
var headset = { 
                0: 'epoc', 1: 'epoc', 2: 'epoc', 3: 'insight', 4: 'insight', 5: 'epoc_plus', 6: 'epoc_plus'  }

var sensorNAME = {
                    epoc: ['AF3','F7','F3','FC5','T7','P7','O1','O2','P8','T8','FC6','F4','F8','AF4'],
                 insight: ['AF3','T7','Pz', 'T8', 'AF4'] }
                 
var sensorDATA = {
                    epoc: [4,5,2,3,6,7,8,9,10,11,14,15,12,13],
                 insight: [1,2,3,4,5,6,7,8,9,10,11,12,13,14] }

var sensorGYRO = {
                 insight: [0,1,2,3,4,5,6,7,8,9,10,11,12] }

var sensorDATA_color  = ['#ff0000','#ff8000', '#ffbf00', '#bfff00','#40ff00','#00ffbf','#00bfff',
                        '#0040ff','#4000ff', '#bf00ff', '#ff00bf','#ff0040','#ff0000','#ffff00'];        
                        
function roundToTwo(num) {    
    return +(Math.round(num + "e+2")  + "e-2");
}

function update_sensorList(select_headset) {
    
    var manualControl = document.getElementById("manualControl").checked;
    var sensorList = document.getElementById("CySelect");

    var i = 0;
    for(i = sensorList.length - 1 ; i >= 0 ; i--) {
        sensorList.remove(i);
    }
    
    var sensorOption = document.createElement("option");
    sensorOption.text = "Select Sensor";
    sensorList.add(sensorOption);
    
    if (manualControl) {
        
        if (formatType == 0) {
            for (i = 0; i < sensorNAME[select_headset].length; i++) {
                var sensorOption = document.createElement("option");
                sensorOption.text = sensorNAME[select_headset][i];
                sensorOption.value = i;
                sensorList.add(sensorOption);
            }
        }
        else {
            for (i = 0; i < 33; i++) {
                var sensorOption = document.createElement("option");
                sensorOption.text = i;
                sensorOption.value = i;
                sensorList.add(sensorOption);
            }
        }
    }
    
}
                        
function openTab(tabName) {
    var i;
    var x = document.getElementsByClassName("tabs");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    document.getElementById(tabName).style.display = "block"; 
    
}

function changeFormat(format) {
    var CyFormat = document.getElementById("CyFormat").value;
    
    if (CyFormat == "Floating Point") {
        formatType = 0;
    }
    else {
        formatType = 1;
    }
    client.sendData("CyKITv2:::changeFormat:::" + formatType);
    update_sensorList(headset[selected_model].replace('epoc_plus','epoc'));
    console.log(formatType);
}
                    
function viewChange(model) {
    var CyView = document.getElementById("CyView").value;
    
    if (CyView == "Data") {
        viewType = "16";
    }
    else {
        viewType = "32";
    }
   
    //console.log(viewType);
}
            
function modelChange(model) {
    if (client == null) { return; }
        console.log(model[model.selectedIndex].id);
        selected_model = model[model.selectedIndex].id;
        client.sendData("CyKITv2:::setModel:::" + selected_model);
    }
            
    document.addEventListener("DOMContentLoaded", function(event) {
            
        window.addEventListener('resize', resizeCanvas, true);

        update_sensorList(headset[selected_model].replace('epoc_plus','epoc'));
        
        var check_Manual = document.querySelector('input[id=manualControl]');
        check_Manual.addEventListener('change', function (event) {
        
            var checkManual = document.getElementById("manualSelection");
            var cyManual = document.getElementById("cyManual");
        
            if (check_Manual.checked) {
                checkManual.style.display = 'none';
                cyManual.style.visibility = 'visible';
                update_sensorList(headset[selected_model].replace('epoc_plus','epoc'));
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
        var oldg = [];
        var baseline = [];
        var mean = [];
        var rms = {
        0: [],
        1: [],
        2: [],
        3: []
        };
        var rmsIndex = 0;
        var reset_counter = 0;
        var rms_counter = 0;
        var v = 0;    
        var scroll_check = document.getElementById("CyScroll").checked;
        
        resizeCanvas();

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
        function convertEPOC_PLUS(value_1, value_2) {
            return (((value_1 * .128205128205129) + 4201.02564096001) + ((value_2 -128) * 32.82051289));
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
            var manualControl = document.getElementById("manualControl").checked;
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
                    
                    sensorOption.text = "Select Sensor";
                    sensorList.add(sensorOption);
                    
                    update_sensorList('insight');
                    
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

                    var settingsButton = document.getElementById("settingsButton");
                    settingsButton.disabled = false;
                    
                    update_sensorList('epoc');

                }
                
                cyHeadset.innerHTML = modelTypes[selected_model];
            
            }
                
        }
    
    client.onData  = function(text) {
        scroll_screen();
        var eeg_resolution = (document.getElementById("myRange").value * .01);
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

                if (battery_check == 127) {
                    var myBattery = document.getElementById("CyBattery");
                    var battery_percent = ((((parseInt(contact[0]) - 255) +31) *3.23));
                    myBattery.innerHTML = parseInt(battery_percent)  + "%";
                }
                reset_counter +=1 ;
                if (reset_counter > 55) {
                    reset_baseline = true;  
                    reset_counter = 0;
                } 
                
                battery_check = contact[0];
                
                if (baseline[1] == null || reset_baseline == true) {
                    for (i = 0; i < contact.length; i++) {
                        
                        if (init_baseline == false) {
                            baseline[i] = baseline[i] + Math.abs(contact[i]);
                            baseline[i] = parseInt((baseline[i] / 2));
                            
                        }
                        else {
                            baseline[i] = Math.abs(contact[i]);
                        }
                    }
                    
                }
                reset_baseline = false;
                
            if (manualControl) {
                var myContact = document.getElementById("CySelect").value;
                var myValue = Math.abs(contact[myContact]);
                
                drawdot(myContact, 10, cy_x, ((eval(myValue) - baseline[myContact]) * eeg_resolution)  + 10, "white");
            }
            else {
                var inc_y_offset = 10;
                var inc_step = (contact.length +1);
                var arr_element;
                for (arr_element in sensorNAME['epoc']) {
                    var c = document.getElementById("e." + sensorNAME['epoc'][arr_element]);
                    var myColor = sensorDATA_color[arr_element];
                    var myContact = sensorDATA['epoc'][arr_element]
                    if (c.checked == true) {
                        inc_y_offset += Math.abs(parseInt((canvasHeight / inc_step)));
                        var currentValue = contact[myContact];
                        
                        //var value_floor = Math.floor((baseline[select_contact] / 1000.0))
                        drawdot(myContact, inc_y_offset, cy_x, (currentValue - baseline[myContact]) * eeg_resolution, myColor);
                    
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

                drawdot(myContact, 60, cy_x, (currentValue - baseline[myContact]) * eeg_resolution, myColor);
            }
            else {
                var arr_element;
                var inc_y_offset = 10;
                var inc_step = (sensorNAME['epoc'].length +1);
                for (arr_element in sensorNAME['epoc']) {
                    if (arr_element == 1) { continue; }
                    var c = document.getElementById("e." + sensorNAME['epoc'][arr_element]);
                    var myColor = sensorDATA_color[arr_element];
                    inc_y_offset += Math.abs(parseInt((canvasHeight / inc_step)));
                    if (c.checked == true) {
                        select_contact = parseInt(sensorDATA['epoc'][arr_element]);
                        var value_data = (baseline[select_contact] - parseFloat(contact[select_contact]));
                        var value_floor = Math.floor((baseline[select_contact] / 1000.0))
                        drawdot(select_contact, inc_y_offset, cy_x, value_floor - (value_data * .128) * eeg_resolution, myColor);
                    }
                }
                    /*
                var arr_element;
                for (arr_element in sensorNAME['insight']) {
                    var c = document.getElementById("i." + sensorNAME['insight'][arr_element]);
                    var myColor = sensorDATA_color[arr_element];
                    if (c.checked == true) {
                        var currentValue = contact[sensorDATA_insight[arr_element]];
                        offset = (((canvasHeight + 22) / sensorNAME['insight'].length) * (arr_element)) + 30;
                        drawdot(arr_element, offset, cy_x, (cy_y - baseline[arr_element]) * .3, myColor);
                    }
                }
                */
            }
        }
        
        // Epoc+ 
        // =======
        if (selected_model == 6) {

            //Check Battery Level. 
            if (contact[0] == 255) {
                if (contact.length < 32) { return; }
                if (contact[1] == 16) {
                    var BatteryLevel = document.getElementById("CyBattery");
                    var battery_percent = (((parseInt(contact[30]) - 117) +26) *3.85);
                    BatteryLevel.innerHTML = parseInt(battery_percent) + "%";
                    reset_baseline = true;
                }
            }
            
            reset_counter +=1 ;
            if (reset_counter > 55) {
                //Counter to Reset Baseline.
                reset_baseline = true;  
                reset_counter = 0;
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

                //Epoc+ Data.   
                if (manualControl) {
                    // Plot single Floating Point value.
                    if (formatType == 0) {
                        var optionValue = document.getElementById("CySelect").value;
                        if (optionValue == "Select Sensor") { return; }
                        var selectedContact = parseInt(optionValue); 
                        var myContact = parseInt(sensorDATA['epoc'][selectedContact]);
                        var value_data = parseFloat(contact[myContact]);
                        drawdot(myContact, 100, cy_x, (value_data - baseline[myContact]) * eeg_resolution, "white");
                    }
                    // Plot single Raw value.
                    else {
                        if (contact.length < 32) { return; }
                        var optionValue = document.getElementById("CySelect").value;
                        if (optionValue == "Select Sensor") { return; }
                        var selectedContact = parseInt(optionValue);
                        var myContact = selectedContact;
                        
                        var value_1 = contact[selectedContact];
                        var value_2 = contact[(selectedContact +1)];
                        var value_data = convertEPOC_PLUS(parseInt(value_1), parseInt(value_2));

                        drawdot(myContact, 50, cy_x, (value_data - baseline[selectedContact]) * eeg_resolution, "white");
                    }
                }
                else {
                    //Plot Multiple Float Point values.
                    if (formatType == 0) {
                        /* Quality Data Code.
                        if ((4 % reset_counter) == 4) {
                            rms_counter += 1;
                            if (baseline[1] == null) { return; }
                            if (rmsIndex < 4) {
                                rmsIndex += 1;
                            }
                            else {
                                rmsIndex = -1;
                                if (mean[1] == null) { 
                                    for (var i = 2; i < (contact.length -4); i++) {
                                        mean[i] = 0;
                                        //baseline[i] = 4201.008546986665;
                                    }
                                }
                                
                                
                                for (var zIndex = 0; zIndex < 4; zIndex++) { 
                                    
                                    for (var i = 2; i < (contact.length -4); i++) {
                                        
                                        mean[i] = ((mean[i] + (rms[zIndex][i])));
                                        
                                        if (zIndex == 3) {
                                            mean[i] = roundToTwo((mean[i] / 4));
                                            
                                        }
                                        
                                    }
                                    
                                }

                            if (rms_counter > 10) { 
                                console.log(mean);
                            }
                                                                            
                                return;
                            }
                            
                            if (rms[rmsIndex] == null) { rms[rmsIndex] = contact; }
                            for (var i = 2; i < (contact.length -4); i++) {
                                
                                rms[rmsIndex][i] = Math.sqrt(eval((baseline[i] - contact[i]) * eeg_resolution)); 
                            }
                        
                        }
                        */
                        
                        var arr_element;
                        var inc_y_offset = 10;
                        var inc_step = (sensorNAME['epoc'].length +1);
                        for (arr_element in sensorNAME['epoc']) {
                            if (arr_element == 1) { continue; }
                            var c = document.getElementById("e." + sensorNAME['epoc'][arr_element]);
                            var myColor = sensorDATA_color[arr_element];
                            inc_y_offset += Math.abs(parseInt((canvasHeight / inc_step)));
                            if (c.checked == true) {
                                select_contact = parseInt(sensorDATA['epoc'][arr_element]);
                                var value_data = (baseline[select_contact] - parseFloat(contact[select_contact]));
                                var value_floor = Math.floor((baseline[select_contact] / 1000.0))
                                drawdot(select_contact, inc_y_offset, cy_x, value_floor - (value_data * .128), myColor);
                            }
                        }
                    }
                    //Plot Multiple Raw Data values.
                    else {
                        var arr_element;
                        var inc_y_offset = 10;
                        var inc_step = (sensorNAME['epoc'].length +1);
                        var v = 0;
                        for (var i = 2; i < (contact.length -4); i+=2) {
                            v += 1;
                            
                            var c = document.getElementById("e." + sensorNAME['epoc'][v]);
                            var myColor = sensorDATA_color[v];
                            inc_y_offset += Math.abs(parseInt((canvasHeight / inc_step)));
                            if (c.checked == true) {

                                
                                
                                var value_1 = contact[i];

                                var value_2 = contact[(i +1)];
                                
                                var value_data = convertEPOC_PLUS(parseInt(value_1), parseInt(value_2));
                                
                                //var value_data = Math.abs(parseFloat(contact[select_contact]) - (baseline[select_contact]));
                                drawdot(v, inc_y_offset, cy_x, (value_data - baseline[v]) * eeg_resolution, myColor);
                            }
                        }
                    }
                }
                
                // Reset Baselines:::Epoc+
                if (contact[1] == "16") {
                    if (baseline[1] == null || reset_baseline == true) {
                        //console.log("Reset Baseline.");
                        if (manualControl) {          
                            if (formatType == 0) {
                                //Baseline for Floating Point. Single data stream.
                                i = myContact;
                                if (init_baseline == false) {
                                    baseline[i] = baseline[i] + Math.abs(value_data) + 4201.02564096001;
                                    baseline[i] = (baseline[i] / 3);
                                }
                                else {
                                    baseline[i] = Math.abs(value_data);
                                }
                            }
                            else {
                                //Baseline for Raw Data integers. Single data stream.
                                if (init_baseline == false) {
                                    baseline[i] = baseline[i] + Math.abs(value_data);
                                    baseline[i] = parseInt((baseline[i] / 2));
                                }
                                else {
                                    baseline[i] = Math.abs(value_data);
                                }
                            }
                        }
                        else {
                            //Baseline for Floating Point. Multiple data streams.
                            if (formatType == 0) {
                                var device_name = headset[selected_model].replace('epoc_plus','epoc');
                                for (arr_element in sensorNAME[device_name]) {
                                    select_contact = parseInt(sensorDATA[device_name][arr_element])
                                    if (init_baseline == false) {
                                        baseline[select_contact] = baseline[select_contact] + parseFloat(contact[select_contact]) + 4201.02564096001;
                                        baseline[select_contact] = (baseline[select_contact] / 3);
                                    }
                                    else {
                                        baseline[select_contact] = Math.abs(parseFloat(contact[select_contact]));
                                    }
                                }
                            }
                            else {
                                    //Baseline for Raw Data Integers. Multiple data streams.
                                    for (var i = 0; i < 33; i++) {
                                        if (init_baseline == false) {
                                            baseline[i] = baseline[i] + Math.abs(value_data);
                                            baseline[i] = parseInt((baseline[i] / 2));
                                        }
                                        else {
                                            baseline[i] = Math.abs(value_data);
                                        }
                                    }
                                }
                            }
                            
                        }
                        reset_baseline = false;
                        init_baseline = false;
                    }
               
                                
                
                // Epoc+ Gyro
                if (contact[1] == "32") {
                   /*
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
                    //init_baseline = false;
                    }       
                    if (manualControl) {                 
                        var myContact = document.getElementById("CySelect").value;
                        var myValue = 127+ Math.abs(contact[myContact]);
                
                        drawdot(myContact, 50, cy_x, ((eval(myValue) - baseline[myContact]) * .3)  + 10, "white");

                    }
                    */
                }
            }
        }   
    }
});

// Record Start Button.
document.getElementById('cyStartRecord').onclick = function(e) {
    client.sendData("CyKITv2:::RecordStart:::" + document.getElementById('cyRecordFile').value); 
}
// Record Stop Button.
document.getElementById('cyStopRecord').onclick = function(e) {
    client.sendData("CyKITv2:::RecordStop");
}

// Connect Button.
document.getElementById('cyConnect').onclick = function(e) {
    client.connect();
}

// Disconnect Button.
document.getElementById('cyDisconnect').onclick = function(e) {
    var cyPicture = document.getElementById("CyKIT-picture");
    cyPicture.style.backgroundImage = "url('./images/CyKITv2-bg-off.png')";
    
    var selectEPOC = document.getElementById("select.Epoc");
    var selectINSIGHT = document.getElementById("select.Insight");
    
    selectEPOC.style.visibility = 'hidden';
    selectINSIGHT.style.visibility = 'hidden';
    client.close();
}

// Change Get_Level mask in emotiv.py
document.getElementById('maskChange').onclick = function(e) {
    client.sendData("CyKITv2:::setMask:::" + document.getElementById('CyMask').value + ":::" + document.getElementById('newMask').value);
    reset_baseline = true;  
}

