import os
import jinja2
from sendgrid.helpers.mail import (Mail, From, To, Subject, PlainTextContent,
    HtmlContent)
from email.message import EmailMessage
from tcw_tasks.templates import TEXT_TEMPLATE, HTML_TEMPLATE


class Formatter:
    def text_from_template(self, contest):
        msg = jinja2.Template(TEXT_TEMPLATE).render(contest=contest)
        return msg.strip()

    def html_from_template(self, contest):
        msg = jinja2.Template(HTML_TEMPLATE).render(contest=contest)
        return msg.strip()


class Message(Formatter):
    """
    Create email message for a finished contest
    """

    def __init__(self, *args, **kwargs):
        self.contest = None
        self.mail_from = os.getenv('TCW_MAIL_FROM', 'user@localhost')
        self.subject = 'Your Contest Kitty contest results'
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

        if self.contest is None:
            raise Exception('Contest object required')


    def get_message(self, local=True):
        if local:
            return self._get_email_msg()
        else:
            return self._get_sendgrid_msg()


    def _get_sendgrid_msg(self):
        msg = Mail(
            From(self.mail_from),
            To(self.contest.email),
            Subject(self.subject),
            PlainTextContent(self.text_from_template(self.contest)),
            HtmlContent(self.html_from_template(self.contest)))

        return msg


    def _get_email_msg(self):
        msg = EmailMessage()
        msg['Subject'] = self.subject
        msg['From'] = self.mail_from
        msg['To'] = self.contest.email

        msg.set_content(self.text_from_template(self.contest))
        msg.add_alternative(self.html_from_template(self.contest),
            subtype='html')

        return msg
