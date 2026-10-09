"""EX-POST read-only diagnostic of unusual first-to-last capacity increases.

Reads only original NASA MAT values from the previously hash-verified archive.
No refitting, no selection of forecasting models, no changes to prior evaluation.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.io import loadmat
import io
from research_nasa_monte_carlo import get_archive,extract_raw_cells,TARGETS

FOCUS=("B0033","B0034","B0036")

def describe(raw,name):
    payload=loadmat(io.BytesIO(raw),simplify_cells=True)
    cycles=payload[name]["cycle"]
    if isinstance(cycles,dict):cycles=[cycles]
    data=[]
    for number,cycle in enumerate(cycles,1):
        if str(cycle["type"]).strip().lower()!="discharge":continue
        row=cycle["data"]
        capacity=float(row["Capacity"])
        summary={"mat_cycle_index":number,"discharge_index":len(data)+1,
                 "capacity_ah":capacity}
        if "Voltage_measured" in row:
            v=np.asarray(row["Voltage_measured"]).reshape(-1)
            if v.size:
                summary.update(first_voltage_v=float(v[0]),last_voltage_v=float(v[-1]),
                               voltage_min_v=float(np.min(v)),voltage_max_v=float(np.max(v)),
                               voltage_samples=int(v.size))
        if "Current_measured" in row:
            current=np.asarray(row["Current_measured"]).reshape(-1)
            if current.size:summary["current_median_a"]=float(np.median(current))
        if "Time" in row:
            time=np.asarray(row["Time"]).reshape(-1)
            if len(time)>1:
                summary["duration_seconds"]=float(time[-1]-time[0])
                if "Current_measured" in row:
                    amp=np.asarray(row["Current_measured"]).reshape(-1)
                    if amp.shape==time.shape and np.all(np.diff(time)>=0):
                        summary["integrated_current_magnitude_ah"]=float(abs(np.trapezoid(amp,time))/3600)
        data.append(summary)
    c=np.array([r["capacity_ah"] for r in data])
    if len(c)!=197:raise AssertionError(f"Expected 197 discharge measurements for {name}; found {len(c)}")
    dif=np.diff(c)
    return {"name":name,"raw_mat_sha256":hashlib.sha256(raw).hexdigest(),
       "num_discharge":len(c),"num_total_cycles":len(cycles),
       "first":float(c[0]),"last":float(c[-1]),"first_to_last_delta":float(c[-1]-c[0]),
       "min":float(c.min()),"min_discharge_index":int(c.argmin()+1),
       "max":float(c.max()),"max_discharge_index":int(c.argmax()+1),
       "number_positive_changes":int((dif>0).sum()),
       "number_negative_changes":int((dif<0).sum()),
       "first_20_median":float(np.median(c[:20])),
       "middle_20_median":float(np.median(c[89:109])),
       "last_20_median":float(np.median(c[-20:])),
       "samples":[*data[:8],data[len(data)//2],*data[-5:]],
       "warning":"First-to-last increase does not establish absence of aging or a monotone trend; inspect full raw profiles and NASA discharge protocols before drawing physical conclusions"}

def main():
    raw=get_archive()
    cells=extract_raw_cells(raw)
    results={k:describe(cells[k],k) for k in FOCUS}
    out={"status":"EX_POST_RAW_CAPACITY_TRAJECTORY_DIAGNOSTIC_ONLY",
         "source":"Original NASA PCoE battery MAT archive, SHA256 verified",
         "changed_original_forecasts":False,
         "original_benchmark_p_values_or_metrics_recomputed":False,
         "cells":results}
    output=Path("results/nasa_trajectory_audit")
    output.mkdir(parents=True,exist_ok=True)
    (output/"report.json").write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
    print("NASA_RAW_TRAJECTORY_DIAGNOSTIC",json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
