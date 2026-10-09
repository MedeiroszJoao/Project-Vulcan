"""Independent NASA raw -> discharge capacity audit for a pinned processed CSV.

Download files only inside ephemeral CI, never commit third-party raw materials.
Intended to fail closed if NASA source is inaccessible or extraction disagrees.
"""
import io,hashlib,json,posixpath,urllib.request,zipfile
from pathlib import Path
from scipy.io import loadmat
from research_battery_benchmark import URL as CSV_URL,SHA as CSV_BLOB,blobsha,ingest

NASA_URL="https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip"
TARGETS={"B0005","B0006","B0007","B0018"}
MAX_DOWNLOAD=250*1024*1024
MAX_FILE=65*1024*1024
MAX_SCANNED=3000
MAX_TOTAL_EXPANDED=650*1024*1024
scanned=0
expanded=0

def fetch(url,limit):
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Vulcan-Independent-Provenance-Audit"}),timeout=100) as r:
        data=r.read(limit+1)
    if len(data)>limit:raise ValueError("Data exceeds predeclared audit size limit")
    return data

def descend_zip(blob,results,depth=0):
    global scanned,expanded
    if depth>5:raise ValueError("Nested archives exceed five levels")
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        entries=z.infolist()
        for entry in entries:
            if entry.is_dir():continue
            scanned+=1
            if scanned>MAX_SCANNED:raise ValueError("Too many archive entries")
            basename=posixpath.basename(entry.filename.replace("\\","/"))
            name=basename.rsplit(".",1)[0].upper()
            # Only read nested ZIPs or desired MATLAB sources.
            relevant=entry.filename.lower().endswith(".zip") or (
                  entry.filename.lower().endswith(".mat") and name in TARGETS)
            if not relevant:continue
            if entry.file_size>MAX_FILE:raise ValueError("Archive member exceeds size cap: "+entry.filename)
            expanded+=entry.file_size
            if expanded>MAX_TOTAL_EXPANDED:raise ValueError("Expanded data exceed safety cap")
            raw=z.read(entry)
            if entry.filename.lower().endswith(".zip"):
                descend_zip(raw,results,depth+1)
            elif name in TARGETS:
                if name in results:
                    # Two versions may exist; do not silently select one.
                    raise ValueError("Duplicate raw cell "+name+" in source archives")
                results[name]=raw

def extract_capacities(raw,cell_id):
    payload=loadmat(io.BytesIO(raw),simplify_cells=True)
    if cell_id not in payload:raise ValueError("MAT missing expected cell key "+cell_id)
    root=payload[cell_id]
    if not isinstance(root,dict) or "cycle" not in root:raise ValueError("Unknown MATLAB layout "+cell_id)
    cycles=root["cycle"]
    if isinstance(cycles,dict):cycles=[cycles]
    vals=[]
    for c in cycles:
        if not isinstance(c,dict):raise ValueError("Unexpected cycle layout")
        kind=c.get("type")
        if isinstance(kind,bytes):kind=kind.decode()
        if str(kind).strip().lower()=="discharge":
            data=c["data"]
            val=float(data["Capacity"])
            vals.append(val)
    return vals

def main():
    csv=fetch(CSV_URL,200000)
    if blobsha(csv)!=CSV_BLOB:raise ValueError("Pinned processed snapshot changed")
    cells=ingest(csv)
    archive=fetch(NASA_URL,MAX_DOWNLOAD)
    raw={};descend_zip(archive,raw)
    if set(raw)!=TARGETS:
        raise ValueError("Expected B0005/06/07/18 raw .mat files absent or ambiguous: "+repr(sorted(raw)))
    output={"NASA_archive_sha256":hashlib.sha256(archive).hexdigest(),
            "NASA_archive_bytes":len(archive),
            "NASA_url":NASA_URL,
            "processed_git_blob_sha1":CSV_BLOB,
            "status":"RAW_NASA_CAPACITY_CROSSCHECK",
            "cell_checks":{}}
    for name in sorted(TARGETS):
        extracted=extract_capacities(raw[name],name)
        expected=cells[name][:,1].tolist()
        if len(extracted)!=len(expected):raise ValueError(f"{name}: cycle count mismatch: {len(extracted)} vs {len(expected)}")
        maxdiff=max(abs(a-b) for a,b in zip(extracted,expected))
        output["cell_checks"][name]={"n":len(expected),
            "raw_mat_sha256":hashlib.sha256(raw[name]).hexdigest(),
            "max_abs_capacity_difference_ah":maxdiff}
        if maxdiff>1e-10:
            raise ValueError(f"{name}: raw/processed capacity discrepancy {maxdiff:.12g} Ah")
    dest=Path("results/battery_external");dest.mkdir(parents=True,exist_ok=True)
    (dest/"raw_source_crosscheck.json").write_text(json.dumps(output,sort_keys=True,indent=2)+"\n")
    print("NASA_RAW_CROSSCHECK_PASS",json.dumps(output,sort_keys=True))

if __name__=="__main__":main()
