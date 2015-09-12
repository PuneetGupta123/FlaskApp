from flask import Flask, request
import flask
import json

import datetime
import sqlite3
import time

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'
@application.route('/')
def hello():
	return 'This is the home directory'
@application.route('/nakul')
def hello1():
	return 'Hello Nakul'


@application.route('/feed')
def getfeed():
	connection = sqlite3.connect(dblink)

	query = "SELECT eid,heading,uid,detail,cid,date FROM entry WHERE fulfilled=0 ORDER BY date DESC LIMIT 15"
	cursor = connection.execute(query)

	feed = dict()
	i = 1

	for line in cursor:
		if i>15:
			break
		result = dict()
		result['eid'] = line[0]
		result['heading'] = line[1]
		result['uid'] = line[2]
		result['detail'] = line[3]
		result['cid'] = line[4]
		result['date'] = line[5]
		feed[i] = result
		i+=1
	feed['num'] = i-1
	feed = str(json.dumps(feed))

	connection.close()
	return feed

@application.route('/entry',methods=['GET'])
def getentry():
	connection = sqlite3.connect(dblink)

	#print '1'
	eid =  request.args.get('eid')
	query = "SELECT reply.rid,reply.uid,reply.content,reply.date,reply.fulfilled FROM entry join reply WHERE entry.eid = "+ str(eid)+" and reply.eid = entry.eid  ORDER BY reply.date DESC "


	try:
		print query
		cursor = connection.execute(query)
		#cursor=connection.execute("SELECT Problem_Id,Accepted,Wrong from SUBMISSIONS where Teamname=?",(str(uname),))
	except sqlite3.OperationalError, msg:
		print sqlite3.OperationalError


	print cursor
	entry = dict()
	i = 1

	for line in cursor:
		#print '1'
		result = dict()
		#print '1'
		result['rid'] = line[0]
		result['uid'] = line[1]
		result['content'] = line[2]
		result['date'] = line[3]
		result['fulfilled'] = line[4]
		entry[i] = result
		#print '1'
		i+=1
	#print '22'
	entry['num'] = i-1

	#print '1'
	query = "SELECT eid,heading,uid,detail,cid,date FROM entry WHERE eid="+str(eid)
	try:
		cursor1 = connection.execute(query)
	except sqlite3.OperationalError, msg:
		print msg
	#print '1'
	result = dict()
	for line1 in cursor1:

		result['eid'] = line1[0]
		result['heading'] = line1[1]
		result['uid'] = line1[2]
		result['detail'] = line1[3]
		result['cid'] = line1[4]
		result['date'] = line1[5]

	#print '1'
	entry['question'] = result

	entry = str(json.dumps(entry))

	connection.close()
	return entry


@application.route('/profile')
def getprofile():
	connection = sqlite3.connect(dblink)

	uid =  request.args.get('uid')
	query = "SELECT uid,name,age,emailid,address FROM user WHERE uid="+str(uid)
	try:
		cursor = connection.execute(query)
	except sqlite3.OperationalError, msg:
		print msg

	print type(cursor)
	for line in cursor:
		profile = dict()
		profile['uid'] = line[0]
		profile['name'] = line[1]
		profile['age'] = line[2]
		profile['emailid'] = line[3]
		profile['address'] = line[4]

		connection.close()
		profile = str(json.dumps(profile))
		return profile
	else:
		connection.close()
		return 'User not found'



@application.route('/addentry', methods=['POST'])
def postaddentry():

	connection = sqlite3.connect(dblink)

	print "1"

	print "Hello World - you sent me " + str(request.values)
	heading=request.values['heading']
	print heading
	uid =  request.values['uid']
	print uid
	detail =  request.values['detail']
	print detail
	cid =  request.values['cid']
	print  cid
	print "1"
	fulfilled = 0
	date = time.time()
	print "1"

	query = "INSERT INTO entry (heading,uid,detail,cid,fulfilled,date) VALUES (?,?,?,?,?,?)"
	try:
		print "1"

		cursor = connection.execute(query,(heading,uid,detail,cid,fulfilled,date))
	except sqlite3.OperationalError, msg:
		print msg
	connection.commit()


	connection.close()
	return 'True'

@application.route('/addreply')
def postaddreply():
	connection = sqlite3.connect(dblink)

	uid =  request.args.get('uid')
	content =  request.args.get('content')
	eid =  request.args.get('eid')
	date = time.time()
	fulfilled = 0


	query = "INSERT INTO reply (uid,content,eid,date,fulfilled) VALUES (?,?,?,?,?)"
	cursor = connection.execute(query,(uid,content,eid,date,fulfilled))
	connection.commit()

	connection.close()
	return 'True'

if __name__ == '__main__':
    application.run(host='0.0.0.0')
