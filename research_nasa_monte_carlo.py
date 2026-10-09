"""NASA PCoE: blind-within-run out-of-cohort degradation forecast stress test.

This code PREDECLARES candidate cells and methods, never fits to or selects
methods using held-out values, and reports every predeclared result, failures
included. Offline 60/40 splitting is not a prospective real-time forecast.
NOT validation of a rocket, GEM 63XL, or original Vulcan mission CPT.

Measured sources: B0025-28, B0029-32, B0033/34/36 in NASA battery archive.
The first four NASA cells used in prior public benchmarks are excluded.
"""
import hashlib
import io
import json
import math
import sys
import unittest
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
from scipy.io import loadmat
from scipy.stats import t as student_t

SOURCE_URL="https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip"
ARCHIVE_SHA256="82302a7db4fc1b34e0b6676326610438d43b816bdf11a69d1d012a464ef2f92e"
TARGETS=tuple(f"B{i:04d}" for i in (25,26,27,28,29,30,31,32,33,34,36))
COHORTS={
    "24C_pulsed":TARGETS[:4],
    "43C_pulsed":TARGETS[4:8],
    "24C_different_protocol":TARGETS[8:]
}
SEED=20261009
SIMULATIONS=4000
TRAIN_FRACTION=.60
MAX_ARCHIVE_BYTES=225*1024*1024
MAX_MEMBER_BYTES=155*1024*1024

def get_archive():
    request=urllib.request.Request(SOURCE_URL,headers={"User-Agent":"Vulcan-scientific-benchmark"})
    with urllib.request.urlopen(request,timeout=120) as handle:
        data=handle.read(MAX_ARCHIVE_BYTES+1)
    if len(data)>MAX_ARCHIVE_BYTES:raise ValueError("Original archive exceeds cap")
    if hashlib.sha256(data).hexdigest()!=ARCHIVE_SHA256:
        raise ValueError("NASA archive digest differs from previously verified primary-source snapshot")
    return data

def extract_raw_cells(outer):
    result={}
    with zipfile.ZipFile(io.BytesIO(outer)) as bundle:
        candidates=[n for n in bundle.namelist() if n.lower().endswith(".zip") and
                    "batteryagingarc_25-44" in n.lower().replace(" ","")]
        if len(candidates)!=1:raise ValueError("NASA 25-44 cohort archive missing/ambiguous")
        info=bundle.getinfo(candidates[0])
        if info.file_size>MAX_MEMBER_BYTES:raise ValueError("NASA nested cohort exceeds cap")
        nested=bundle.read(info)
    with zipfile.ZipFile(io.BytesIO(nested)) as cohort:
        for member in cohort.infolist():
            name=member.filename.replace("\\","/").split("/")[-1]
            if not name.lower().endswith(".mat"):continue
            ident=name[:-4].upper()
            if ident not in TARGETS:continue
            if ident in result:raise ValueError("Duplicate cell in NASA archive: "+ident)
            if member.file_size>20*1024*1024:raise ValueError("MAT too large: "+ident)
            result[ident]=cohort.read(member)
    if set(result)!=set(TARGETS):raise ValueError("Missing NASA cells: "+repr(sorted(set(TARGETS)-set(result))))
    return result

def extract_measured_capacities(raw,ident):
    obj=loadmat(io.BytesIO(raw),simplify_cells=True)
    if ident not in obj:raise ValueError("Missing battery name "+ident)
    root=obj[ident]
    cycles=root["cycle"]
    if isinstance(cycles,dict):cycles=[cycles]
    vals=[]
    for cycle in cycles:
        kind=str(cycle["type"]).strip().lower()
        if kind=="discharge":
            cap=float(cycle["data"]["Capacity"])
            if not (math.isfinite(cap) and 0<cap<3.5):
                raise ValueError(f"{ident} contains invalid capacity {cap}")
            vals.append(cap)
    if len(vals)<22:raise ValueError("Insufficient measured discharges for "+ident)
    return np.asarray(vals,dtype=float)

