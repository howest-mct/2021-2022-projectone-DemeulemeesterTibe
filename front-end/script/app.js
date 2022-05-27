// veranderen naar window.location.hostname
const lanIP = `192.168.168.169:5000`;
const socket = io(`http://${lanIP}`);

const showResultAddAlarm = function (jsonObject) {
  console.log('fout');
  console.log(jsonObject);
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
const showError = function (err) {
  console.log(err);
};
const getAlarmen = function () {
  const url = 'http://192.168.168.169:5000/api/alarm/';
  handleData(url, showAlarmen, showError);
};

const listenToUI = function () {
  input = document.querySelector('.js-makealarm');
  input.addEventListener('click', function () {
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
  });
};
const listenToSocket = function () {
  socket.on('B2F_verandering_ldr', function (jsonObject) {
    console.log('Ldr binnen');
    document.querySelector(
      '.js-test'
    ).innerHTML = `${jsonObject.ldr.waarde} ${jsonObject.ldr.meeteenheid}`;
  });
};

const toggleNav = function () {
  let toggleTrigger = document.querySelectorAll('.js-toggle-nav');
  for (let i = 0; i < toggleTrigger.length; i++) {
    toggleTrigger[i].addEventListener('click', function () {
      document.querySelector('body').classList.toggle('has-mobile-nav');
    });
  }
};

const init = function () {
  getAlarmen();
  toggleNav();
  listenToSocket();
  listenToUI();
};

document.addEventListener('DOMContentLoaded', init);
