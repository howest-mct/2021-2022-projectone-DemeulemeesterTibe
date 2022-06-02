// veranderen naar window.location.hostname
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
console.log(window.location.hostname);

//#region ***  DOM references                           ***********
let RingAan = 0;
let Slapen = 0;
//#endregion

//#region ***  Callback-Visualisation - show___         ***********
const showResultAddAlarm = function (jsonObject) {
  console.log(jsonObject);
  socket.emit('F2B_Addalarm', { alarmID: jsonObject });
};
const showAlarmen = function (jsonObject) {
  const alarmen = document.querySelector('.c-alarmen-list');
  let html = '';
  for (alarm of jsonObject.alarmen) {
    html += `<a class="c-alarm" href="detail.html?alarmid=${alarm.alarmID}">
                    <div class="c-alarm__content">
                        <h2 class="c-alarm__title">${alarm.naam}</h2>
                        <h3 class="c-alarm__day">${alarm.dag}</h3>
                        <div class="c-alarm__periode"><span class="c-alarm__van">${alarm.tijdstip}</span></div>
                    </div>
                </a>`;
  }
  alarmen.innerHTML = html;
};
const showResultAddColor = function (jsonObject) {
  console.log('historiek', jsonObject);
};
const showError = function (err) {
  console.error(err);
};
const showAlarm = function (jsonObject) {
  console.log(jsonObject);
  document.querySelector('.js-alarmid').value = jsonObject.alarm.alarmID;
  document.querySelector('.js-naam').value = jsonObject.alarm.naam;
  let time = jsonObject.alarm.datetime;
  time = time.replace(' ', 'T');
  document.querySelector('.js-tijdstip').value = time;
};
const ShowSlaapGrafiek = function (jsonObject) {
  let converted_labels = [];
  let converted_data = [];
  let rec = [];
  for (let s of jsonObject.slaap) {
    console.log(s.hoursMin);
    let hours = Math.round(s.sleptmin % 60, 2);
    console.log('hours', hours);
    converted_data.push(s.hoursMin);
    converted_labels.push(s.datum);
  }
  drawChart(converted_labels, converted_data);
};
const showHistoriek = function () {
  console.log('NOG AFWERKEN');
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
const drawChart = function (l, d) {
  console.log('data', d, 'labels', l);
  let options = {
    chart: {
      id: 'myChart',
      type: 'bar',
    },
    plotOptions: {
      bar: {
        borderRadius: 10,
      },
    },
    stroke: {
      curve: 'smooth',
    },
    dataLabels: {
      enabled: true,
      style: {
        fontSize: '16px',
        colors: ['#000000'],
      },
    },
    plotOptions: {
      bar: {
        dataLabels: {
          position: 'top',
        },
      },
    },
    series: [
      {
        type: 'column',
        name: 'Uren geslapen',
        data: d,
        color: '#ff0000',
      },
    ],
    labels: l,
    noData: {
      text: 'Loading...',
    },
  };
  let chart = new ApexCharts(document.querySelector('.js-content'), options);
  chart.render();
};
//#endregion

//#region ***  Data Access - get___                     ***********
const getAlarmen = function () {
  const url = `http://${lanIP}/api/alarm/`;
  handleData(url, showAlarmen, showError);
};
const getAlarm = function (id) {
  console.log(id);
  const url = `http://${lanIP}/api/alarm/${id}/`;
  handleData(url, showAlarm, showError);
};
const getSlaapData = function () {
  const url = `http://${lanIP}/api/slaap/`;
  handleData(url, ShowSlaapGrafiek, showError);
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
    document.querySelector('.c-input__color').style.backgroundColor = hexcode;
  });
  socket.on('B2F_SetBrightness', function (jsonObject) {
    document.querySelector('.js-brightness').value = jsonObject['brightness'];
    document.querySelector('.js-rangeValue').innerHTML =
      Math.round(document.querySelector('.js-brightness').value * 100) + ' %';
  });
  socket.on('B2F_Addalarm', function () {
    getAlarmen();
  });
  socket.on('B2F_Ringstatus', function (jsonObject) {
    RingAan = jsonObject.ring;
  });
  socket.on('B2F_SlaapStatus', function (jsonObject) {
    Slapen = jsonObject.slapen;
  });
};
const listenToUI = function () {
  if (document.querySelector('.js-alarmen')) {
    // index.html
    document
      .querySelector('.js-makealarm')
      .addEventListener('click', listenToCreateAlarm);
    document
      .querySelector('.js-setcolor')
      .addEventListener('click', listenToSetColor);
    document
      .querySelector('.js-rgbtoggle')
      .addEventListener('click', listenToRgbToggle);
    document
      .querySelector('.js-setbrightness')
      .addEventListener('click', listenToSetBrightness);
    listenToChangeColor();
    document
      .querySelector('.js-GoSleep')
      .addEventListener('click', ListenToGoSleep);
  } else if (document.querySelector('.js-updatealarm')) {
    // detail.html
    document
      .querySelector('.js-deletealarm')
      .addEventListener('click', listenToDeleteAlarm);
    document
      .querySelector('.js-updatealarm')
      .addEventListener('click', listenToUpdateAlarm);
  } else if (document.querySelector('.js-slaap')) {
    document.querySelector('.js-slaap').addEventListener('click', getSlaapData);
    document
      .querySelector('.js-historiek')
      .addEventListener('click', showHistoriek);
  }
};
const listenToCreateAlarm = function () {
  let t = document.querySelector('.js-alarm').value;
  t = t.replace('T', ' ');
  const url = `http://192.168.168.169:5000/api/alarm/`;
  let naam = '';
  console.log('dsfsqdfsdqf', document.querySelector('.js-alarmnaam').value);
  if (document.querySelector('.js-alarmnaam').value == '') {
    naam = 'Alarm';
  } else {
    naam = document.querySelector('.js-alarmnaam').value;
  }
  const payload = JSON.stringify({
    naam: naam,
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
const listenToSetBrightness = function () {
  const brightness = document.querySelector('.js-brightness').value;
  console.log(brightness);
  socket.emit('F2B_SetBrightness', { brightness: brightness });
};
const listenToChangeColor = function () {
  document.querySelector('.c-input__color').oninput = function () {
    this.style.backgroundColor = this.value;
  };
};
const listenToDeleteAlarm = function () {
  let id = document.querySelector('.js-alarmid').value;
  socket.emit('F2B_DELalarm', { alarmid: id });
  window.location.href = 'index.html';
};
const listenToUpdateAlarm = function () {
  let id = document.querySelector('.js-alarmid').value;
  let naam = document.querySelector('.js-naam').value;
  let tijdstip = document.querySelector('.js-tijdstip').value;
  tijdstip = tijdstip.replace(' ', 'T');
  socket.emit('F2B_UpdateAlarm', {
    alarmid: id,
    naam: naam,
    tijdstip: tijdstip,
  });
};
const ListenToGoSleep = function () {
  if (Slapen == 0) {
    Slapen = 1;
    console.log('Slaapwel');
  } else if (Slapen == 1) {
    Slapen = 0;
    console.log('Goeiemorgen /Middag /Avond');
  }
  socket.emit('F2B_GaanSlapen', { Slapen: Slapen });
};
//#endregion

//#region ***  Init / DOMContentLoaded                  ***********

const init = function () {
  toggleNav();
  if (document.querySelector('.js-alarmen')) {
    document.querySelector('.c-input__color').style.backgroundColor =
      document.querySelector('.c-input__color').value;
    getAlarmen();
    listenToSocket();
    listenToUI();
    document.querySelector('.js-brightness').oninput = function () {
      document.querySelector('.js-rangeValue').innerHTML =
        Math.round(document.querySelector('.js-brightness').value * 100) + ' %';
    };
  } else if (document.querySelector('.js-updatealarm')) {
    let urlParams = new URLSearchParams(window.location.search);
    alarmid = urlParams.get('alarmid');
    if (alarmid) {
      listenToUI();
      getAlarm(alarmid);
    } else {
      window.location.href = 'index.html';
    }
  } else if (document.querySelector('.js-slaap')) {
    listenToUI();
  }
};

document.addEventListener('DOMContentLoaded', init);
//#endregion
