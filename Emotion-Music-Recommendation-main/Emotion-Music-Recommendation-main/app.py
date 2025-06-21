from flask import Flask, render_template, Response, jsonify
import gunicorn
from camera import *
import time
from pygame import mixer 
mixer.init()

app = Flask(__name__)

headings = ("Name","Album","Artist")
df1 = music_rec()
df1 = df1.head(15)

@app.route('/')
def index():
    print(df1.to_json(orient='records'))
    #music_dist={0:"songs/angry.csv",1:"songs/disgusted.csv ",2:"songs/fearful.csv",
    #3:"songs/happy.csv",4:"songs/neutral.csv",5:"songs/sad.csv",6:"songs/surprised.csv"}

    return render_template('index.html', headings=headings, data=df1)

def gen(camera):
    flag1 = False
    flag2 = False
    while True:
        
        global df1
        frame, df1 = camera.get_frame()
        #print('hii,,,',music_dist[show_text[0]])
        str = music_dist[show_text[0]]
        
        if str == 'songs/happy.csv' and not(flag1):
            
            mixer.music.load('play/1.mp3')
            mixer.music.play()

            flag1 = True 
            flag2 = False
            

        if str == 'songs/sad.csv' and not(flag2):
            
            mixer.music.load('play/2.mp3')
            mixer.music.play()

            flag2 = True 
            flag1 = False
            
        
           

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
           

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/t')
def gen_table():

    return df1.to_json(orient='records')

if __name__ == '__main__':
    app.debug = True
    app.run()
