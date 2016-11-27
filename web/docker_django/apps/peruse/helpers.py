from django.http import HttpResponse
from . import models

import datetime
import time

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
	doi = str(now).replace('.0', '') + '.' + seconds

	date = t.strftime('%Y-%M-%d')

	XMLparams['doiId'] = doi
	XMLparams['date'] = date
	XMLparams['year'] = t.strftime('%Y')


	# save doi into doi status model
	# oarStatus = OARUploadStatus()
	# oarStatus.doi = doi
	# oarStatus.oar_type = 'image'
	# oarStatus.status = 0
	# oarStatus.save()


	XMLTemplateFile = open(templateFile, 'r')
	XMLStream = XMLTemplateFile.readlines()
	templateStr = ''.join(XMLStream)
	newXMLContentStr = templateStr.format(**XMLparams)
	XMLTemplateFile.close()

	XMLFile = XMLPath + doi  + '.xml';

	file = open(XMLFile, 'w')
	file.write(newXMLContentStr)
	file.close()

	return HttpResponse(XMLFile)

	file = open(XMLFile, 'rb')

	files = {'file': (XMLFile, file, MIME)}

	serverResponse = requests.put(OARurl, files=files, headers=headers)
	resp = str(newXMLContentStr) + '<br><br>Server Response' + str(serverResponse)
	response = HttpResponse(resp)

	file.close()

	return  response
