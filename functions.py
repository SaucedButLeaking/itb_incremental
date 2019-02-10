def set(key,val):
	session[key] = val
	return 'ok'

def get(key):
	return session.get(key,'error')