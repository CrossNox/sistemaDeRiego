from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
import dht11
import ledRingPercentage as lrp
import motor
from threading import Thread, Event
from time import sleep

app = Flask(__name__)
app.config['SECRET KEY']='secret'
socketio = SocketIO(app)

m = motor.motor(13)
l = lrp.ledRingPercentage(18)
d = dht11.dht11(4)

thread = Thread()
thread_stop_event = Event()

class dhtUpdater(Thread):
	def __init__(self,dht1,lrp,dht2=None,usePMT=False):
		self.delay = 5
		self.dht1 = dht1
		self.dht2 = dht2
		self.lrp = lrp
		self.lrp.clear()
		self.usePMT = usePMT
		super(dhtUpdater, self).__init__()
		
	def readAndUpdate(self):
		print 'reading dht'
		while not thread_stop_event.isSet():
			hum, temp = self.dht1.readHumAndTemp()
			if(hum <= 100):
                                self.lrp.showPercentage(hum);
                                socketio.emit('updatedht11', {'hum':hum, 'temp':temp})
			sleep(self.delay)
	
	def run(self):
		self.readAndUpdate()

@app.route("/")
def main():
   # Pass the template data into the template main.html and return it to the user
   return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('connect')
def handle_dht11():
	global thread
	print 'Connected'
	if not thread.isAlive():
		print 'starting dht updater'
		thread = dhtUpdater(dht1=d, lrp=l)
		thread.start()

@socketio.on('my event')
def handle_my_custom_event(json):
	print('received ' + str(json))
	
@socketio.on('toggleMotor')
def handle_my_custom_event(arg1):
	if (arg1 == 1):
		m.turnOn()
	elif(arg1 == 0):
		m.turnOff()
	

if __name__ == "__main__":
   socketio.run(app, host='0.0.0.0', port=8181, debug=True)
