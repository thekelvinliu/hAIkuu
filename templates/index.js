$( document ).ready(function() {

	resizeDiv();
	$( window ).resize(
		resizeDiv
		);
	$("#inputImage").on("change", function () {
		var file = document.getElementById("inputImage").files[0];
		var blob_url = window.URL.createObjectURL(file);
		$("#outputImage").attr("src", blob_url)
		$("#outputImage").show();
		convertToDataURLviaCanvas(blob_url, function(base64Img){
		    // Base64DataURL
		    $.ajax({
			  headers: {authorization: "Bearer UhaCGlZ2mOM34YkXSYQaWeGbgb8qRc"},
			  url: "https://api.clarifai.com/v1/tag",
			  type: "post",
			  data: {encoded_image:base64Img.substring(base64Img.indexOf(",") + 1)}
			})
			.success(function (data) {
			 console.log(data)
			})
		});
	})
});

var resizeDiv = function () {
	$("#outputImage").css("width", $( window ).height()*0.5);
	$("#mainDiv").height($( window ).height()*0.8)
	$("#mainDiv").width($( window ).width()*0.8)
	$("#mainDiv").css(
		{
			top: ($( window ).height()/2 - $("#mainDiv").height()/2), 
			left: ($( window ).width()/2 - $("#mainDiv").width()/2)
		});
}

var convertToDataURLviaCanvas = function (url, callback, outputFormat){
    var img = new Image();
    img.crossOrigin = 'Anonymous';
    img.onload = function(){
        var canvas = document.createElement('CANVAS');
        var ctx = canvas.getContext('2d');
        var dataURL;
        canvas.height = this.height;
        canvas.width = this.width;
        ctx.drawImage(this, 0, 0);
        dataURL = canvas.toDataURL(outputFormat);
        callback(dataURL);
        canvas = null; 
    };
    img.src = url;
}