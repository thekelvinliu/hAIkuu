var wordlist = null;

$( document ).ready(function() {
    hideuploads();
    $("#outputImage").hide();
    $("#inputImage").on("change", function () {
        var file = document.getElementById("inputImage").files[0];
        var blob_url = window.URL.createObjectURL(file);
        $("#outputImage").attr("src", blob_url);
        $("#outputImage").css("width",300);
        $("#outputImage").show();
        wordlist = null;
        $("#generate").unbind('click').on("click", function() {
            createHaiku(blob_url)
        });
    });
    $("#useURL").on("click", function () {
        var file = document.getElementById("inputImage").files[0];
        var blob_url = window.URL.createObjectURL(file);
        $("#outputImage").attr("src", $("#url").val());
        $("#outputImage").css("width",300);
        $("#outputImage").show();
        wordlist = null;
        $("#generate").unbind('click').on("click", createHaikuURL);
    }); 
    $(".listbutton").on("click", function () {
        hideuploads();
        $(this.dataset.target).show();
        if (this.dataset.target == "#wordUpload") {
            $("#generate").unbind('click').on("click", function() {
            createHaikuWords()
            });
        } else {
            $("#imageWrapper").show();
        }
    })
});

var createHaikuWords = function () {
    $("#loading").show();
    $("#haiku").empty();
    wordlist = $("#keywordinput").val().split(",");
    for (var i = 0; i < wordlist.length; i++) {
        wordlist[i] = wordlist[i].toLowerCase().trim();
    };
    generateHaiku();
}

var createHaikuURL = function () {
    $("#loading").show();
    $("#haiku").empty();
    $.ajax({
          headers: {authorization: "Bearer brwV2MxCkjH7J5Jai8gZ8JaxIHCdWT"},
          url: "https://api.clarifai.com/v1/tag?url=" + $("#url").val(),
          type: "get"
        })
        .success(function (data) {
             wordlist = data.results[0].result.tag.classes;
             generateHaiku(data);
        })
}
var hideuploads = function () {
    $("#imageUpload").hide();
    $("#urlUpload").hide();
    $("#wordUpload").hide();
    $("#imageWrapper").hide();
}

var createHaiku = function(blob_url) {
    $("#loading").show();
    $("#haiku").empty();
    
    if (wordlist == null) {
        convertToDataURLviaCanvas(blob_url, function(base64Img){
            // Base64DataURL
            $.ajax({
              headers: {authorization: "Bearer brwV2MxCkjH7J5Jai8gZ8JaxIHCdWT"},
              url: "https://api.clarifai.com/v1/tag",
              type: "post",
              data: {encoded_image:base64Img.substring(base64Img.indexOf(",") + 1)}
            })
            .success(function (data) {
                 wordlist = data.results[0].result.tag.classes;
                 generateHaiku(data);
            })
        });
    } else {
        generateHaiku(wordlist);
    }
}

var generateHaiku = function () {
    $.ajax({
      url: window.location.protocol + "//" + window.location.host + "/"+ "haiku",
      type: "post",
      data: JSON.stringify({"keywords" : wordlist}),
      contentType : "application/json; charset=utf-8"
    })
    .success(function (data) {
        $("#haiku").html("<h2>" + data.split('/').join(", <br />") + "</h2>");
        $("#loading").hide();
    })
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
        if (canvas.height > 400 || canvas.width > 400) {
            canvas = downScaleCanvas(canvas, 0.3);
        }
        dataURL = canvas.toDataURL(outputFormat);
        callback(dataURL);
        canvas = null; 
    };
    img.src = url;
}

