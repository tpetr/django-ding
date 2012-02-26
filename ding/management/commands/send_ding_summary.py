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
        make_option('--seconds',
            action='store',
            type='int',
            dest='seconds',
            default=0,
            help='Seconds'),
		make_option('--minutes',
			action='store',
			type='int',
			dest='minutes',
			default=0,
			help='Minutes'),
		make_option('--hours',
			action='store',
			type='int',
			dest='hours',
			default=0,
			help='Hours'),
		make_option('--days',
			action='store',
			type='int',
			dest='seconds',
			default=0,
			help='Seconds')
		)

	def handle(self, *args, **options):
		# make interval
		interval = timedelta(seconds=options.get('seconds', 0), minutes=options.get('minutes', 0), hours=options.get('hours', 0), days=options.get('days', 0))

		# default to 1 day if no args
		if interval.total_seconds() == 0:
			interval = timedelta(days=1)

		start = datetime.now() - interval

		# get models
		try:
			model_names = settings.DING.keys()
		except AttributeError:
			print "DING not set in settings file"
			return

		# filter models, if needed
		if len(args) > 0:
			keys = [key for key in keys if key in args]

		# loop through models
		for model_name in model_names:
			ding = settings.DING[model_name]

			# resolve model class
			model = get_model(*model_name.split('.'))

			# get objects
			objects = ding['QUERYSET'](model, start)

			# send email
			if objects.count() > 0:
				print "%s new object(s) for %s" % (objects.count(), model_name)
				msg = EmailMessage(render_to_string(ding['SUMMARY_SUBJECT_TEMPLATE'], {'objects': objects, 'interval': interval}).strip(),
					render_to_string(ding['SUMMARY_BODY_TEMPLATE'], {'objects': objects, 'interval': interval}),
					ding['FROM'],
					ding['RECIPIENTS'])
				msg.content_subtype = 'html'
				msg.send()
			else:
				print "No new objects for %s" % key
		