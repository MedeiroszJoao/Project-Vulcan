"""Offline consistency validation, not authentication of external registration."""
import hashlib,json,re
from datetime import datetime,timedelta,timezone
from urllib.parse import urlparse
from .model import Y_NAMES
from .prospective import categorical_score

def utc(value):
    t=datetime.fromisoformat(value.replace('Z','+00:00'))
    if t.tzinfo is None or t.utcoffset()!=timedelta(0): raise ValueError('explicit UTC timestamp required')
    return t

def https(url):
    p=urlparse(url)
    if p.scheme!='https' or not p.netloc or 'utm_' in url: raise ValueError('clean HTTPS URL required')

def score_record(raw, record):
    """Validate internal consistency and score a public observation.

    VOID_CONFIGURATION and NOT_LAUNCHED are *dispositions*, not extra Y
    categories, and they are retained without a numerical proper score.
    External publication/provenance authenticity must be checked independently.
    """
    f = json.loads(raw)
    h = hashlib.sha256(raw).hexdigest()
    if record['registered_forecast_sha256'] != h:
        raise ValueError('registered forecast hash mismatch')
    if f['report_signal_categories'] != Y_NAMES:
        raise ValueError('category ordering changed')
    https(record['freeze_url'])
    if not re.fullmatch('[0-9a-fA-F]{40}', record['commit_sha']):
        raise ValueError('commit SHA')
    freeze = utc(record['registered_at_utc'])
    coded = utc(record['coded_at_utc'])
    expiry = utc(f['valid_until_utc_exclusive'])
    if not freeze < expiry:
        raise ValueError('forecast must be registered before episode expiration')
    if not freeze < coded:
        raise ValueError('coding predates registration')

    outcome = record['outcome']
    cutoff = expiry
    score = None
    flight = None
    if outcome == 'NOT_LAUNCHED':
        if record.get('flight_at_utc') or coded < expiry:
            raise ValueError('NOT_LAUNCHED only after episode expiry without a liftoff')
    elif outcome in Y_NAMES or outcome == 'VOID_CONFIGURATION':
        flight = utc(record['flight_at_utc'])
        if not freeze < flight < expiry:
            raise ValueError('flight outside prospective validity')
        cutoff = flight.replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(days=15)
        if coded < cutoff:
            raise ValueError('T14 evidence window still open')
        if outcome == 'VOID_CONFIGURATION':
            if record.get('configuration_matches') is not False:
                raise ValueError('void requires a documented physical configuration mismatch')
            if len(record.get('configuration_change_description','').strip()) < 12:
                raise ValueError('void requires a concrete configuration change description')
        else:
            if record.get('configuration_matches') is not True:
                raise ValueError('configuration changed; void episode instead of scoring')
            score = categorical_score(f['public_report_signal_pmf'],Y_NAMES.index(outcome))
    else:
        raise ValueError('unknown outcome/disposition')

    if not record.get('evidence'):
        raise ValueError('documentary evidence/search log required')
    timestamps = []
    for e in record['evidence']:
        https(e['url'])
        posted = utc(e['first_public_at_utc'])
        if posted > coded:
            raise ValueError('future evidence cannot exist at scoring time')
        if outcome != 'NOT_LAUNCHED' and posted >= cutoff:
            raise ValueError('post-cutoff evidence')
        if not re.fullmatch('[0-9a-f]{64}',e['snapshot_sha256']):
            raise ValueError('snapshot SHA256')
        timestamps.append(posted)
    if outcome == 'NOT_LAUNCHED':
        # An archive or dated statement of non-launch after expiry can verify
        # the full observation window; a months-earlier schedule alone cannot.
        if not any(posted >= expiry for posted in timestamps):
            raise ValueError('no post-expiry documentary check of non-launch')
    elif not any(posted >= flight for posted in timestamps):
        # An old schedule page is not evidence of a later launch outcome.
        raise ValueError('no post-liftoff published evidence for outcome')

    return dict(episode_id=f['episode_id'],forecast_sha256=h,outcome=outcome,
        evidence_cutoff_exclusive_utc=cutoff.isoformat(),record=record,score=score,
        registration_verification='LOCAL_CONSISTENCY_ONLY; external timestamp and public hash require independent verification')
