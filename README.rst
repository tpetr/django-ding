===========
django-ding
===========

An easy way to send notifications when an object is created (ex. "DING! New User!" emails)

Getting Started
===============

- Add django_ding to your PYTHONPATH

- Add ding to the INSTALLED_APPS list in settings.py:

::

    INSTALLED_APPS = (
        'django.contrib.auth',
        ...
        'ding',
    )

- Populate DING dict in settings.py with the models to notify:

::

	DING = {
	    'auth.User': {
	    	# path to template for new object email subject
	        'NEW_SUBJECT_TEMPLATE': 'ding/new_object_subject.txt',

	        # path to template for new object email body
	        'NEW_BODY_TEMPLATE': 'ding/new_object_body.html',

	        # list of recipients (NOTE: must be a list, even if just one email address!)
	        'RECIPIENTS': ['trpetr@gmail.com'],

	        # email address to send from
	        'FROM': 'poop@poop.com'
	    }
	}

Summary Emails
==============

If you don't want to send out an email for every new object, you can instead send out a peroidic summary email. Make sure you have these settings in your DING dict:

::

	DING = {
		'auth.User': {
			# lambda that returns a queryset of objects to summarize
			'QUERYSET': lambda Model, time: Model.objects.filter(date_joined__gte=time),

			# path to template for summary email subject
			'SUMMARY_SUBJECT_TEMPLATE': 'ding/summary_subject.txt',

			# path to template for summary email body
			'SUMMARY_BODY_TEMPLATE': 'ding/summary_body.html',

			# list of recipients (NOTE: must be a list, even if just one email address!)
	        'RECIPIENTS': ['trpetr@gmail.com'],

	        # email address to send from
	        'FROM': 'poop@poop.com'
		}
	}

You can trigger the email by running ./manage.py send_ding_summary.