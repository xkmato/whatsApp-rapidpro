# whatsApp-rapidpro
WhatsApp external channel for Rapidpro (Can basically work as WhatsApp Aggregator)

## Getting started
You have to setup a rapidpro external channer with you domain and give it the `https://<youdomain>/from_rapidpro` as endpoint

Then add the following to your settings. 

`CREDENTIALS = ("<YOUR WHATSAPP PHONE NUMBER>", "<YOUR WHATSAPP PASSWORD>")`
`RAPIDPRO_NOTIFY_RECEIVED = 'http://machine.ballotuganda.com/api/v1/external/received/<your rapidpro channel uuid>/'`
`RAPIDPRO_NOTIFY_SENT = 'http://machine.ballotuganda.com/api/v1/external/sent/<your rapidpro cahnnel uuid>/'`

* Run Celery the usual way
* Run receiver with `python manage.py receive` (This should run forever, so you probably want to figure out the best way to do that)
* Run server the django way
