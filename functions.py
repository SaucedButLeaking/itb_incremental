def set(key,val):
	session[key] = val
	return 'ok'

def get(key):
	return session.get(key,'error')

def debug(msg):
	with open("debug.txt","w") as f:
		f.write(msg)