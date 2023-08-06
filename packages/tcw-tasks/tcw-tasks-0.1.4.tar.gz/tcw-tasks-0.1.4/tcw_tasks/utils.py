import datetime
from tcw.database import session
from tcw.apps.contest.models import Contest

def expired_contests():
    now = datetime.datetime.utcnow()
    contests = session.query(Contest).filter(Contest.expires < now).all()
    if not contests:
        raise Exception("No contests that meet criteria")

    return contests