def fit_forecasts(y,ident,simulations=SIMULATIONS):
    """All fitting and innovation sampling from first 60% only."""
    a=np.asarray(y,dtype=float)
    n=len(a)
    if n<22 or not np.isfinite(a).all():raise ValueError("Series length/finite")
    cut=int(TRAIN_FRACTION*n)
    train=a[:cut].copy()
    future=a[cut:] # read for scoring ONLY, never for model fitting/selection
    x=np.arange(1,cut+1,dtype=float)
    xf=np.arange(cut+1,n+1,dtype=float)
    h=np.arange(1,len(future)+1,dtype=float)
    rng=np.random.default_rng(SEED+int(ident[-4:]))
    xmat=np.column_stack((np.ones(cut),x))
    a0,b0=np.linalg.lstsq(xmat,train,rcond=None)[0]
    trend=a0+b0*xf
    residual=train-(a0+b0*x)
    phi=float(np.dot(residual[:-1],residual[1:])/
              max(np.dot(residual[:-1],residual[:-1]),1.e-15))
    phi=float(np.clip(phi,-.97,.97))
    innovation=residual[1:]-phi*residual[:-1]
    sigma=float(np.sqrt(np.mean(innovation**2)))
    sigma=max(sigma,1e-8)
    qpath=np.empty((simulations,len(h)),dtype=float)
    previous=np.full(simulations,residual[-1],dtype=float)
    for j in range(len(h)):
        previous=phi*previous+rng.normal(0.,sigma,simulations)
        qpath[:,j]=trend[j]+previous
    # Random walk path bootstrapping uses *centered* observed training increments;
    # this is explicitly a driftless random-walk baseline.
    delta=np.diff(train)
    increments=delta-delta.mean()
    draws=rng.choice(increments,(simulations,len(h)),replace=True)
    rwpath=train[-1]+np.cumsum(draws,axis=1)
    xmatf=np.column_stack((np.ones(len(h)),xf))
    dof=cut-2
    e=train-(xmat@np.array([a0,b0]))
    mse=max(float(e@e/dof),1e-14)
    inv=np.linalg.inv(xmat.T@xmat)
    tscale=np.sqrt(mse*(1.+np.einsum("ij,jk,ik->i",xmatf,inv,xmatf)))
    tcrit=float(student_t.ppf(.95,dof))
    tlo,thi=trend-tcrit*tscale,trend+tcrit*tscale
    models={
        "last_driftless_rw":(np.full(len(h),train[-1]),rwpath),
        "linear_gaussian_t":(trend,None),
        "trend_AR1_mc":(np.mean(qpath,axis=0),qpath),
    }
    scored={}
    plot={}
    for model,(pred,paths) in models.items():
        if model=="linear_gaussian_t":
            lo,hi=tlo,thi
            prob_event=student_t.cdf((1.4-trend[-1])/tscale[-1],dof)
        else:
            lo=np.quantile(paths,.05,axis=0)
            hi=np.quantile(paths,.95,axis=0)
            prob_event=float(np.mean(paths[:,-1]<1.4))
        err=pred-future
        scored[model]={
            "MAE_ah":float(np.mean(np.abs(err))),
            "RMSE_ah":float(np.sqrt(np.mean(err**2))),
            "bias_ah":float(np.mean(err)),
            "coverage_nominal_90pct":float(np.mean((future>=lo)&(future<=hi))),
            "mean_interval_width_ah":float(np.mean(hi-lo)),
            "last_cycle_event_probability_lt_1p4Ah":float(prob_event),
            "last_cycle_event_outcome_lt_1p4Ah":bool(future[-1]<1.4),
            "last_cycle_event_brier":float((prob_event-float(future[-1]<1.4))**2),
            "last_predicted_ah":float(pred[-1]),
        }
        plot[model]=(pred,lo,hi)
    return {
        "n":n,"train":cut,"heldout":n-cut,"phi":phi,"sigma":sigma,
        "first_capacity":float(a[0]),"last_capacity":float(a[-1]),
        "models":scored,
        "visualization":(np.arange(1,n+1),a,cut,plot)
    }

