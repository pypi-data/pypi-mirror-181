import os
import sys
import time
import logging
import random
import datetime
import smtplib
from sendgrid import SendGridAPIClient
from tcw.database import session, init_engine
from tcw.apps.contest.models import Contest
from tcw_tasks.utils import expired_contests
from tcw_tasks.models import Message


# globals #
logger = logging.getLogger('tcw-tasks')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s|%(name)s|%(levelname)s|%(message)s'
)

def main():
    uri = os.getenv('SQLALCHEMY_DATABASE_URI', None)
    if not uri:
        logger.error('Must have SQLALCHEMY_DATABASE_URI environment var')
        sys.exit(1)

    init_engine(uri)
    logger.info("STARTING")
    while True:
        finish_contests()
        time.sleep(60)


def finish_contests():
    contests = []

    try:
        contests = expired_contests()
        logger.info("%d contests pending closure" % len(contests))
    except:
        logger.debug("No contests pending closure")
        return

    for c in contests:
        try:
            if c.attributes is None or 'winners' not in c.attributes:
                winners = c.pick_winners()
                c.attributes = {'winners': winners}
                session.commit()

            notify_owner(c)
            logger.info("Closing contest (%s) %s" % (c.name, c.title))
            session.delete(c)
            session.commit()

        except Exception as x:
            logger.warning(x)
            session.rollback()


def notify_owner(contest):
    local = not bool(os.getenv('SENDGRID_API_KEY', 0))
    msg = Message(contest=contest).get_message(local)
    if local:
        with smtplib.SMTP('localhost', 25) as s:
            s.send_message(msg)
    else:
        client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = client.send(msg)


if __name__ == '__main__':
    main()
