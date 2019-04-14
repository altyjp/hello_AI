/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

var graph = undefined;

function postImg(){
    var raw_sendData = document.getElementById('canvassample');
    
    if(!raw_sendData){
        console.log("get canvas Data FAILD");
        $("#result").html( "<h2>" + "ERROR. send failed</h2>");
        return -1;
    }
    
    //ボタンの無効化
    $("#canvas_ctrl_clear").css('background-color','silver');
    $("#canvas_ctrl_start").css('background-color','silver');
    $("#canvas_ctrl_clear").prop("disabled", true);
    $("#canvas_ctrl_start").prop("disabled", true);
    
    $("#result").html( "<h2>sending...</h2>");
    var sendData = {};
    sendData["img"] = raw_sendData.toDataURL();
    
    $.post("/image_recognition",sendData)
            .done(
                function(data){
                var max = Math.max.apply(null, data);
                var highestIndx = data.indexOf(max);

                $("#result").html( "<h2>" + "result:" + highestIndx + "</h2>");

                drawGraph(data);
                $("#result_graph").show("fast");

                //ボタンの有効化
                $("#canvas_ctrl_clear").css('background-color','#ff0033');
                $("#canvas_ctrl_start").css('background-color','#3399ff');
                $("#canvas_ctrl_clear").prop("disabled", false);
                $("#canvas_ctrl_start").prop("disabled", false);
            })
            .fail(function(jqXHR, textStatus, errorThrown){
                $("#result").html( "<h2>ERROR:Link failed. please retry.</h2>");
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
                //ボタンの有効化
                $("#canvas_ctrl_clear").css('background-color','#ff0033');
                $("#canvas_ctrl_start").css('background-color','#3399ff');
                $("#canvas_ctrl_clear").prop("disabled", false);
                $("#canvas_ctrl_start").prop("disabled", false);
            });
    
    
}

function drawGraph(Data){
    var chartChart = document.getElementById("result_graph");
    destroyGraph();
    graph = new Chart(chartChart, {
        type: 'bar',
        data: {
            labels: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
            datasets: [{
                label: 'degree of similarity',
                data: Data,
                backgroundColor: '#FF6384'
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}

function destroyGraph(){
    if(graph){
        graph.destroy();
    }
}