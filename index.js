/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
const execSync = require('child_process').execSync;

var fs = require('fs');
var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var path = require('path');


app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static('html'));


var server = app.listen(8080, function(){
    console.log("Node.js is listening to PORT:" + server.address().port);
});

// クライアント側でAPI
app.post("/image_recognition", function(req, res, ){
    
    body_img = req.body['img'];
    
    const base64Data = body_img.split(',')[1];
    const decode = new Buffer.from(base64Data,'base64');
    const png_fileName = generateUuid() + '.png';
    const png_filepath = 'posted_img/' + png_fileName;
    
    var abspath = path.resolve('posted_img/');
    
    fs.writeFileSync(png_filepath, decode);
    const result =  execSync('python python_lib/start_NN_2.py ' +
                                          abspath+ '/' + png_fileName).toString();
    data = JSON.parse(result);
    res.send(data);
    
    fs.unlink(png_filepath, function (err) {
                if(err){
                    throw err;
                }
            }
    );
    
});

//UUIDジェネレータ
function generateUuid() {
    // https://github.com/GoogleChrome/chrome-platform-analytics/blob/master/src/internal/identifier.js
    // const FORMAT: string = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx";
    let chars = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".split("");
    for (let i = 0, len = chars.length; i < len; i++) {
        switch (chars[i]) {
            case "x":
                chars[i] = Math.floor(Math.random() * 16).toString(16);
                break;
            case "y":
                chars[i] = (Math.floor(Math.random() * 4) + 8).toString(16);
                break;
        }
    }
    return chars.join("");
}