function btnAction()
{var express = require('express');
var app = express();
var fs = require("fs");
var multer  = require('multer');
app.use('/public',express.static('public'));
app.use(multer({ dest: '/text/'}).array('text'));
app.post('/file_upload',function (req, res) {
    fs.readFile( req.files[0].path, function (err, data) {
        var des_file = __dirname + "/public/text/" + req.files[0].originalname;
        fs.writeFile(des_file, data, function (err) {
            if(err){
                console.log( err );
            }else{
               var response = {
                    message:'文件上传成功',
                    filename:req.files[0].originalname
                };
            }
            res.send( JSON.stringify( response ) );
        });
    });
})
var server = app.listen(8081, function () {
    var host = server.address().address;
    var port = server.address().port;
    console.log("http://127.0.0.1:5500/", host, port)
})}