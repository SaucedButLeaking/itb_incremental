def set(key,val):
	session[key] = val
	return 'ok'

def get(key):
	return session.get(key,'error')

def debug(msg):
	with open("instance/debug.txt","a") as f:
		f.write("\n" + msg)