from StringIO import StringIO
import urllib2
from urllib2 import Request

from bs4 import BeautifulSoup


# Parse the response

def extract_pdf_schedule(permit_number):
    '''
    The contents of the scedule are stored in a PDF file...unfortunately.
    I'm going to read and parse the PDF on start, and create the database from
    the extracted data. This step may take a long time; however,
    it will be updated via crons/jenkins if fully deployed
    '''

    custom_url = 'http://bsmnt.sfdpw.org/reportviewer/?title=form&report=/BSM/BSMReports/' \
                 'MFFPermitLocationInfo&ExportPDF=1&filename=form&params=permit={}'.format(permit_number)

    open = urllib2.urlopen(Request(custom_url)).read()
    memoryFile = StringIO(open).read()
    request = urllib2.Request('http://pdfx.cs.man.ac.uk', memoryFile, headers={'Content-Type': 'application/pdf'})
    response = urllib2.urlopen(request).read()
    schedule_soup = BeautifulSoup(response)
    for item in schedule_soup.find_all('outsider'):
        if "AM" in item.string or "PM" in item.string:
            print item.string.split(":")

def ingest_csv_file():
    '''
    Each line links to a PDF with a specific schedule on the food truck.
    It appears that the location modifies according to the date.
    '''

extract_pdf_schedule('14MFF-0034')