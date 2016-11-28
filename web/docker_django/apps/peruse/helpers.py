from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from . import models
import os
import datetime
import time
import requests

def sendImageToOAR(XMLparams):
	XMLPath = '/usr/src/app/static/library/xml/'

	templateFile = XMLPath + 'temp/image-submission-to-OAR.xml'
	testDir = 'test/'
	XMLPath += testDir
	MIME = 'application/marcxml+xml'
	OARurl = 'http://oar.sci-gaia.eu/batchuploader/robotupload/insert'
	
	headers = {
		'Content-Type': 'application/marcxml+xml',
		'User-Agent': 'invenio_webupload'
	}

	# now = datetime.datetime.now().strftime('%H:%M:%S')
	t = datetime.datetime.now()
	seconds = t.strftime('%S')
	now = time.mktime(t.timetuple())
	doiSurfix = str(now).replace('.0', '') + '.' + seconds
	doiId = os.environ['doiPrefix'] + doiSurfix

	date = t.strftime('%Y-%M-%d')

	XMLparams['doiId'] = doiId
	XMLparams['date'] = date
	XMLparams['year'] = t.strftime('%Y')


	# save doiId into doiId status model
	oarStatus = models.OARUploadStatus()
	oarStatus.doi = doiId
	oarStatus.oar_type = 'image'
	oarStatus.save()

	# replace placeholders with XML parameters and store it in a string
	XMLTemplateFile = open(templateFile, 'r')
	XMLStream = XMLTemplateFile.readlines()
	templateStr = ''.join(XMLStream)
	newXMLContentStr = templateStr.format(**XMLparams)
	XMLTemplateFile.close()

	# write new xml into a new xml file
	XMLFile = XMLPath + doiSurfix  + '.xml';
	file = open(XMLFile, 'w')
	file.write(newXMLContentStr)
	file.close()


	# open new xml file for reading, Note must leave the b option otherwise you will get error 400 as response
	file = open(XMLFile, 'rb')

	files = {'file': (XMLFile, file, MIME)}

	serverResponse = requests.put(OARurl, files=files, headers=headers)
	resp = str(newXMLContentStr) + '<br><br>Server Response' + str(serverResponse)
	
	# update OARUploadStatus status on successful submission to OAR
	if serverResponse.status_code == 200:
		oarStatus2 = get_object_or_404(models.OARUploadStatus, doi = doiId)
		oarStatus2.status = True
		oarStatus2.save()	

	file.close()

	# resp = str(serverResponse)
	return  resp
