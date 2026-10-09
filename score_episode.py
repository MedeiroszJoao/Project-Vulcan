"""Score a frozen forecast using a documentary record; never overwrite output."""
import argparse,json,hashlib
from pathlib import Path
from src.scoring import score_record

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--forecast',default='forecast/reference.json')
    ap.add_argument('--record',required=True,help='JSON evidence and registration record; see docs/FORECAST_PROTOCOL.md')
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    try:
        record_path=Path(args.record);record=json.loads(record_path.read_text())
        # Hash-check documentary bytes, not merely the existence of hash strings.
        for e in record.get('evidence',[]):
            path=(record_path.parent/e['snapshot_file']).resolve()
            if hashlib.sha256(path.read_bytes()).hexdigest()!=e['snapshot_sha256']:
                raise ValueError('evidence snapshot hash mismatch')
        result=score_record(Path(args.forecast).read_bytes(),record)
    except (ValueError,KeyError,OSError) as e:ap.error(str(e))
    dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(result,indent=2,allow_nan=False))
if __name__=='__main__':main()
