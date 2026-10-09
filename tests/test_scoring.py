import unittest,json,hashlib,copy
from src.prospective import build_forecast,reported_count_forecast
from src.model import Scenario
from src.scoring import score_record

class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.raw=json.dumps(build_forecast()).encode()
        self.r=dict(registered_forecast_sha256=hashlib.sha256(self.raw).hexdigest(),
          freeze_url='https://example.org/registration',commit_sha='a'*40,
          registered_at_utc='2026-10-17T12:00:00Z',coded_at_utc='2026-11-20T12:00:00Z',
          flight_at_utc='2026-10-29T14:30:00Z',configuration_matches=True,outcome='clean_report',
          evidence=[dict(url='https://example.org/report',first_public_at_utc='2026-11-12T23:59:59Z',snapshot_sha256='b'*64)])
    def test_late_coding_with_frozen_cutoff(self):
        r=score_record(self.raw,self.r)
        self.assertEqual(r['evidence_cutoff_exclusive_utc'],'2026-11-13T00:00:00+00:00')
        self.assertIsNotNone(r['score'])
    def test_no_hindsight_in_evidence(self):
        self.r['evidence'][0]['first_public_at_utc']='2026-11-13T00:00:00Z'
        with self.assertRaises(ValueError):score_record(self.raw,self.r)
    def test_no_registration_after_flight(self):
        self.r['registered_at_utc']='2026-10-29T15:00:00Z'
        with self.assertRaises(ValueError):score_record(self.raw,self.r)
    def test_reject_hash_mismatch(self):
        self.r['registered_forecast_sha256']='c'*64
        with self.assertRaises(ValueError):score_record(self.raw,self.r)
    def test_unlaunched_only_after_expiry(self):
        self.r['outcome']='NOT_LAUNCHED';self.r.pop('flight_at_utc')
        with self.assertRaises(ValueError):score_record(self.raw,self.r)
        self.r['coded_at_utc']='2027-01-02T00:00:00Z'
        self.r['evidence'][0]['first_public_at_utc']='2027-01-01T12:00:00Z'
        self.assertIsNone(score_record(self.raw,self.r)['score'])
    def test_no_early_scoring_or_changed_configuration(self):
        self.r['coded_at_utc']='2026-11-12T20:00:00Z'
        with self.assertRaises(ValueError):score_record(self.raw,self.r)
        self.r['coded_at_utc']='2026-11-20T20:00:00Z';self.r['configuration_matches']=False
        with self.assertRaises(ValueError):score_record(self.raw,self.r)
    def test_mnar_count_mass(self):
        a=reported_count_forecast(Scenario(mnar=True,anomaly_disclosure=.3))
        self.assertAlmostEqual(sum(a),1,12)
        self.assertGreater(a[-1],.1)

class ExtraProspectiveGuards(unittest.TestCase):
    def setUp(self):
        self.raw=json.dumps(build_forecast()).encode()
        self.record=dict(
            registered_forecast_sha256=hashlib.sha256(self.raw).hexdigest(),
            freeze_url='https://example.org/registration', commit_sha='a'*40,
            registered_at_utc='2026-10-17T12:00:00Z',
            coded_at_utc='2026-11-20T12:00:00Z',
            flight_at_utc='2026-10-29T14:30:00Z',
            configuration_matches=True, outcome='clean_report',
            evidence=[dict(url='https://example.org/report',first_public_at_utc='2026-11-12T10:00:00Z',snapshot_sha256='b'*64)])

    def test_avoid_retrospective_registration_after_expiry(self):
        self.record['registered_at_utc']='2027-01-01T01:00:00Z'
        self.record['coded_at_utc']='2027-01-02T01:00:00Z'
        with self.assertRaises(ValueError):score_record(self.raw,self.record)

    def test_no_prelaunch_document_as_outcome_evidence(self):
        self.record['evidence'][0]['first_public_at_utc']='2026-10-27T10:00:00Z'
        with self.assertRaises(ValueError):score_record(self.raw,self.record)

    def test_void_configuration_written_as_unscored_disposition(self):
        self.record['outcome']='VOID_CONFIGURATION'
        self.record['configuration_matches']=False
        self.record['configuration_change_description']='Actual flight with only four boosters, not the predeclared six'
        result=score_record(self.raw,self.record)
        self.assertIsNone(result['score'])
        self.assertEqual(result['outcome'],'VOID_CONFIGURATION')
        self.record['configuration_matches']=True
        with self.assertRaises(ValueError):score_record(self.raw,self.record)

    def test_unlaunched_requires_post_expiry_evidence(self):
        self.record['outcome']='NOT_LAUNCHED'
        self.record.pop('flight_at_utc')
        self.record['coded_at_utc']='2027-01-02T00:00:00Z'
        with self.assertRaises(ValueError):score_record(self.raw,self.record)
        self.record['evidence'][0]['first_public_at_utc']='2027-01-01T12:00:00Z'
        self.assertIsNone(score_record(self.raw,self.record)['score'])

    def test_future_evidence_rejected(self):
        self.record['evidence'][0]['first_public_at_utc']='2026-11-21T12:00:00Z'
        with self.assertRaises(ValueError):score_record(self.raw,self.record)
