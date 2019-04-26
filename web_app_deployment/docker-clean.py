# Run in Python 2.7
# Removes all "web_app" images that were created more than 2 weeks ago.

import datetime
import docker

client = docker.from_env()
images = client.images.list()
now = datetime.datetime.utcnow()

max_time_ago = datetime.timedelta(weeks=2)

for image in images:
	if image.tags and 'web_app' in image.tags[0]:
		created_unix = image.history()[0]['Created']
		created = datetime.datetime.utcfromtimestamp(created_unix)
		time_ago = now - created
		print image.tags[0]
		print created
		print time_ago
		if time_ago > max_time_ago:
			for tag in image.tags:
				client.images.remove(tag)
			print "REMOVED"
		else:
			print "PRESERVED"
		print ""

client.images.prune()
