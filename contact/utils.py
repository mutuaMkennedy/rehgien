from django.core.mail import send_mail, BadHeaderError

def contact_support(first_name, last_name, email, phone, message):
	try:
		subject = 'You have a new Customer Support Request!'
		plainMessage = "First Name: {fn}. \nLast Name: {ln}. \nEmail: {e}. \nPhone: {p}. \n\nMessage: \n\n{m}".format(fn=first_name, ln=last_name, e=email, p=phone, m=message)

		send_mail(
			subject,
			plainMessage,
			'Rehgien <do-not-reply@mg.rehgien.com>',
			['support@rehgien.com'],
			fail_silently=False,
		)
		return True

	except BadHeaderError:
		return False
