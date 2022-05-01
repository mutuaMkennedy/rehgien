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

def send_lead_support(pro, service, client, email, phone, message):
	try:
		subject = 'NEW LEAD ALERT'
		plainMessage = (
		f"Pro Contacted:{pro}. \nRequested Service:{service}. \nClient: {client}. \nClient Email: {email}. \nClient Phone: {phone}. \nClient Message: {message}"
		)
 
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