# from playsound import playsound
# playsound("")


from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import vlc
instance = vlc.Instance('--aout=alsa')
p = instance.media_player_new()
m = instance.media_new('/home/student/2021-2022-projectone-DemeulemeesterTibe/sounds/marco-prima.mp3') 
p.set_media(m)

vlc.libvlc_audio_set_volume(p, 100)

@app.route('/')
def hello():
    return 'Hello, World!'
@app.route('/start')
def start():
    p.play() 
    return 'start'
@app.route('/stop')
def stop():
    p.stop()
    p.pause()
    return 'stop'


app.run(debug=False, host='0.0.0.0', port=8888)