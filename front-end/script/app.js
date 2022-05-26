// veranderen naar window.location.hostname
const lanIP = `192.168.168.169:5000`;
const socket = io(`http://${lanIP}`);

const listenToSocket = function () {
  console.log('test');
  socket.on('connected', function () {
    console.log('verbonden met socket webserver');
  });
  socket.on('B2F_verandering_ldr', function (jsonObject) {
    console.log(jsonObject);
    console.log('Ldr binnen');
    console.log(jsonObject);
    document.querySelector(
      '.js-test'
    ).innerHTML = `${jsonObject.ldr.waarde} ${jsonObject.ldr.meeteenheid}`;
  });
};

const init = function () {
  listenToSocket();
};

document.addEventListener('DOMContentLoaded', init);
