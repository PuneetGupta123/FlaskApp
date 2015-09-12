from flask import Flask, request
import json
import requests
import datetime
import sqlite3
import time

app = Flask(__name__)

dblink = 'database.sql'
connection = sqlite3.connect(dblink)

@app.route('/')
def hello():
	return 'This is the home directory'

@app.route('/feed')
def getfeed():
	query = "SELECT eid,heading,uid,detail,cid,date FROM entry WHERE fulfilled=0 ORDER BY date DESC LIMIT 10"
	cursor = connection.execute(query)

	feed = dict()
	i = 1
	
	for line in cursor:
		if i>10:
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
	return feed

@app.route('/entry')
def getentry():
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
	return entry


@app.route('/profile')
def getprofile():
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

		profile = str(json.dumps(profile))
		return profile
	else:
		return 'User not found'

@app.route('/addentry')
def postaddentry():
	heading =  request.args.get('heading')
	uid =  request.args.get('uid')
	detail =  request.args.get('detail')
	cid =  request.args.get('cid')
	fulfilled = 0
	date = time.time()

	query = "INSERT INTO entry (heading,uid,detail,cid,fulfilled,date) VALUES (?,?,?,?,?,?)"
	cursor = connection.execute(query,(heading,uid,detail,cid,fulfilled,date))
	connection.commit()

	return 'True'

@app.route('/addreply')
def postaddreply():
	uid =  request.args.get('uid')
	content =  request.args.get('content')
	eid =  request.args.get('eid')
	date = time.time()
	fulfilled = 0
	

	query = "INSERT INTO reply (uid,content,eid,date,fulfilled) VALUES (?,?,?,?,?)"
	cursor = connection.execute(query,(uid,content,eid,date,fulfilled))
	connection.commit()
	return 'True'

if __name__ == '__main__':
    app.run()