def evaluate(data,write=True):
    if set(data)!=set(TARGETS):raise ValueError("Did not get all prespecified cells")
    results={k:fit_forecasts(data[k],k) for k in TARGETS}
    report={"status":"EXTERNAL COHORT STRESS TEST: post-hoc methodology benchmark, not LV-01",
        "time":"2026-10-09",
        "data":"NASA original MAT capacities (no processed mirror)",
        "original_source":SOURCE_URL,
        "NASA_archive_sha256":ARCHIVE_SHA256,
        "target_cells":list(TARGETS),
        "cohorts":{k:list(v) for k,v in COHORTS.items()},
        "method_predeclared":"No cross-cohort training; 60% chronological train per cell; rest evaluated once; 4000 seeded Monte Carlo paths; no holdout tuning",
        "interpretation_limit":"Only 11 battery devices; temporal correlation; AR1 Gaussian innovation model is illustrative; 90% nominal bands not guaranteed calibrated; 1.4Ah is a fixed example event threshold; no rocket safety inference.",
        "per_cell":{},"pooled":{},"by_cohort":{}}
    for k,r in results.items():
        report["per_cell"][k]={t:v for t,v in r.items() if t!="visualization"}
    for name,cells in [("ALL",TARGETS),*COHORTS.items()]:
        total=sum(results[k]["heldout"] for k in cells)
        agg={}
        for model in ("last_driftless_rw","linear_gaussian_t","trend_AR1_mc"):
            metrics={}
            for key in ("MAE_ah","RMSE_ah","coverage_nominal_90pct","mean_interval_width_ah","last_cycle_event_brier"):
                values=[results[k]["models"][model][key] for k in cells]
                if key=="RMSE_ah":
                    metrics[key]=float(np.sqrt(np.average(np.square(values),weights=[results[k]["heldout"] for k in cells])))
                elif key=="last_cycle_event_brier":
                    metrics[key]=float(np.mean(values)) # only one binary endpoint per device
                else:
                    metrics[key]=float(np.average(values,weights=[results[k]["heldout"] for k in cells]))
            metrics["number_of_physical_cells"]=len(cells)
            agg[model]=metrics
        if name=="ALL":report["pooled"]=agg
        else:report["by_cohort"][name]=agg
    if write:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        root=Path("results/nasa_monte_carlo")
        root.mkdir(parents=True,exist_ok=True)
        (root/"report.json").write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
        for k in ("B0025","B0029","B0033","B0036"):
            r=results[k]; x,observed,cut,plot=r["visualization"]
            fig,ax=plt.subplots(figsize=(9,4.8))
            ax.plot(x[:cut],observed[:cut],label="Measured training",color="black")
            ax.plot(x[cut:],observed[cut:],label="Measured untouched hold-out",color="gray",linewidth=2)
            colors={"last_driftless_rw":"tab:blue","linear_gaussian_t":"tab:orange","trend_AR1_mc":"tab:green"}
            for m,(pred,lo,hi) in plot.items():
                ax.plot(x[cut:],pred,label=m,color=colors[m])
                ax.fill_between(x[cut:],lo,hi,alpha=.12,color=colors[m])
            ax.axvline(cut+.5,linestyle=":",color="black")
            ax.set(title=f"{k}: fixed-horizon forecasts with 90% model intervals",
                   xlabel="Discharge number",ylabel="Measured discharge capacity (Ah)")
            ax.legend(fontsize=7);fig.tight_layout()
            fig.savefig(root/(k+"_forecast.png"),dpi=165)
            plt.close(fig)
        fig,axs=plt.subplots(1,2,figsize=(12,4.5),layout="constrained")
        labels=list(agg.keys())
        for i,k in enumerate(COHORTS):
            x0=np.arange(3)+i*.24
            axs[0].bar(x0,[report["by_cohort"][k][model]["MAE_ah"] for model in labels],width=.22,label=k)
            axs[1].bar(x0,[report["by_cohort"][k][model]["coverage_nominal_90pct"] for model in labels],width=.22)
        for ax in axs:
            ax.set_xticks(np.arange(3)+.24,[x.replace("_"," ") for x in labels],rotation=17,ha="right")
        axs[0].set(title="MAE on never-tuned test cycles",ylabel="Ah")
        axs[1].set(title="Nominal 90% forecast interval coverage",ylabel="Observed coverage",ylim=(0,1.05))
        axs[1].axhline(.9,linestyle="--",color="black")
        axs[0].legend(fontsize=8)
        fig.savefig(root/"comparison_by_cohort.png",dpi=160)
        plt.close(fig)
    return report

class AdversarialSyntheticTests(unittest.TestCase):
    def sample(self,n=75):
        x=np.arange(n,dtype=float)
        return 1.95-.006*x+.008*np.sin(x/4.)
    def test_no_future_leakage(self):
        y=self.sample()
        orig=fit_forecasts(y,"B0025",simulations=500)
        modified=y.copy();modified[int(.6*len(y)):]+=.40
        changed=fit_forecasts(modified,"B0025",simulations=500)
        for m in orig["models"]:
            self.assertEqual(orig["models"][m]["last_predicted_ah"],
                             changed["models"][m]["last_predicted_ah"])
            self.assertNotEqual(orig["models"][m]["MAE_ah"],changed["models"][m]["MAE_ah"])
    def test_monte_carlo_reproducible(self):
        a=fit_forecasts(self.sample(),"B0033",simulations=1000)
        b=fit_forecasts(self.sample(),"B0033",simulations=1000)
        self.assertEqual(a["models"]["trend_AR1_mc"],b["models"]["trend_AR1_mc"])
    def test_AR1_stability(self):
        y=self.sample()
        r=fit_forecasts(y,"B0036",simulations=300)
        self.assertLess(abs(r["phi"]),1.)
        self.assertGreater(r["sigma"],0.)
    def test_reject_nan(self):
        y=self.sample();y[3]=np.nan
        with self.assertRaises(ValueError):fit_forecasts(y,"B0025",simulations=200)
    def test_coverage_bound(self):
        r=fit_forecasts(self.sample(),"B0025",simulations=300)
        for val in r["models"].values():
            self.assertTrue(0<=val["coverage_nominal_90pct"]<=1)
            self.assertTrue(0<=val["last_cycle_event_probability_lt_1p4Ah"]<=1)
    def test_dependent_first_60pct_only(self):
        y=self.sample()
        r=fit_forecasts(y,"B0033",simulations=300)
        self.assertEqual(r["train"],45)
        self.assertEqual(r["heldout"],30)
    def test_fail_not_enough_cells(self):
        with self.assertRaises(ValueError):evaluate({"B0025":self.sample()},write=False)

if __name__=="__main__":
    if "--self-test" in sys.argv:unittest.main(argv=[sys.argv[0]],verbosity=2)
    else:
        raw=get_archive()
        cells={k:extract_measured_capacities(v,k) for k,v in extract_raw_cells(raw).items()}
        results=evaluate(cells)
        print("NASA_OUT_OF_COHORT_MONTE_CARLO",json.dumps(results,sort_keys=True))
