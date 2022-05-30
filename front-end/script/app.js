// veranderen naar window.location.hostname
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region ***  DOM references                           ***********
let RingAan = 0;
//#endregion

//#region ***  Callback-Visualisation - show___         ***********
const showResultAddAlarm = function (jsonObject) {
  console.log('fout');
  console.log(jsonObject);
  getAlarmen();
};
const showAlarmen = function (jsonObject) {
  console.log(jsonObject);
  const alarmen = document.querySelector('.c-alarmen-list');
  let html = '';
  for (alarm of jsonObject.alarmen) {
    console.log(alarm);
    html += `<a class="c-alarm" href="detail.html?id=${alarm.alarmID}">
                    <div class="c-alarm__content">
                        <h2 class="c-alarm__title">${alarm.naam}</h2>
                        <h3 class="c-alarm__day">${alarm.dag}</h3>
                        <div class="c-alarm__periode"><span class="c-alarm__van">${alarm.tijdstip}</span></div>
                        <p class="c-alarm__description">Bla bla bla</p>
                    </div>
                </a>`;
  }
  alarmen.innerHTML = html;
};
const showResultAddColor = function (jsonObject) {
  console.log('historiek', jsonObject);
};
const showError = function (err) {
  console.log(err);
};
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***********
const hexToRgb = function (hex) {
  let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  if (result) {
    let r = parseInt(result[1], 16);
    let g = parseInt(result[2], 16);
    let b = parseInt(result[3], 16);
    return r + ',' + g + ',' + b; //return 23,14,45 -> reformat if needed
  }
  return null;
};
const rgbToHex = function (r, g, b) {
  return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
};
//#endregion

//#region ***  Data Access - get___                     ***********
const getAlarmen = function () {
  const url = 'http://192.168.168.169:5000/api/alarm/';
  handleData(url, showAlarmen, showError);
};
//#endregion

//#region ***  Event Listeners - listenTo___            ***********
const toggleNav = function () {
  let toggleTrigger = document.querySelectorAll('.js-toggle-nav');
  for (let i = 0; i < toggleTrigger.length; i++) {
    toggleTrigger[i].addEventListener('click', function () {
      document.querySelector('body').classList.toggle('has-mobile-nav');
    });
  }
};
const listenToSocket = function () {
  socket.on('B2F_verandering_ldr', function (jsonObject) {
    console.log('Ldr binnen');
    document.querySelector(
      '.js-test'
    ).innerHTML = `${jsonObject.ldr.waarde} ${jsonObject.ldr.meeteenheid}`;
  });
  socket.on('B2F_SetColor', function (jsonObject) {
    console.log('B2F_SETCOLOR', jsonObject);
    const hexcode = rgbToHex(
      jsonObject['red'],
      jsonObject['green'],
      jsonObject['blue']
    );
    console.log('HEXCODE', hexcode);
    document.querySelector('.js-color').value = hexcode;
  });
};
const listenToUI = function () {
  document
    .querySelector('.js-makealarm')
    .addEventListener('click', listenToCreateAlarm);
  document
    .querySelector('.js-setcolor')
    .addEventListener('click', listenToSetColor);
  document
    .querySelector('.js-rgbtoggle')
    .addEventListener('click', listenToRgbToggle);
};
const listenToCreateAlarm = function () {
  let t = document.querySelector('.js-alarm').value;
  t = t.replace('T', ' ');
  console.log('test');
  test = document.querySelector('.js-alarm').value;
  const url = `http://192.168.168.169:5000/api/alarm/`;
  const payload = JSON.stringify({
    naam: document.querySelector('.js-alarmnaam').value,
    tijd: t,
  });
  console.log(payload);
  handleData(url, showResultAddAlarm, showError, 'POST', payload);
};
const listenToSetColor = function () {
  console.log('color');
  const url = 'http://192.168.168.169:5000/api/historiek/';
  let color = hexToRgb(document.querySelector('.js-color').value);
  console.log(color);
  const payload = JSON.stringify({
    color: color,
    deviceID: 4,
    actieID: 2,
  });
  socket.emit('F2B_SetColor', { color: color });
  handleData(url, showResultAddColor, showError, 'POST', payload);
};
const listenToRgbToggle = function () {
  if (RingAan == 0) {
    RingAan = 1;
  } else if (RingAan == 1) {
    RingAan = 0;
  }
  socket.emit('F2B_RGBring', { aan: RingAan });
  console.log(RingAan);
};
//#endregion

//#region ***  Init / DOMContentLoaded                  ***********

const init = function () {
  getAlarmen();
  toggleNav();
  listenToSocket();
  listenToUI();
};

document.addEventListener('DOMContentLoaded', init);
//#endregion
