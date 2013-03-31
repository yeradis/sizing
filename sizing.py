# -*- coding: utf-8 -*-
## libpng,libjpeg for mac http://ethan.tira-thompson.com/Mac_OS_X_Ports.html
from flask import Flask, request, make_response, send_file
from PIL import Image
from flask.ext.cache import Cache

import requests
from StringIO import StringIO

cache = Cache()
app = Flask(__name__)
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

@cache.memoize(50)
def serve_image(img_source_url,new_width,quality):
	img = Image.open(StringIO(requests.get(img_source_url).content))
	format = img.format
	percent = (new_width/float(img.size[0]))
	new_height = int((float(img.size[1])*float(percent)))
	img = img.resize((new_width,new_height), Image.ANTIALIAS)
	img_io = StringIO()
	img.save(img_io,"%s"%(format),quality=quality)
	img_io.seek(0)
	return send_file(img_io,mimetype='IMAGE/%s'%(format),as_attachment=False)

@app.route('/sizing/<int:quality>/<int:width>/<path:url>')
def sizing(quality,width,url):
	try:
		return serve_image(url,width,quality)	
	except:
		return "<h1>500 - Internal Server Error</h1>", 500
	

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)