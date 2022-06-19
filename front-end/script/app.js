// veranderen naar window.location.hostname
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
console.log(window.location.hostname);

//#region ***  DOM references                           ***********
let RingAan = 0;
let Slapen = 0;
let brightnessbool = false;
let colorbool = false;
let chart;
let chartActive = false;
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
    let actief = alarm.actief == 1 ? 'c-alarm__on' : '';
    let herhaal = alarm.herhaal;
    if (herhaal != '') {
      herhaal = 'Iedere ' + herhaal.replaceAll(',', ' ');
    } else {
      herhaal = 'Wordt niet herhaalt';
    }
    herhaal = herhaal.replace('Monday', 'Maandag');
    herhaal = herhaal.replace('Tuesday', 'Dinsdag');
    herhaal = herhaal.replace('Wednesday', 'Woensdag');
    herhaal = herhaal.replace('Thursday', 'Donderdag');
    herhaal = herhaal.replace('Friday', 'Vrijdag');
    herhaal = herhaal.replace('Saturday', 'Zaterdag');
    herhaal = herhaal.replace('Sunday', 'Zondag');
    html += `<a class="c-alarm ${actief}" href="detail.html?alarmid=${alarm.alarmID}">
                    <div class="c-alarm__content">
                    <h2 class="c-alarm__title">${alarm.naam}</h2>
                    <div class="c-alarm__periode"><span class="c-alarm__van">${alarm.tijdstip}</span></div></div>
                    <h3 class="c-alarm__day">${alarm.date}</h3>
                    <p class="c-alarm__description">${herhaal}</p>
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
  console.log('sdfqlgijuhfqsdlukghsdfquhildfqsuyiqsdfyuiodfqs', jsonObject);
  let converted_labels = [];
  let converted_data = [];
  for (let s of jsonObject.slaap) {
    converted_data.push(s.avgUur + '.' + s.avgmin);
    converted_labels.push(s.datum);
  }
  if (chartActive == false) {
    drawChart(converted_labels, converted_data);
    chartActive = true;
  } else {
    chart.updateOptions({
      xaxis: {
        categories: converted_labels,
      },
      series: [
        {
          data: converted_data,
        },
      ],
    });
    let val = document.querySelector('.js-selectHistoriekFilter').value;
    if (val == 1 || val == 2 || val == 3) {
      chart.updateOptions({
        tooltip: {
          custom: function (opt) {
            let data =
              opt.w.config.series[opt.seriesIndex].data[opt.dataPointIndex];
            data = String(data).replace('.', ':');
            let array = data.split(':');
            let text = '';
            if (array[0] != '00') {
              text += `${array[0]} Uren `;
            }
            if (array[1] != '00') {
              text += `${array[1]} Minuten`;
            }
            text += ' Geslapen';
            let label = opt.w.globals.labels[opt.dataPointIndex];
            return (
              `<div class="apexcharts-tooltip-title" style="font-family: Helvetica, Arial, sans-serif; font-size: 12px;">${label}</div>` +
              `<div class="apexcharts-tooltip-series-group apexcharts-active" style="order: 1; display: flex;"><span class="apexcharts-tooltip-marker" style="background-color: rgb(96, 97, 222);"></span><div class="apexcharts-tooltip-text" style="font-family: Helvetica, Arial, sans-serif; font-size: 12px;"><div class="apexcharts-tooltip-y-group"><span class="apexcharts-tooltip-text-y-label"></span><span class="apexcharts-tooltip-text-y-value">${text}</span></div><div class="apexcharts-tooltip-goals-group"><span class="apexcharts-tooltip-text-goals-label"></span><span class="apexcharts-tooltip-text-goals-value"></span></div><div class="apexcharts-tooltip-z-group"><span class="apexcharts-tooltip-text-z-label"></span><span class="apexcharts-tooltip-text-z-value"></span></div></div></div>`
            );
          },
        },
      });
    }
    if (val == 1) {
      chart.updateOptions({
        title: {
          text: 'Week overzicht van hoelang je slaapt',
        },
      });
    } else if (val == 2) {
      chart.updateOptions({
        title: {
          text: 'Maand overzicht van hoelang je slaapt',
        },
      });
    } else if (val == 3) {
      chart.updateOptions({
        title: {
          text: 'Overzicht van hoelang je slaapt',
        },
      });
    } else if (val == 4) {
      chart.updateOptions({
        title: {
          text: 'Hoelang duurt het om de wekker uit te zetten',
        },
        tooltip: {
          custom: function (opt) {
            let data =
              opt.w.config.series[opt.seriesIndex].data[opt.dataPointIndex];
            data = String(data).replace('.', ':');
            let array = data.split(':');
            let text = '';
            if (array[0] != '00') {
              text += `${array[0]} Minuten `;
            }
            if (array[1] != '00') {
              text += `${array[1]} Seconden`;
            }
            let label = opt.w.globals.labels[opt.dataPointIndex];
            return (
              `<div class="apexcharts-tooltip-title" style="font-family: Helvetica, Arial, sans-serif; font-size: 12px;">${label}</div>` +
              `<div class="apexcharts-tooltip-series-group apexcharts-active" style="order: 1; display: flex;"><span class="apexcharts-tooltip-marker" style="background-color: rgb(96, 97, 222);"></span><div class="apexcharts-tooltip-text" style="font-family: Helvetica, Arial, sans-serif; font-size: 12px;"><div class="apexcharts-tooltip-y-group"><span class="apexcharts-tooltip-text-y-label"></span><span class="apexcharts-tooltip-text-y-value">${text}</span></div><div class="apexcharts-tooltip-goals-group"><span class="apexcharts-tooltip-text-goals-label"></span><span class="apexcharts-tooltip-text-goals-value"></span></div><div class="apexcharts-tooltip-z-group"><span class="apexcharts-tooltip-text-z-label"></span><span class="apexcharts-tooltip-text-z-value"></span></div></div></div>`
            );
          },
        },
      });
    }
  }
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
  let options = {
    responsive: [
      {
        breakpoint: 576,
        options: {
          plotOptions: {
            bar: {
              horizontal: true,
            },
          },
        },
      },
    ],
    chart: {
      id: 'myChart',
      type: 'bar',
      foreColor: '#ffffff',
      background: '#1f1d1f',
      toolbar: {
        show: false,
      },
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
        // fontSize: '16px',
        fontFamily: 'Changa',
        colors: ['#ffffff'],
      },
      formatter: function (val, opt) {
        let formattedtijd =
          opt.w.config.series[opt.seriesIndex].data[opt.dataPointIndex];
        formattedtijd = String(formattedtijd).replace('.', ':');
        return formattedtijd;
      },
    },
    theme: {
      mode: 'dark',
      monochrome: {
        enabled: false,
        color: '#1f1d1f',
        shadeTo: 'light',
        shadeIntensity: 0.65,
      },
    },
    title: {
      text: 'Aantal uren geslapen',
      align: 'center',
      margin: 10,
      floating: false,
      style: {
        fontSize: '16px',
        fontWeight: 'bold',
        fontFamily: 'Changa',
        color: '#ffffff',
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
        color: '#6061de',
      },
    ],
    labels: l,
    noData: {
      text: 'Er is geen data aanwezig',
    },
    xaxis: {
      labels: {
        style: {
          // fontSize: '12px',
          fontFamily: 'Changa',
        },
      },
    },
    yaxis: {
      labels: {
        style: {
          // fontSize: '12px',
          fontFamily: 'Changa',
        },
      },
    },
    tooltip: {
      custom: function (opt) {
        let data =
          opt.w.config.series[opt.seriesIndex].data[opt.dataPointIndex];
        data = String(data).replace('.', ':');
        let array = data.split(':');
        let text = '';
        if (array[0] != '00') {
          text += `${array[0]} Uren `;
        }
        if (array[1] != '00') {
          text += `${array[1]} Minuten`;
        }
        text += ' Geslapen';
        let label = opt.w.globals.labels[opt.dataPointIndex];
        return (
          `<div class="apexcharts-tooltip-title" style="font-family: Helvetica, Arial, sans-serif; font-size: 12px;">${label}</div>` +
          `<div class="apexcharts-tooltip-series-group apexcharts-active" style="order: 1; display: flex;"><span class="apexcharts-tooltip-marker" style="background-color: rgb(96, 97, 222);"></span><div class="apexcharts-tooltip-text" style="font-family: Helvetica, Arial, sans-serif; font-size: 12px;"><div class="apexcharts-tooltip-y-group"><span class="apexcharts-tooltip-text-y-label"></span><span class="apexcharts-tooltip-text-y-value">${text}</span></div><div class="apexcharts-tooltip-goals-group"><span class="apexcharts-tooltip-text-goals-label"></span><span class="apexcharts-tooltip-text-goals-value"></span></div><div class="apexcharts-tooltip-z-group"><span class="apexcharts-tooltip-text-z-label"></span><span class="apexcharts-tooltip-text-z-value"></span></div></div></div>`
        );
      },

      // <div class="apexcharts-tooltip-title" style="font-family: Helvetica, Arial, sans-serif; font-size: 12px;">31 May 2022</div>
      // <div class="apexcharts-tooltip-series-group apexcharts-active" style="order: 1; display: flex;"><span class="apexcharts-tooltip-marker" style="background-color: rgb(96, 97, 222);"></span><div class="apexcharts-tooltip-text" style="font-family: Helvetica, Arial, sans-serif; font-size: 12px;"><div class="apexcharts-tooltip-y-group"><span class="apexcharts-tooltip-text-y-label"></span><span class="apexcharts-tooltip-text-y-value">10.00</span></div><div class="apexcharts-tooltip-goals-group"><span class="apexcharts-tooltip-text-goals-label"></span><span class="apexcharts-tooltip-text-goals-value"></span></div><div class="apexcharts-tooltip-z-group"><span class="apexcharts-tooltip-text-z-label"></span><span class="apexcharts-tooltip-text-z-value"></span></div></div></div>
      theme: 'dark',
      x: {
        show: true,
      },
      y: {
        title: {
          formatter: function () {
            return '';
          },
        },
      },
    },
    fill: {
      opacity: 1,
    },
  };
  chart = new ApexCharts(document.querySelector('.js-content'), options);
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
const test = function (jsonObject) {
  console.log('json', jsonObject);
  let converted_labels = [];
  let converted_data = [];
  for (let s of jsonObject.slaap) {
    converted_data.push(s.hoursMin);
    converted_labels.push(s.datum);
  }
  if (chartActive == false) {
    drawChart(converted_labels, converted_data);
    chartActive = true;
  } else {
    console.log('UPDATE');
    chart.updateOptions({
      xaxis: {
        categories: converted_labels,
      },
      series: [
        {
          data: converted_data,
        },
      ],
    });
    let val = document.querySelector('.js-selectHistoriekFilter').value;
    if (val == 1) {
      chart.updateOptions({
        title: {
          text: 'Week overzicht van hoelang je slaapt',
        },
      });
    } else if (val == 2) {
      chart.updateOptions({
        title: {
          text: 'Maand overzicht van hoelang je slaapt',
        },
      });
    } else if (val == 3) {
      chart.updateOptions({
        title: {
          text: 'Overzicht van hoelang je slaapt',
        },
      });
    } else if (val == 4) {
      chart.updateOptions({
        title: {
          text: 'Overzicht van hoelang het duurt om de wekker uit te zetten',
        },
      });
    }
  }
};
const getSlaapDataWeek = function () {
  const url = `http://${lanIP}/api/slaap/week/`;
  handleData(url, ShowSlaapGrafiek, showError);
};
const getSlaapDataMaand = function () {
  const url = `http://${lanIP}/api/slaap/maand/`;
  handleData(url, ShowSlaapGrafiek, showError);
};
const getWekkerDiffData = function () {
  const url = `http://${lanIP}/api/slaap/wekkerdiff/`;
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
      document.querySelector('.js-alarm').classList.remove('c-input--empty');
    });
  document.onclick = function (event) {
    if (event.target == document.querySelector('.c-createalarm')) {
      document.querySelector('.c-createalarm').style.display = 'none';
      document.querySelector('.c-floatingButton').style.display = 'flex';
      document.querySelector('.js-alarm').classList.remove('c-input--empty');
    }
  };
};
const listenToSocket = function () {
  if (document.querySelector('.js-alarmen')) {
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
        document.querySelector('.c-input__color').style.backgroundColor =
          hexcode;
      }
    });
    socket.on('B2F_SetBrightness', function (jsonObject) {
      if (brightnessbool == false) {
        document.querySelector('.js-brightness').value =
          jsonObject['brightness'];
        document.querySelector('.js-rangeValue').innerHTML =
          Math.round(document.querySelector('.js-brightness').value * 100) +
          ' %';
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
      if (Slapen == 1) {
        document.querySelector('.js-GoSleep').innerHTML = 'Wakker Worden';
      } else {
        document.querySelector('.js-GoSleep').innerHTML = 'Gaan Slapen';
      }
      console.log('Slapen binnen', Slapen);
    });
    socket.on('B2F_autoBrightness', function (jsonObject) {
      console.log(jsonObject);
      if (jsonObject['autobrightness'] == true) {
        // document.querySelector('.js-autobrightnessauto').innerHTML = 'Auto';
        document.querySelector('.js-brightness').disabled = true;
        document.querySelector('.js-rgb').disabled = true;
        document
          .querySelector('.c-input__range')
          .classList.add('c-input__range--disabled');
      } else {
        document.querySelector('.js-brightness').disabled = false;
        document.querySelector('.js-rgb').disabled = false;
        // document.querySelector('.js-autobrightnessauto').innerHTML = 'Manueel';
        document
          .querySelector('.c-input__range')
          .classList.remove('c-input__range--disabled');
      }
      document.querySelector('.js-autobrightness').checked =
        jsonObject['autobrightness'];
    });
  } else if (document.querySelector('.js-slaap')) {
    console.log('dfqsfd');
    socket.on('B2F_NewSleepData', function () {
      console.log('binnen');
      ListenToChangeFilter();
    });
  }
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
    document
      .querySelector('.js-autobrightness')
      .addEventListener('click', ListenToSetAutoBrightness);
  } else if (document.querySelector('.js-updatealarm')) {
    // detail.html
    document
      .querySelector('.js-deletealarm')
      .addEventListener('click', listenToDeleteAlarm);
    document
      .querySelector('.js-updatealarm')
      .addEventListener('click', listenToUpdateAlarm);
  } else if (document.querySelector('.js-content')) {
    document.querySelector('.js-slaap').addEventListener('click', getSlaapData);
    document
      .querySelector('.js-selectHistoriekFilter')
      .addEventListener('change', ListenToChangeFilter);
  }
};
const listenToCreateAlarm = function () {
  let t = document.querySelector('.js-alarm').value;
  if (t) {
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
    document.querySelector('.js-alarm').classList.remove('c-input--empty');
    document.querySelector('.c-floatingButton').style.display = 'flex';
    document.querySelector('.c-createalarm').style.display = 'None';
    handleData(url, showResultAddAlarm, showError, 'POST', payload);
  } else {
    console.error('NOOB');
    document.querySelector('.js-alarm').classList.add('c-input--empty');
  }
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
  window.location.href = 'index.html';
};
const ListenToGoSleep = function () {
  let time;
  if (Slapen == 0) {
    Slapen = 1;
    console.log('GaanSlapen');
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
  console.log('Slapen', Slapen, 'tijd', time);
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
const ListenToSetAutoBrightness = function () {
  let val = document.querySelector('.js-autobrightness').checked;
  // if (val == true) {
  //   document.querySelector('.js-autobrightnessauto').innerHTML = 'Auto';
  // } else {
  //   document.querySelector('.js-autobrightnessauto').innerHTML = 'Manueel';
  // }
  socket.emit('F2B_setautobrightness', { autobrightness: val });
};
const ListenToChangeFilter = function () {
  let value = document.querySelector('.js-selectHistoriekFilter').value;
  console.log(value);
  if (value == 1) {
    console.log('week');
    getSlaapDataWeek();
  } else if (value == 2) {
    console.log('maand');
    getSlaapDataMaand();
  } else if (value == 3) {
    console.log('alles');
    getSlaapData();
  } else if (value == 4) {
    console.log('hoelang');
    getWekkerDiffData();
  }
};
const ListenToShutdown = function () {
  const buttons = document.querySelectorAll('.js-shutdown');
  for (const button of buttons) {
    button.addEventListener('click', function () {
      console.log('shutdown');
      socket.emit('F2B_Shutdown');
    });
  }
};
//#endregion

//#region ***  Init / DOMContentLoaded                  ***********
const init = function () {
  toggleNav();
  ListenToShutdown();
  if (document.querySelector('.js-alarmen')) {
    document.querySelector('.c-input__color').style.backgroundColor =
      document.querySelector('.c-input__color').value;
    // herhaalDagen();
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
  } else if (document.querySelector('.js-content')) {
    listenToSocket();
    listenToUI();
    getSlaapDataWeek();
  }
};

document.addEventListener('DOMContentLoaded', init);
//#endregion
