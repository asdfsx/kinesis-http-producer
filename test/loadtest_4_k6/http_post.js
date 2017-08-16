import http from "k6/http";

export default function() {
  var url = "http://192.168.3.178:8000/app";
  var payload = JSON.stringify({"packType":"app","packId":"c8b1d5e8-511b-4e91-843b-c20d2c511079","packTime":1502768767798,"appId":"0345045caf264c4d","deviceId":"6e115edce33cd2e793ab5f74b2001f8c","androidId":"49f69d81dd23bd0d","macAddr":"F4:09:D8:1E:93:76","deviceBranding":"samsung","deviceModel":"SM-G9008V","os":"Android","channel":"360 Market","longitude":999.0,"latitude":999.0,"network":"Wi-Fi","timezone":"GMT+08:00","carrier":"No Carrier","language":"zh-cn","osVersion":"5.0","resolution":"1080x1920","appVersion":"1.0","sdkVersion":"1.2","packData":[{"category":"sessionStart","sessionId":"7f1d6a0a-061a-45e0-899c-1caf401072a9","timestamp":1502768757968,"longitude":999,"latitude":999,"network":"Wi-Fi","carrier":"No Carrier","language":"zh-cn","osVersion":"5.0","resolution":"1080x1920","timezone":"GMT+08:00","appVersion":"1.0","sdkVersion":"1.2"},{"category":"pv","sessionId":"7f1d6a0a-061a-45e0-899c-1caf401072a9","pageId":"MainActivity","pageName":"MainActivity","sessionStartTime":1502768757968,"timestamp":1502768758029}]});
  var params =  { headers: { "Content-Type": "application/json" } }
  http.post(url, payload, params);
};