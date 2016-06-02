import requests
import yaml
import re
import os
from lxml import html

main_base = os.path.dirname(__file__)
config_file = os.path.join(main_base, "config.yml")

_config = yaml.safe_load(open(config_file))

class AuthenticationException(Exception):
    def __init__(self):
        Exception.__init__(self,"An authentication error occured. Check your username \
        and password if you are using them.") 

class ConnectionError(Exception):
	def __init__(self):
		Exception.__init__(self,"There was an error connecting to the Motion server. \
			Please check your configuration and try again")

def _make_motion_http_request(username = None, password = None, thread = 0, domain = None, port = None, target = None, parameters=None):
	## Buisness logic of forming HTTP request and sending it off
	if bool(username) ^ bool(password):
		raise AuthenticationException()
	if(target is None):
		target = '/'
	domain = domain or 'localhost'
	port = port or '8080'
	url = 'http://{dom}:{p}/{thr}{tar}'.format(dom=domain, p=port, tar=target, thr=thread)
	if(_config['develop']): print(url)
	try:
		if(username):
			resp = requests.get(url, auth=(username, password), timeout=0.5, params=parameters)
		else:
			resp = requests.get(url, timeout=0.5, params=parameters)
		if resp.status_code == requests.codes.unauthorized:
			raise AuthenticationException()
		if resp.status_code != requests.codes.ok:
			raise Exception("Something went wrong. Request returned with code {} on url {}".format(resp.status_code, url))
		return resp.text
	except requests.exceptions.ConnectionError as err:
		raise ConnectionError()

def get_threads(**kwargs):
	## Returns string indicies of all threads currently running
	kwargs['target'] = ""
	kwargs['thread'] = ""
	resp =  _make_motion_http_request(**kwargs)
	webpage = html.fromstring(resp)
	threads = webpage.xpath('//a/@href')
	return [link.strip('/') for link in threads]

def take_snapshot(**kwargs):
	kwargs['target'] = '/action/snapshot'
	_make_motion_http_request(**kwargs)

def make_movie(**kwargs):
	kwargs['target'] = '/action/makemovie'
	_make_motion_http_request(**kwargs)

def restart(**kwargs):
	kwargs['target'] = '/action/restart'
	_make_motion_http_request(**kwargs)

def quit(**kwargs):
	kwargs['target'] = '/action/quit'
	_make_motion_http_request(**kwargs)

def detection_status(**kwargs):
	## Returns true if detection is turned on
	kwargs['target'] = '/detection/status'
	resp =  _make_motion_http_request(**kwargs)
	return 'ACTIVE' in resp

def detection_start(**kwargs):
	kwargs['target'] = '/detection/start'
	_make_motion_http_request(**kwargs)

def detection_pause(**kwargs):
	kwargs['target'] = '/detection/pause'
	_make_motion_http_request(**kwargs)

def detection_connection(**kwargs):
	## Returns true if we can connect to device
	kwargs['target'] = '/detection/connection'
	resp =  _make_motion_http_request(**kwargs)
	return 'OK' in resp

def config_get(query, **kwargs):
	kwargs['parameters'] = {'query':query}
	kwargs['target'] = '/config/get'
	resp = _make_motion_http_request(**kwargs)
	p = re.compile('= (.+) &')
	first = p.findall(resp)[0]
	return first

def config_list(**kwargs):
	ans = {}
	for setting in _config['config_params']:
		ans[setting] = config_get(setting, **kwargs)
	print(ans)
	return ans

def config_set(key,value, **kwargs):
	assert key in _config['config_params']
	kwargs['parameters'] = {key:value}
	kwargs['target'] = '/config/set'
	_make_motion_http_request(**kwargs)

def config_write(**kwargs):
	kwargs['target'] = '/config/writeyes'
	_make_motion_http_request(**kwargs)


if __name__ == "__main__":
	config_set('width','353')