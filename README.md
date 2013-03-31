# Sizing #

Easy to use Flask + PIL application server to help you to dynamically resize images for the ever increasing number of responsive sites and mobile screen sizes. 

And running with a simple cache, because we do not want to waste resources, right?

Right now there are only three required params:

**Quality** : An **Integer value** that specify the new image quality (does not make magic , no good quality from a bad source)
**Width** : An **Integer value** that specify the new image width, keeping the scale proportions
**Path** : An **URL** that points to the original image url in hight resolution ?

When you run the app, you need to call in this way:

    http://yourdomain:5000/sizing/<int:quality>/<int:width>/<path:url> 

By default listen on port 5000
Example url:

	http://localhost:5000/sizing/100/80/http://lorempixel.com/g/400/400/



Use in your html as any other external image url.

The current way without sizing:

	<img
	  src='http://lorempixel.com/g/400/400/'
	  alt='My original image'
	/>

Using the sizing stuff:

	<img
	  src='http://localhost:5000/sizing/100/80/http://lorempixel.com/g/400/400/'
	  alt='My new resized image'
	/>


Pd: i do not need to mention that you can use a simple javascript to dynamically change the width param in the url based on your screen size right ?