import json
import datetime
import urllib.request
import tkinter as tk
import threading as th
from time import sleep

def initui():
	# main screen
	root.title(u"Combine Tool")
	root.geometry("585x365")
	
	# input file
	lblIn.place(x=10, y=10)
	entIn.place(x=110, y=10)
	entIn.insert(tk.END,"http://localhost:8000/status-json.xsl")
	
	# output file
	lblOut.place(x=10, y=35)
	entOut.place(x=110, y=35)
	entOut.insert(tk.END,"output.txt")
	
	# cron cycle
	lblSlp.place(x=10, y=60)
	entSlp.place(x=110, y=60)
	entSlp.insert(tk.END,"5")
	
	# select style
	lblStl.place(x=10, y=85)
	rb1l.place(x=105, y=85)
	rb2l.place(x=200, y=85)
	rbVar.set(0)
	
	# execute button
	btnGo.place(x=10, y=115)
	
	# stop button
	btnEnd.place(x=10, y=145)
	btnEnd['state'] = tk.DISABLED

	# log
	txtLog.place(x=10, y=180)
	txtLog['width'] = 80
	txtLog['height'] = 13


	
	root.mainloop()

def run():
	global stop_flag
	global thread
	
	btnGo['state'] = tk.DISABLED
	btnEnd['state'] = tk.NORMAL
	entIn['state'] = tk.DISABLED
	entOut['state'] = tk.DISABLED
	entSlp['state'] = tk.DISABLED
	rb1l['state'] = tk.DISABLED
	rb2l['state'] = tk.DISABLED

	if not thread:
		thread = th.Thread(target=getJsonTxt)
		stop_flag = False
		thread.start()

	txtLog.insert(1.0, '---run---\n')

def stop():
	global stop_flag
	global thread
	
	if thread:
		stop_flag = True
		thread.join()
		thread = None
	
	btnGo['state'] = tk.NORMAL
	btnEnd['state'] = tk.DISABLED
	entIn['state'] = tk.NORMAL
	entOut['state'] = tk.NORMAL
	entSlp['state'] = tk.NORMAL
	rb1l['state'] = tk.NORMAL
	rb2l['state'] = tk.NORMAL
	txtLog.insert(1.0, '---stop---\n')

def getJsonTxt():
	global frame
	global stop_flag
	strArtist = ''
	strTitle = ''
	
	inPath  = entIn.get()
	outPath = entOut.get()
	cronCycle = entSlp.get()
	
	# input check
	if inPath == '' or outPath == '':
		txtLog.insert(1.0, '!!!WRONG!!!\n')
		return
	
	while not stop_flag:
		try:
			with urllib.request.urlopen(inPath) as jsnData:
				jsnObj = json.load(jsnData)
				btnEnd['state'] = tk.NORMAL
			
			SOURCE = jsnObj['icestats']['source']
			ARTIST = SOURCE['artist']
			TITLE  = SOURCE['title']

			if not ARTIST:
				ARTIST = 'no data'
			if not TITLE:
				TITLE = 'no data'
			
			if ARTIST != strArtist or TITLE != strTitle:
				with open(outPath, 'w', encoding='utf-8') as txtData:
					if rbVar.get() == 0:
						txtData.write(ARTIST + ' - ' + TITLE + '\n')
					else:
						txtData.write(ARTIST + '\n' + TITLE + '\n')
			strArtist = ARTIST
			strTitle = TITLE

			now = datetime.datetime.now().isoformat()
			logStr = now + ' : ' + ARTIST + ' - ' + TITLE + '\n'
			txtLog.insert(1.0, logStr)
			
		except OSError as e:
			txtLog.insert(1.0, '\n')
			txtLog.insert(1.0, e)
			with open(outPath, 'w', encoding='utf-8') as txtData:
				txtData.write('no data')
		
		except KeyError as e:
			txtLog.insert(1.0, '\n')
			txtLog.insert(1.0, e)
			txtLog.insert(1.0, 'KeyError ')
			with open(outPath, 'w', encoding='utf-8') as txtData:
				txtData.write('no data')
		
		except json.JSONDecodeError as e:
			txtLog.insert(1.0, '\n')
			txtLog.insert(1.0, e)
			txtLog.insert(1.0, 'JSONDecodeError ')
			with open(outPath, 'w', encoding='utf-8') as txtData:
				txtData.write('no data')

		for i in range(int(cronCycle)):
			if stop_flag:
				break
			else:
				sleep(1)


if __name__=='__main__':
	root = tk.Tk()
	lblIn = tk.Label(text=u'Icecast XSL URL')
	entIn = tk.Entry(width=50)
	lblOut = tk.Label(text=u'Output File Path')
	entOut = tk.Entry(width=50)
	lblSlp = tk.Label(text=u'Cron Cycle(sec)')
	entSlp = tk.Entry(width=3)
	btnGo = tk.Button(text=u'GO',width=20,command=run)
	btnEnd = tk.Button(text=u'STOP',width=20,command=stop)
	txtLog = tk.Text(root)
	lblStl = tk.Label(text=u'Output style')
	rbVar = tk.IntVar()
	rb1l = tk.Radiobutton(root, value=0, variable=rbVar, text='Artist - Title')
	rb2l = tk.Radiobutton(root, value=1, variable=rbVar, text='Artist \\n Title')

	stop_flag = False
	thread = None

	initui()
	
	stop_flag = True
	if thread:
		thread.join()
