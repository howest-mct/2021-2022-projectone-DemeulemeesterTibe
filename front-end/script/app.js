// veranderen naar window.location.hostname
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
console.log(window.location.hostname);

//#region ***  DOM references                           ***********
let RingAan = 0;
let Slapen = 0;
let brightnessbool = false;
let colorbool = false;
//#endregion

//#region ***  Callback-Visualisation - show___         ***********
const showResultAddAlarm = function (jsonObject) {
  console.log(jsonObject);
  socket.emit('F2B_Addalarm', { alarmID: jsonObject });
};
const showAlarmen = function (jsonObject) {
  console.log(jsonObject);
  const alarmen = document.querySelector('.c-alarmen-list');
  let html = '';
  for (alarm of jsonObject.alarmen) {
    html += `<a class="c-alarm" href="detail.html?alarmid=${alarm.alarmID}">
                    <div class="c-alarm__content">
                    <h2 class="c-alarm__title">${alarm.naam}</h2>
                    <div class="c-alarm__periode"><span class="c-alarm__van">${alarm.tijdstip}</span></div></div>
                    <h3 class="c-alarm__day">${alarm.date}</h3>
                    <p class="c-alarm__description"></p>
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
  console.log(jsonObject.alarm.herhaal);
  let dagen = jsonObject.alarm.herhaal;
  if (dagen) {
    dagen = dagen.split(',');
    for (let dag of dagen) {
      console.log(dag);
      document.querySelector(`.js-${dag}`).checked = true;
    }
  }
  document.querySelector('.js-alarmid').value = jsonObject.alarm.alarmID;
  document.querySelector('.js-naam').value = jsonObject.alarm.naam;
  let time = jsonObject.alarm.datetime;
  time = time.replace(' ', 'T');
  document.querySelector('.js-tijdstip').value = time;
  document.querySelector('.js-actief').checked = jsonObject.alarm.actief;
};
const ShowSlaapGrafiek = function (jsonObject) {
  let converted_labels = [];
  let converted_data = [];
  for (let s of jsonObject.slaap) {
    let hours = Math.round(s.sleptmin % 60, 2);
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
const herhaalDagen = function () {
  let repeat = '';
  let teller = 0;
  let vorTeller = 0;
  if (document.querySelector('.js-Monday').checked == true) {
    if (teller != vorTeller) {
      repeat += ',';
      vorTeller = teller;
    }
    repeat += 'Monday';
    teller += 1;
  }
  if (document.querySelector('.js-Tuesday').checked == true) {
    if (teller != vorTeller) {
      repeat += ',';
      vorTeller = teller;
    }
    repeat += 'Tuesday';
    teller += 1;
  }
  if (document.querySelector('.js-Wednesday').checked == true) {
    if (teller != vorTeller) {
      repeat += ',';
      vorTeller = teller;
    }
    repeat += 'Wednesday';
    teller += 1;
  }
  if (document.querySelector('.js-Thursday').checked == true) {
    if (teller != vorTeller) {
      repeat += ',';
      vorTeller = teller;
    }
    repeat += 'Thursday';
    teller += 1;
  }
  if (document.querySelector('.js-Friday').checked == true) {
    if (teller != vorTeller) {
      repeat += ',';
      vorTeller = teller;
    }
    repeat += 'Friday';
    teller += 1;
  }
  if (document.querySelector('.js-Saturday').checked == true) {
    if (teller != vorTeller) {
      repeat += ',';
      vorTeller = teller;
    }
    repeat += 'Saturday';
    teller += 1;
  }
  if (document.querySelector('.js-Sunday').checked == true) {
    if (teller != vorTeller) {
      repeat += ',';
      vorTeller = teller;
    }
    repeat += 'Sunday';
    teller += 1;
  }
  return repeat;
};
const drawChart = function (l, d) {
  console.log(d);
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
const togglePopUP = function () {
  document
    .querySelector('.js-showCreateAlarm')
    .addEventListener('click', function () {
      document.querySelector('.c-createalarm').style.display = 'flex';
      document.querySelector('.c-floatingButton').style.display = 'None';
    });
  document
    .querySelector('.js-removeCreateAlarm')
    .addEventListener('click', function () {
      document.querySelector('.c-floatingButton').style.display = 'flex';
      document.querySelector('.c-createalarm').style.display = 'None';
    });
  document.onclick = function (event) {
    if (event.target == document.querySelector('.c-createalarm')) {
      document.querySelector('.c-createalarm').style.display = 'none';
      document.querySelector('.c-floatingButton').style.display = 'flex';
    }
  };
};
const listenToSocket = function () {
  socket.on('B2F_verandering_ldr', function (jsonObject) {
    console.log('Ldr binnen');
    document.querySelector(
      '.js-test'
    ).innerHTML = `${jsonObject.ldr.waarde} ${jsonObject.ldr.meeteenheid}`;
  });
  socket.on('B2F_SetColor', function (jsonObject) {
    if (colorbool == false) {
      console.log('B2F_SETCOLOR', jsonObject);
      const hexcode = rgbToHex(
        jsonObject['red'],
        jsonObject['green'],
        jsonObject['blue']
      );
      console.log('HEXCODE', hexcode);
      document.querySelector('.js-color').value = hexcode;
      document.querySelector('.c-input__color').style.backgroundColor = hexcode;
    }
  });
  socket.on('B2F_SetBrightness', function (jsonObject) {
    if (brightnessbool == false) {
      document.querySelector('.js-brightness').value = jsonObject['brightness'];
      document.querySelector('.js-rangeValue').innerHTML =
        Math.round(document.querySelector('.js-brightness').value * 100) + ' %';
    }
  });
  socket.on('B2F_Addalarm', function () {
    getAlarmen();
  });
  socket.on('B2F_Ringstatus', function (jsonObject) {
    RingAan = jsonObject.ring;
    if (RingAan == 1) {
      document.querySelector('.js-rgb').checked = true;
    } else {
      document.querySelector('.js-rgb').checked = false;
    }
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
    document.querySelector('.js-rgb').addEventListener('change', ListenToRgb);
    document
      .querySelector('.js-GoSleep')
      .addEventListener('click', ListenToGoSleep);
    listenToChangeColor();
    listenToChangeBrightness();
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
  const url = `http://${lanIP}/api/alarm/`;
  let naam = '';
  if (document.querySelector('.js-alarmnaam').value == '') {
    naam = 'Alarm';
  } else {
    naam = document.querySelector('.js-alarmnaam').value;
  }
  const herhaling = herhaalDagen();
  const payload = JSON.stringify({
    naam: naam,
    tijd: t,
    actief: document.querySelector('.js-actief').checked,
    herhaal: herhaling,
  });
  document.querySelector('.c-floatingButton').style.display = 'flex';
  document.querySelector('.c-createalarm').style.display = 'None';
  console.log(payload);
  handleData(url, showResultAddAlarm, showError, 'POST', payload);
};
const listenToChangeColor = function () {
  document.querySelector('.c-input__color').oninput = function () {
    colorbool = true;
    this.style.backgroundColor = this.value;
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
  document
    .querySelector('.c-input__color')
    .addEventListener('blur', function () {
      colorbool = false;
    });
};
const listenToChangeBrightness = function () {
  document.querySelector('.js-brightness').oninput = function () {
    brightnessbool = true;
    document.querySelector('.js-rangeValue').innerHTML =
      Math.round(document.querySelector('.js-brightness').value * 100) + ' %';
    const brightness = document.querySelector('.js-brightness').value;
    console.log(brightness);
    socket.emit('F2B_SetBrightness', { brightness: brightness });
  };
  const myTimeout = setTimeout(function () {
    brightnessbool = false;
  }, 1000);
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
  const herhaling = herhaalDagen();
  socket.emit('F2B_UpdateAlarm', {
    alarmid: id,
    naam: naam,
    tijdstip: tijdstip,
    actief: document.querySelector('.js-actief').checked,
    herhaal: herhaling,
  });
};
const ListenToGoSleep = function () {
  let time;
  if (Slapen == 0) {
    Slapen = 1;
    if (document.querySelector('.js-GoSleepInput').value) {
      console.log(document.querySelector('.js-GoSleepInput').value);
      time = document.querySelector('.js-GoSleepInput').value;
    } else {
      let today = new Date();
      time = today.toTimeString().split(' ');
      time = time[0].substring(0, 5);
      document.querySelector('.js-GoSleepInput').value = time;
    }
    console.log('Slaapwel');
  } else if (Slapen == 1) {
    Slapen = 0;
    console.log('Goeiemorgen /Middag /Avond');
  }
  socket.emit('F2B_GaanSlapen', { Slapen: Slapen, tijd: time });
};
const ListenToRgb = function () {
  if (this.checked == true) {
    RingAan = 1;
  } else if (this.checked == false) {
    RingAan = 0;
  }
  socket.emit('F2B_RGBring', { aan: RingAan });
  console.log(RingAan);
};
//#endregion

//#region ***  Init / DOMContentLoaded                  ***********
const init = function () {
  toggleNav();
  herhaalDagen();
  if (document.querySelector('.js-alarmen')) {
    document.querySelector('.c-input__color').style.backgroundColor =
      document.querySelector('.c-input__color').value;
    togglePopUP();
    getAlarmen();
    listenToSocket();
    listenToUI();
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
