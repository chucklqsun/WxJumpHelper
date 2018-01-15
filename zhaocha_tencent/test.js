var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var md5 = require('./md5.js').exports;
var fs = require('fs');

var resID = 1666;   //replace with other resID of image

var GetKey = function (e) {
    e += "QQGameZC";
    for (var t = md5.hash(e, !0), o = new ArrayBuffer(16), a = new Uint8Array(o), n = 0; n < 16; n++)a[n] = t.charCodeAt(n);
    console.log("Key is "+a);
    return a
};
var DecryptFile =  function (r, e) {
    for (var t = GetKey(r), o = 0; o < e.length; o += t.length)for (var a = 0; o + a < e.length && a < t.length; ++a)e[o + a] ^= t[a];
    return e;
};

var url = "https://zhaocha.qq.com/resource/zhaocha/"+ Math.floor(resID / 1e4) +"/"+ resID +"/mixed_image.dat";
var request = require('xhr-request');

request(url, {
    method: 'GET',
    responseType: 'arraybuffer'
}, function (err, data) {
    if (err) throw err
    var arrayBuffer = data;
    if (arrayBuffer) {
        var byteArray = new Uint8Array(arrayBuffer);
        var picarray = DecryptFile(resID, byteArray);
        var all = fs.createWriteStream("./"+resID+".png");
        all.write(picarray);
        all.end();
    }else{
        console.log("arrayBuffer failed");
    }
});
