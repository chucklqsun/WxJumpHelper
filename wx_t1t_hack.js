var CryptoJS = require('crypto-js');
var request = require('request-promise');
var sleep = require('sleep');

/*
 * npm install crypto-js request-promise request sleep
 * node wx_t1t_hack.js
 */
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

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

function wxagame_bottlereport(game_start, game_over, best_score, times){
    game_start = Math.floor(game_start/1000);
    game_over = Math.floor(game_over/1000);
    console.log("begin bottle report");
    var data = {
        base_req: {
            session_id: session_id,
            fast: 1,
            client_info: {
                platform: "android",
                brand: "Xiaomi",
                model: "MI 5s",
                system: "Android 7.0"
            }
        },
        report_list : []
    };
    var duration = getRandomInt(1,10);
    var duration2 = getRandomInt(1,10);

    var t = {
        ts: game_start-duration-duration2,
        type: 0,
        scene: 1089
    };
    data.report_list.push(t);

    t = {
        ts: game_start-duration2,
        type: 10
    };
    data.report_list.push(t);

    t = {
        ts: game_over,
        type: 2,
        score: score,
        best_score: best_score,
        break_record: score > best_score ? 1:0,
        duration: duration2,
        times: times
    };
    data.report_list.push(t);

    var quitReportTime = Math.floor(Date.now()/1000);
    t = {
        ts : quitReportTime,
        type: 1,
        duration: quitReportTime - game_over
    };
    data.report_list.push(t);

    console.log(data);
    path = 'wxagame_bottlereport';
    request({
        method: 'POST',
        url: base_site + path,
        headers: headers,
        json: true,
        body: extend({}, data)
    }).then(function (response) {
        console.log(path, response);
        console.log('bottleReport Posted')
    }).catch(function (error) {
        console.log(error)
    })
}

function wxagame_settlement(best_score,times){
    var seed = Date.now();
    var action = [],
        musicList = [],
        touchList = [],
        steps = [],
        timestamp = [];
    var game_over = 0;
    for(var i=score;i>0;i--){
        console.log(i);
        var duration = Math.random().toFixed(getRandomInt(2,3));
        var calY = (-1.9932*duration+2.7486).toFixed(2);
        var delta = duration*1000+calY*1000+getRandomInt(1,300);
        action.push([duration,calY,false]); //false for quick, which < 800ms between 2 steps
        musicList.push(false);
        var touch_x = (getRandomInt(100,200)-Math.random()*20).toFixed(getRandomInt(0,3));
        var touch_y = (getRandomInt(300,600)-Math.random()*30).toFixed(getRandomInt(0,3));
        touchList.push([parseFloat(touch_x), parseFloat(touch_y)]);
        var step = [];
        for(var s =0;s<5;++s) {
            step.push(parseFloat(touch_x));
            step.push(parseFloat(touch_y));
        }
        steps.push(step);
        sleep.msleep(delta);
        game_over = Date.now();
        timestamp.push(game_over)
    }
    wxagame_bottlereport(seed, game_over, best_score, times);
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
    console.log(data);
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
}

var score_you_want = 10; //replace with the score you want post
var version = 6,
    score = Math.round(score_you_want+Math.random()*20),
    // replace with your session_id here
    session_id = 'xxxxxxxx';

var headers = {
    'User-Agent': 'MicroMessenger/6.6.1.1220(0x26060133) NetType/WIFI Language/en',
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
    console.log(response);
    var best_score = response.my_user_info.history_best_score;
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
        wxagame_settlement(best_score,times);
    })
}).catch(function (error) {
    console.log(error);
    console.log('something crash')
});
