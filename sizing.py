# -*- coding: utf-8 -*-
## libpng,libjpeg for mac http://ethan.tira-thompson.com/Mac_OS_X_Ports.html
from flask import Flask, request, make_response, send_file
from PIL import Image,ImageOps
from flask.ext.cache import Cache

import requests
from StringIO import StringIO
import os

import Queue
import threading

os.environ['http_proxy']=''
requests.adapters.DEFAULT_RETRIES = 5

app = Flask(__name__)

q = Queue.Queue()
def put_url(q, url, body):
	q.put(requests.put(url,data=body).close())

def serve_image(img_source_url,new_width,quality):
	req = requests.get(img_source_url, verify=False)
	img = Image.open(StringIO(req.content))
	req.close()
	format = img.format
	percent = (new_width/float(img.size[0]))
	new_height = int((float(img.size[1])*float(percent)))
	img = img.resize((new_width,new_height), Image.ANTIALIAS)
	img_io = StringIO()
	img.save(img_io,"%s"%(format),quality=quality)
	img_io.seek(0)
	
	#storing into memcached through nginx
	try:
		url = request.url
		body = img_io.getvalue()
		t = threading.Thread(target=put_url, args = (q,url,body))
		t.daemon = True
		t.start()
	except ValueError:
		print 'something wrong'
		print ValueError
	
	return send_file(img_io,mimetype='IMAGE/%s'%(format),as_attachment=False)

def fit_image(img_source_url,new_width,quality):
	img = Image.open(StringIO(requests.get(img_source_url).content))
	format = img.format
	percent = (new_width/float(img.size[0]))
	new_height = int((float(img.size[1])*float(percent)))
	img = ImageOps.fit(img, (new_width, new_height), Image.ANTIALIAS)
	img_io = StringIO()
	img.save(img_io,"%s"%(format),quality=quality)
	img_io.seek(0)
	return send_file(img_io,mimetype='IMAGE/%s'%(format),as_attachment=False)

@app.route('/sizing/<int:quality>/<int:width>/<path:url>')
def sizing(quality,width,url):
	return serve_image(url,width,quality)
	
@app.route('/sizing/fit/<int:quality>/<int:width>/<path:url>')
def sizing_fit(quality,width,url):
        try:
                return fit_image(url,width,quality)
        except:
                return "<h1>500 - Internal Server Error</h1>", 500

if __name__ == '__main__':
    app.run(threaded=True, debug=True,host='0.0.0.0', port=5002)