function downScaleCanvas(cv, scale) {
    if (!(scale < 1) || !(scale > 0)) throw ('scale must be a positive number <1 ');
    var sqScale = scale * scale; // square scale = area of source pixel within target
    var sw = cv.width; // source image width
    var sh = cv.height; // source image height
    var tw = Math.floor(sw * scale); // target image width
    var th = Math.floor(sh * scale); // target image height
    var sx = 0, sy = 0, sIndex = 0; // source x,y, index within source array
    var tx = 0, ty = 0, yIndex = 0, tIndex = 0; // target x,y, x,y index within target array
    var tX = 0, tY = 0; // rounded tx, ty
    var w = 0, nw = 0, wx = 0, nwx = 0, wy = 0, nwy = 0; // weight / next weight x / y
    // weight is weight of current source point within target.
    // next weight is weight of current source point within next target's point.
    var crossX = false; // does scaled px cross its current px right border ?
    var crossY = false; // does scaled px cross its current px bottom border ?
    var sBuffer = cv.getContext('2d').
    getImageData(0, 0, sw, sh).data; // source buffer 8 bit rgba
    var tBuffer = new Float32Array(3 * tw * th); // target buffer Float32 rgb
    var sR = 0, sG = 0,  sB = 0; // source's current point r,g,b
    /* untested !
    var sA = 0;  //source alpha  */    

    for (sy = 0; sy < sh; sy++) {
        ty = sy * scale; // y src position within target
        tY = 0 | ty;     // rounded : target pixel's y
        yIndex = 3 * tY * tw;  // line index within target array
        crossY = (tY != (0 | ty + scale)); 
        if (crossY) { // if pixel is crossing botton target pixel
            wy = (tY + 1 - ty); // weight of point within target pixel
            nwy = (ty + scale - tY - 1); // ... within y+1 target pixel
        }
        for (sx = 0; sx < sw; sx++, sIndex += 4) {
            tx = sx * scale; // x src position within target
            tX = 0 |  tx;    // rounded : target pixel's x
            tIndex = yIndex + tX * 3; // target pixel index within target array
            crossX = (tX != (0 | tx + scale));
            if (crossX) { // if pixel is crossing target pixel's right
                wx = (tX + 1 - tx); // weight of point within target pixel
                nwx = (tx + scale - tX - 1); // ... within x+1 target pixel
            }
            sR = sBuffer[sIndex    ];   // retrieving r,g,b for curr src px.
            sG = sBuffer[sIndex + 1];
            sB = sBuffer[sIndex + 2];

            /* !! untested : handling alpha !!
               sA = sBuffer[sIndex + 3];
               if (!sA) continue;
               if (sA != 0xFF) {
                   sR = (sR * sA) >> 8;  // or use /256 instead ??
                   sG = (sG * sA) >> 8;
                   sB = (sB * sA) >> 8;
               }
            */
            if (!crossX && !crossY) { // pixel does not cross
                // just add components weighted by squared scale.
                tBuffer[tIndex    ] += sR * sqScale;
                tBuffer[tIndex + 1] += sG * sqScale;
                tBuffer[tIndex + 2] += sB * sqScale;
            } else if (crossX && !crossY) { // cross on X only
                w = wx * scale;
                // add weighted component for current px
                tBuffer[tIndex    ] += sR * w;
                tBuffer[tIndex + 1] += sG * w;
                tBuffer[tIndex + 2] += sB * w;
                // add weighted component for next (tX+1) px                
                nw = nwx * scale
                tBuffer[tIndex + 3] += sR * nw;
                tBuffer[tIndex + 4] += sG * nw;
                tBuffer[tIndex + 5] += sB * nw;
            } else if (crossY && !crossX) { // cross on Y only
                w = wy * scale;
                // add weighted component for current px
                tBuffer[tIndex    ] += sR * w;
                tBuffer[tIndex + 1] += sG * w;
                tBuffer[tIndex + 2] += sB * w;
                // add weighted component for next (tY+1) px                
                nw = nwy * scale
                tBuffer[tIndex + 3 * tw    ] += sR * nw;
                tBuffer[tIndex + 3 * tw + 1] += sG * nw;
                tBuffer[tIndex + 3 * tw + 2] += sB * nw;
            } else { // crosses both x and y : four target points involved
                // add weighted component for current px
                w = wx * wy;
                tBuffer[tIndex    ] += sR * w;
                tBuffer[tIndex + 1] += sG * w;
                tBuffer[tIndex + 2] += sB * w;
                // for tX + 1; tY px
                nw = nwx * wy;
                tBuffer[tIndex + 3] += sR * nw;
                tBuffer[tIndex + 4] += sG * nw;
                tBuffer[tIndex + 5] += sB * nw;
                // for tX ; tY + 1 px
                nw = wx * nwy;
                tBuffer[tIndex + 3 * tw    ] += sR * nw;
                tBuffer[tIndex + 3 * tw + 1] += sG * nw;
                tBuffer[tIndex + 3 * tw + 2] += sB * nw;
                // for tX + 1 ; tY +1 px
                nw = nwx * nwy;
                tBuffer[tIndex + 3 * tw + 3] += sR * nw;
                tBuffer[tIndex + 3 * tw + 4] += sG * nw;
                tBuffer[tIndex + 3 * tw + 5] += sB * nw;
            }
        } // end for sx 
    } // end for sy

    // create result canvas
    var resCV = document.createElement('canvas');
    resCV.width = tw;
    resCV.height = th;
    var resCtx = resCV.getContext('2d');
    var imgRes = resCtx.getImageData(0, 0, tw, th);
    var tByteBuffer = imgRes.data;
    // convert float32 array into a UInt8Clamped Array
    var pxIndex = 0; //  
    for (sIndex = 0, tIndex = 0; pxIndex < tw * th; sIndex += 3, tIndex += 4, pxIndex++) {
        tByteBuffer[tIndex] = Math.ceil(tBuffer[sIndex]);
        tByteBuffer[tIndex + 1] = Math.ceil(tBuffer[sIndex + 1]);
        tByteBuffer[tIndex + 2] = Math.ceil(tBuffer[sIndex + 2]);
        tByteBuffer[tIndex + 3] = 255;
    }
    // writing result to canvas.
    resCtx.putImageData(imgRes, 0, 0);
    return resCV;
}