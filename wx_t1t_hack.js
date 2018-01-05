var CryptoJS = require('crypto-js');
var request = require('request-promise');
var sleep = require('sleep');

/*
 * npm install crypto-js request-promise request sleep
 * node wx_t1t_hack.js
 */

function encrypt (text, originKey) {
    originKey = originKey.slice(0, 16);
    var key = CryptoJS.enc.Utf8.parse(originKey),
        iv = CryptoJS.enc.Utf8.parse(originKey),
        msg = JSON.stringify(text);
    var ciphertext = CryptoJS.AES.encrypt(msg, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return ciphertext.toString()
}

function extend (target) {
    var sources = [].slice.call(arguments, 1);
    sources.forEach(function (source) {
        for (var prop in source) {
            target[prop] = source[prop]
        }
    });
    return target
}

var score_you_want = 218;
var version = 6,
    score = Math.round(score_you_want+Math.random()*20),
    // replace with your session_id here
    session_id = 'xxxxxxxx';

var headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C153 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx7c8d593b2c3a7703/' + version + '/page-frame.html',
    'Content-Type': 'application/json',
    'Accept-Language': 'zh-cn',
    'Accept': '*/*'
};
var base_req = {
    'base_req': {
        'session_id': session_id,
        'fast': 1
    }
};
var base_site = 'https://mp.weixin.qq.com/wxagame/';

var path = 'wxagame_getuserinfo';
request({
    method: 'POST',
    url: base_site + path,
    headers: headers,
    json: true,
    body: base_req
}).then(function (response) { 
    // console.log(path, response) 
});

path = 'wxagame_getfriendsscore';
request({
    method: 'POST',
    url: base_site + path,
    headers: headers,
    json: true,
    body: base_req
}).then(function (response) {
    var times = response.my_user_info.times + 1,
        path = 'wxagame_init';
    request({
        method: 'POST',
        url: base_site + path,
        headers: headers,
        json: true,
        body: extend({}, {version: 9}, base_req)
    }).then(function (response) {
        // console.log(path, response)
        var seed = Date.now();
        var action = [],
            musicList = [],
            touchList = [],
            steps = [],
            timestamp = [];
        for(var i=Math.round(score_you_want+Math.random()*20);i>0;i--){
            console.log(i);
            var duration = Math.random().toFixed(3);
            var holdTime = (Math.random()*2).toFixed(2);
            var delta = duration*1000+holdTime*1000;
            action.push([duration,holdTime,i%8===0]);
            musicList.push(false);
            var touch_x = (250-Math.random()*10).toFixed(4);
            var touch_y= (670-Math.random()*20).toFixed(4);
            touchList.push([touch_x, touch_y]);
            var step = [];
            step.push(touch_x);
            step.push(touch_y);
            steps.push(step);
            sleep.msleep(delta);
            timestamp.push(Date.now())
        }
        var data = {
            score: score,
            times: times,
            game_data: JSON.stringify({
                seed: seed,
                action: action,
                musicList: musicList,
                touchList: touchList,
                steps : steps,
                timestamp: timestamp,
                version: 2
            })
        };
        path = 'wxagame_settlement';
        request({
            method: 'POST',
            url: base_site + path,
            headers: headers,
            json: true,
            body: extend({}, {action_data: encrypt(data, session_id)}, base_req)
        }).then(function (response) {
            console.log(path, response);
            console.log('2018! Happy new year! 🎉')
        }).catch(function (error) {
            console.log(error)
        })
    })
}).catch(function (error) {
    console.log(error);
    console.log('something crash')
});
