import uuid
import os

from app.cache_model import Cacheout
from app.settings import global_cache


class UrlsAnalyzer:
	def __init__(self, url_string=None, url_status=None):
		self.uid = uuid.uuid4().hex
		self.url_string = url_string
		self.url_status = url_status
	
	def __repr__(self):
		return "uid:%s url_string:%s url_status:%s" % (self.uid, self.url_string, self.url_status)
	
	def __str__(self):
		return "uid:%s url_string:%s url_status:%s" % (self.uid, self.url_string, self.url_status)
	
	def load_url_list(self):
		file = open(os.path.join('./app', "static", "url_list.txt"), 'r', encoding="ISO-8859-1")
		urls = file.readlines()
		# remove duplicates
		clean_urls = list(dict.fromkeys(urls))
		# clean cache start over
		Cacheout.cache.clear()
		g_settings = Cacheout.get_global_settings(Cacheout)
		for url in clean_urls:
			item = UrlsAnalyzer(url, g_settings["STATUSES"]["ACCEPTED"])
			global_cache.cache.set(item.uid, item)
		return True
