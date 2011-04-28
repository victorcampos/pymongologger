MongoLogger 0.1
===============

Author: Victor Campos

Goal
----

This project is intended to be a simple click logger for ads as an app for
Django. It's API should be very simple and straightforward to understand.

Usage
-----

### Installation
Import mongologger project folder to your Django code folder

### Usage
* Instantiating
	from mongologger import mongologtools
	mylogger = mongologtools.MongoLogger(db='click_logging', collection='log')

* Logging	
	mylogger.log(ad_id=YOUR_AD_ID)
	
* Fetching data
	mylogger.fetch(ad_id=YOUR_AD_ID, start_date=DATE_OBJECT, end_date=DATE_OBJECT, [optional]total=True)
	
	
	
	
