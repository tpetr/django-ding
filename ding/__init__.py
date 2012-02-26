from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.exceptions import ImproperlyConfigured

from django.conf import settings

from django.db.models import get_model

class Ding(object):
	def __init__(self, model, subject_template, body_template, recipients, from_email):
		self.model = model
		self.subject_template = subject_template
		self.body_template = body_template
		self.recipients = recipients
		self.from_email = from_email

	def notify(self, sender, instance, created, **kwargs):
		if sender == self.model and created:
			msg = EmailMessage(render_to_string(self.subject_template, {'object': instance}).strip(), render_to_string(self.body_template, {'object': instance}), self.from_email, self.recipients)
			msg.content_subtype = 'html'
			msg.send()

try:
	for model_name, data in settings.DING.items():
		model = get_model(*model_name.split('.'))
		ding = Ding(model, data['NEW_SUBJECT_TEMPLATE'], data['NEW_BODY_TEMPLATE'], data['RECIPIENTS'], data['FROM'])
		post_save.connect(ding.notify, sender=model)
except AttributeError:
	pass