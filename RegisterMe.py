import re, mechanize, yaml, smtplib, os, platform, sys

UVIC_URL = "https://www.uvic.ca/"
REGISTER_URL = UVIC_URL + "BAN2P/bwskfreg.P_AltPin"
MYPAGE_URL = UVIC_URL + "cas/login?service=" + UVIC_URL + "mypage/Login"

if platform.system() == 'Windows':
	WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "\\"
else:
	WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "/"

def testingMode(br, profile):

	print "\nTESTING MODE ENABLED\n"	
	print "TESTING UVIC LOGIN..."
	login(br, profile)
	
	print "\nTESTING EMAIL..."
	course = " ".join(map(str, profile['CRN'])) # Converts each item in a list to a string, then joins them
	sendEmail(profile, course, "FAILED_COURSES")

	print "\nDISPLAYING CRNS"
	for course in profile['CRN']:
		print course
	
	print"\nDESIRED SEMESTER"
	print profile['SEMESTER'][profile['DESIRED_SEMESTER']]
	
	print "\nTESTING COMPLETE\n"
	print "REVIEW OUTPUT FOR ERRORS BEFORE IMPLEMENTATION"
	
	
def login(br, profile): 
	
	br.open(MYPAGE_URL)
	br.select_form("credentials")

	userNameControl = br.form.find_control("username")
	userNameControl.value = profile['UVIC_LOGIN']['USERNAME']
	passwordControl = br.form.find_control("password")
	passwordControl.value = profile['UVIC_LOGIN']['PASSWORD']

	br.submit()
	if bool(re.search("The credentials you entered do not match our records",br.response().read())):
		print "LOGIN FAILED!"
		print "CHECK UVIC LOGIN USERNAME AND PASSWORD"
	else:
		print "LOGIN SUCCESSFUL"

def selectTerm(br, profile):

	br.open(REGISTER_URL)
	
	# Regex to get the correct dropdown value for the DESIRED_SEMESTER
	termSelectValue = re.search('\<OPTION VALUE\=\"([0-9]+)\"\>%s'%profile['SEMESTER'][profile['DESIRED_SEMESTER']], br.response().read())
	termSelectValue = str(termSelectValue.group(1))

	# Selecting the term select form
	br.form = list(br.forms())[1]  # Used because the form name was not named

	termSelectControl = br.form.find_control("term_in")
	termSelectControl.value = [termSelectValue]

	br.submit()

def register(br, profile):

	br.form = list(br.forms())[1]

	registeredCourses = ""
	failedRegisteredCourses = ""

	for index in range(len(profile['CRN'])):
		crnInput = br.form.find_control("CRN_IN", nr=index)
		crnInput.readonly = False
		crnInput.value = str(profile['CRN'][index])

	br.submit()

	for course in profile['CRN']:
		if bool(re.search("><INPUT TYPE=\"hidden\" NAME=\"CRN_IN\" VALUE=\"%d\""%course, br.response().read())):
			registeredCourses += str(course) + " "
			print "SUCCESSFULLY REGISTERED FOR " + str(course)
		else:
			failedRegisteredCourses += str(course) + " "
 
	if len(failedRegisteredCourses) > 0:
		print "FAILED TO REGISTER FOR " + failedRegisteredCourses

	if len(registeredCourses) > 0:
		sendEmail(profile, registeredCourses, failedRegisteredCourses)


def sendEmail(profile, successCourse, failedCourse):

	sender = "AmIinYet <AmIinYet@example.com>"
	recipient = profile['UVIC_LOGIN']['USERNAME'] + "@uvic.ca"
	subject = "Registered in your course" + str(successCourse)
	if len(failedCourse) > 0:
		body = "You have been registered in " + str(successCourse) + " however failed to register for " + str(failedCourse)
	else:
		body = "You have been registered in " + str(successCourse)

	message = "\From: %s\nTo: %s\nSubject: %s\n\n%s "%(sender, recipient, subject, body)

	try:
		emailSession = smtplib.SMTP("smtp.gmail.com", 587)
		emailSession.ehlo()
		emailSession.starttls()

		emailSession.login(profile['GMAIL']['ADDRESS'], profile['GMAIL']['PASSWORD'])
		emailSession.sendmail(sender, recipient, message)
		emailSession.close()

		print "EMAIL SENT SUCCESSFULLY!"

	except:
		print "FAILED TO SEND EMAIL"
		print "CHECK USERNAME/PASSWORD AND NETWORK"

if __name__ == "__main__":
	
	print "================================="
	print "            RegisterMe           "
	print "    Developed by Marc Laventure  "
	print "================================="
	print ""
	
	profile = yaml.safe_load(open(WORKING_DIRECTORY + "profile.yml", "r"))	
	br = mechanize.Browser()
	
	if len(sys.argv) > 1 and sys.argv[1] == "--test":
		testingMode(br, profile)
	else:		
		login(br, profile)
		selectTerm(br, profile)
		register(br, profile)
