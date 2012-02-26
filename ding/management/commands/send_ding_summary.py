from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from optparse import make_option

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import get_model

class Command(BaseCommand):
	help = "Sends DING email summary for the past N minutes"
	args = "app.Model1 app.Model2"

	option_list = BaseCommand.option_list + (
        make_option('--interval',
            action='store',
            type='int',
            dest='interval',
            default=5,
            help='Time interval (in minutes)'),
        )

	def handle(self, *args, **options):
		interval = options.get('interval', 5)
		start = datetime.now() - timedelta(minutes=int(interval))

		# get models
		try:
			keys = settings.DING.keys()
		except AttributeError:
			print "DING not set in settings file"
			return

		# filter models, if needed
		if len(args) > 0:
			keys = [key for key in keys if key in args]

		for key in keys:
			ding = settings.DING[key]
			model = get_model(*key.split('.'))

			# get objects
			objects = ding['QUERYSET'](model, start)

			# send email
			if objects.count() > 0:
				print "%s new object(s) for %s" % (objects.count(), key)
				msg = EmailMessage(render_to_string(ding['SUMMARY_SUBJECT_TEMPLATE'], {'objects': objects, 'interval': interval}).strip(),
					render_to_string(ding['SUMMARY_BODY_TEMPLATE'], {'objects': objects, 'interval': interval}),
					ding['FROM'],
					ding['RECIPIENTS'])
				msg.content_subtype = 'html'
				msg.send()
			else:
				print "No new objects for %s" % key
		