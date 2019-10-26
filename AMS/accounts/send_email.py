from django.utils import crypto

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_mail(email):
    #write logc for sending mail here
    message = Mail(
        from_email='amansonkar93@gmail.com',
        to_emails=email,
        subject='Link to setup Username and Password',
        html_content='<a href="http://127.0.0.1:8000/register/'+email+'>Click here</a>')
    try:
        print('in mail')
        print(os.environ.get('SENDGRID_API_KEY'),'   is key')
        sg = SendGridAPIClient('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')
        print(sg)
        response = sg.send(message)
        print('response')
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return response
    except Exception as e:
        print(e.message)
        return None

def create_and_send_reset_password_link(email=None):
    if email is not None:
        user = UserProfile.objects.filter(email=email).first()
        if user is not None:
            link = generate_password_reset_link(user=user)
            if link is not None:
                api_response = Email().send_reset_link(receivers=[email], link=link, name=user.name)
                nm().add_notification_post_send(nm.RESET_LINK_SEND, nm.MEDIUM_EMAIL, [user.email],
                                                api_response)
                if api_response.get('status') is not None and api_response.get('status') is True:
                    return api_response, None
                return None, 'Error occurred in sending password reset link.'
            return None, 'Error occurred in generating password reset link. Try again.'
        return None, 'We could not find any user associated with that email address.'
    return None, 'Email cannot be empty.'


def generate_password_reset_link(user=None):
    if user is not None:
        token = make_hash_value()
        reset_password_end_point, base_url = os.environ['LIS_RESET_PASSWORD'], os.environ['LIS_BASE_URL']
        link = base_url + reset_password_end_point + "?" + "hash=" + str(token)
        expiry_time = timezone.now() + timedelta(hours=24)
        try:
            ResetPassword.objects.create(user_id=user.id, token=token, expires_at=expiry_time)
        except DatabaseError as e:
            log('create_reset_password', format(e), 'error')
            return None
        return link
def make_hash_value():
    return crypto.get_random_string(length=64)