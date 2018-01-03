var CryptoJS = require('crypto-js')
var request = require('request-promise')

/*
 * npm install crypto-js request-promise request
 * node wx_t1t_hack.js
 */

// export function testEncription(msg, fullKey) {
//   var fullKey = fullKey.slice(0, 16)
//   var key = CryptoJS.enc.Utf8.parse(fullKey)
//   var iv = CryptoJS.enc.Utf8.parse(fullKey)

//   var passWord = CryptoJS.AES.encrypt(msg, key, { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 })
//   var base64 = passWord.toString()

//   console.log('passWord', passWord)
//   console.log('sessionId', sessionId)
//   console.log('key', key)
//   console.log('base64', base64)

//   var bytes = CryptoJS.AES.decrypt(base64, key, {
//     iv: iv
//   });
//   console.log('bytes', bytes)
//   var plaintext = CryptoJS.enc.Utf8.stringify(bytes);
//   console.log('plaintext', plaintext)
// }

function encrypt (text, originKey) {
    var originKey = originKey.slice(0, 16),
        key = CryptoJS.enc.Utf8.parse(originKey),
        iv = CryptoJS.enc.Utf8.parse(originKey),
        msg = JSON.stringify(text)
    var ciphertext = CryptoJS.AES.encrypt(msg, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return ciphertext.toString()
}

function decrypt (text, originKey) {
    var originKey = originKey.slice(0, 16),
        key = CryptoJS.enc.Utf8.parse(originKey),
        iv = CryptoJS.enc.Utf8.parse(originKey)
    var bytes = CryptoJS.AES.decrypt(text, key, {
        iv: iv
    })
    var plaintext = CryptoJS.enc.Utf8.stringify(bytes)
    return plaintext
}

function extend (target) {
    var sources = [].slice.call(arguments, 1)
    sources.forEach(function (source) {
        for (var prop in source) {
            target[prop] = source[prop]
        }
    })
    return target
}


var version = 5,
    score = Math.round(10000+Math.random()*2000),
    // replace with your session_id here
    session_id = 'xxxxxxxx'

var headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C153 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx7c8d593b2c3a7703/' + version + '/page-frame.html',
    'Content-Type': 'application/json',
    'Accept-Language': 'zh-cn',
    'Accept': '*/*'
}
var base_req = {
    'base_req': {
        'session_id': session_id,
        'fast': 1
    }
}
var base_site = 'https://mp.weixin.qq.com/wxagame/'

var path = 'wxagame_getuserinfo'
request({
    method: 'POST',
    url: base_site + path,
    headers: headers,
    json: true,
    body: base_req
}).then(function (response) { 
    // console.log(path, response) 
})

path = 'wxagame_getfriendsscore'
request({
    method: 'POST',
    url: base_site + path,
    headers: headers,
    json: true,
    body: base_req
}).then(function (response) {
    // console.log(response.my_user_info)
    var times = response.my_user_info.times + 1
    path = 'wxagame_init'
    request({
        method: 'POST',
        url: base_site + path,
        headers: headers,
        json: true,
        body: extend({}, {version: 9}, base_req)
    }).then(function (response) {
        // console.log(path, response)
        var action = [],
            musicList = [],
            touchList = []
        for(var i=Math.round(12000+Math.random()*2000);i>0;i--){
            action.push([Math.random().toFixed(3),(Math.random()*2).toFixed(2),i/5000==0?true:false]);
            musicList.push(false);
            touchList.push([(250-Math.random()*10).toFixed(4),(670-Math.random()*20).toFixed(4)]);
        }
        //for (var i = 0; i < score; i++) {
        //    action.push([0.752, 1.32, false])
        //    musicList.push(false)
        //    touchList.push([185, 451])
        //}
        var data = {
            score: score,
            times: times,
            game_data: JSON.stringify({
                seed: Date.now(),
                action: action,
                musicList: musicList,
                touchList: touchList,
                version: 1
            })
        }
        path = 'wxagame_settlement'
        request({
            method: 'POST',
            url: base_site + path,
            headers: headers,
            json: true,
            body: extend({}, {action_data: encrypt(data, session_id)}, base_req)
        }).then(function (response) {
            console.log(path, response)
            console.log('2018! Happy new year! 🎉')
        }).catch(function (error) {
            console.log(error)
        })
    })
}).catch(function (error) {
    console.log('something crash')
})
