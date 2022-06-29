// function btnAction()
// {var express = require('express');
// var app = express();
// var fs = require("fs");
// var multer  = require('multer');
// app.use('/',express.static(''));
// app.use(multer({ dest: '/'}).any());
// app.post('/',function (req, res) {
//     fs.readFile( req.files[0].path, function (err, data) {
//         var des_file = __dirname + "/" + req.files[0].originalname;
//         fs.writeFile(des_file, data, function (err) {
//             if(err){
//                 console.log( err );
//             }else{
//                var response = {
//                     message:'文件上传成功',
//                     filename:req.files[0].originalname
//                 };
//             }
//             res.send( JSON.stringify( response ) );
//         });
//     });
// })
// var server = app.listen(8081, function () {
//     var host = server.address().address;
//     var port = server.address().port;
//     console.log("http://127.0.0.1:5500/", host, port)
// })}
//点击普通按钮


function openFileDialog()
		{
			//模拟鼠标点击事件
			$(".filebutton").click();
		}

		// 用户选择了一个文件 onchange事件被触发
		function fileSelected()
		{
			var fbutton = $(".filebutton")[0];  //DOM
			var file = fbutton.files[0];   //fbutton.files可能一次选择了多个文件
			fbutton.value = "";  //清空选择
			startUpload(file);   //开始上传
		}

		// 开始上传, 参数为 File 对象
		function startUpload( file )
		{
			var uploadUrl = "http://127.0.0.1:8080/";

			// 手工构造一个 form 对象
			var formData = new FormData();
			formData.append('file', file); // 'file' 为HTTP Post里的字段名, file 对浏览器里的File对象

			// 手工构造一个请求对象，用这个对象来发送表单数据
			// 设置 progress, load, error, abort 4个事件处理器
		    var request = new XMLHttpRequest();
		    request.upload.addEventListener("progress", window.evt_upload_progress, false);
		    request.addEventListener("load", window.evt_upload_complete, false);
		    request.addEventListener("error", window.evt_upload_failed, false);
		    request.addEventListener("abort", window.evt_upload_cancel, false);
			request.open("POST", uploadUrl ); // 设置服务URL
		    request.send(formData);  // 发送表单数据
		}

		window.evt_upload_progress = function (evt)
		{
		    if (evt.lengthComputable)
		    {
		    	var progress = Math.round(evt.loaded * 100 / evt.total);
		    	console.log ("上传进度: " + progress);
		    }
		};
		window.evt_upload_complete = function (evt)
		{
			if(evt.loaded == 0)
			{
				console.log ("上传失败!");
			}
			else
			{
				console.log("上传完成!");
		    	var response = JSON.parse(evt.target.responseText);
		   		console.log (response);
			}
		};
		window.evt_upload_failed = function (evt)
		{
			console.log  ("上传出错");
		};
		window.evt_upload_cancel = function (evt)
		{
			console.log( "上传中止!");
		};


		
	function submitForm(){
				// 得到文本框的值
				var query = document.getElementById("query").value;
				//判断是否为空
				if( isEmpty(query) ){ //为空
					// 设置提示信息(设置span元素的值)
					document.getElementById("msg").innerHTML = "*Query不能为空!";

					// 阻止表单提交
					return;
				}

				// 手动提交表单
				document.getElementById("queryform").submit();
			}
	function isEmpty(str){
				// 判断是否为空
				if(str == null || str.trim() == "") {
					return true;
				}
				return false;
			}
