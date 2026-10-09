"""Transfer-method benchmark on experimental NASA PCoE battery measurements.
Source is third-party extracted CSV pinned to Git blob, NOT raw-NASA-byte validated.
NEVER interpret this exercise as GEM63XL physical risk model validation.
"""
import csv,hashlib,io,json,math,sys,unittest
from pathlib import Path
from urllib.request import Request,urlopen
import numpy as np
from scipy.stats import norm,t as tdist

SHA="adc395fdf25c6fa1b911535dc0ffc1c2a10e589e"
COMMIT="e414d2e00ecc369d042637df6a6147a948718649"
URL="https://raw.githubusercontent.com/amirhossein-sadeghi2003/battery-health-forecasting-baselines/"+COMMIT+"/data/processed/discharge_capacity.csv"
SIZES={"B0005":168,"B0006":168,"B0007":168,"B0018":132}
COLS={"battery_id","cycle_index","discharge_index","ambient_temperature","capacity_ah","num_samples"}

def blobsha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def ingest(raw):
    if blobsha(raw)!=SHA:raise ValueError("Pinned third-party source data changed")
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    if set(reader.fieldnames or ())!=COLS:raise ValueError("Source schema mismatch")
    cells={k:[] for k in SIZES}
    for r in reader:
        b=r["battery_id"]
        if b not in cells:raise ValueError("Unknown battery")
        c=float(r["capacity_ah"]);j=int(r["discharge_index"])
        if not math.isfinite(c) or not .5<c<3:raise ValueError("Bad capacity")
        cells[b].append((j,c))
    for b,rows in cells.items():
        if len(rows)!=SIZES[b] or [x[0] for x in rows]!=list(range(1,SIZES[b]+1)):
            raise ValueError("Broken discharge ordering")
    return {k:np.asarray(v,float) for k,v in cells.items()}

def fit_and_score(series):
    a=np.asarray(series,float)
    n=len(a);s=int(.6*n)
    if n<20 or not np.allclose(a[:,0],np.arange(1,n+1)):raise ValueError("Wrong time sequence")
    x=a[:,0];y=a[:,1];xf=x[s:];yf=y[s:];xt=x[:s];yt=y[:s]
    if xf.min()<=xt.max():raise AssertionError("Lookahead leakage")
    h=xf-xt[-1]
    # No later observation enters a prediction, even once.
    sd=max(float(np.std(np.diff(yt),ddof=1)),1e-6)
    last=np.full(len(yf),yt[-1]); last_scale=sd*np.sqrt(h)
    X=np.column_stack((np.ones(s),xt))
    beta=np.linalg.lstsq(X,yt,rcond=None)[0]
    res=yt-X@beta;df=s-2
    s2=max(float(res@res/df),1e-12)
    Xf=np.column_stack((np.ones(len(xf)),xf))
    lin=Xf@beta;inv=np.linalg.inv(X.T@X)
    lin_scale=np.sqrt(s2*(1+np.einsum("ij,jk,ik->i",Xf,inv,Xf)))
    quad=np.polyval(np.polyfit(xt,yt,2),xf)
    modes={"last_random_walk":(last,norm.logpdf(yf,loc=last,scale=last_scale),
               norm.ppf(.05,loc=last,scale=last_scale),norm.ppf(.95,loc=last,scale=last_scale)),
           "linear_student_t":(lin,tdist.logpdf(yf,df,loc=lin,scale=lin_scale),
               tdist.ppf(.05,df,loc=lin,scale=lin_scale),tdist.ppf(.95,df,loc=lin,scale=lin_scale)),
           "quadratic_point_only":(quad,None,None,None)}
    scores={}
    for k,(pred,lp,lo,hi) in modes.items():
        delta=pred-yf
        r={"mae_ah":float(np.mean(np.abs(delta))),
           "rmse_ah":float(np.sqrt(np.mean(delta*delta))),
           "bias_ah":float(np.mean(delta)),
           "last_test_forecast_ah":float(pred[-1])}
        if lp is not None:
            r["mean_neg_log_score"]=float(-np.mean(lp))
            r["coverage_90pct"]=float(np.mean((yf>=lo)&(yf<=hi)))
        scores[k]=r
    return {"n":n,"train_n":s,"test_n":n-s,"first_test_cycle":s+1,
            "last_true_capacity_ah":float(y[-1]),"initial_capacity_ah":float(y[0]),
            "scores":scores,
            "plot":(x,y,s,{k:v[0] for k,v in modes.items()},
                     modes["linear_student_t"][2],modes["linear_student_t"][3])}

def run(raw,output="results/battery_external"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    result={b:fit_and_score(v) for b,v in ingest(raw).items()}
    root=Path(output);root.mkdir(parents=True,exist_ok=True)
    pooled={}
    for model in ("last_random_walk","linear_student_t","quadratic_point_only"):
        rows=[(r["scores"][model],r["test_n"]) for r in result.values()]
        pooled[model]={"micro_mae_ah":float(np.average([r["mae_ah"] for r,n in rows],weights=[n for r,n in rows])),
            "micro_rmse_ah":float(np.sqrt(np.average([r["rmse_ah"]**2 for r,n in rows],weights=[n for r,n in rows]))),
            "macro_mae_ah":float(np.mean([r["mae_ah"] for r,n in rows]))}
        if "coverage_90pct" in rows[0][0]:
            pooled[model]["micro_coverage_90pct"]=float(np.average([r["coverage_90pct"] for r,n in rows],weights=[n for r,n in rows]))
            pooled[model]["micro_mean_neg_log_score"]=float(np.average([r["mean_neg_log_score"] for r,n in rows],weights=[n for r,n in rows]))
    for b,r in result.items():
        x,y,n,preds,lo,hi=r["plot"]
        fig,ax=plt.subplots(figsize=(8,4.5))
        ax.plot(x[:n],y[:n],label="Measured: training")
        ax.plot(x[n:],y[n:],label="Measured: held-out",linewidth=2)
        for k,v in preds.items():ax.plot(x[n:],v,label=k)
        ax.fill_between(x[n:],lo,hi,alpha=.12,label="Linear Student-t nominal 90% band")
        ax.axvline(n+.5,linestyle=":",color="black")
        ax.set(xlabel="Discharge index",ylabel="Capacity (Ah)",
               title=b+" — true held-out forecasts (no updating)")
        ax.legend(fontsize=7);fig.tight_layout()
        fig.savefig(root/(b+"_heldout.png"),dpi=165);plt.close(fig)
    report={"scientific_status":"observational transfer-method benchmark only; NOT launch physical validation",
      "source_description":"Third-party derived NASA PCoE measured battery capacity CSV; unverified against original .mat",
      "original_NASA_url":"https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/",
      "pinned_processed_url":URL,"processed_git_blob_sha1":SHA,
      "protocol":"per battery train first floor(0.6*n), predict remaining cycles once, no test updates",
      "n_total":sum(r["n"] for r in result.values()),
      "n_heldout":sum(r["test_n"] for r in result.values()),
      "limits":"Only four cells; time-correlated errors; Student t coverage might fail; third-party extraction not independently audited",
      "pooled":pooled,"per_cell":{b:{k:v for k,v in r.items() if k!="plot"} for b,r in result.items()}}
    (root/"report.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("EXTERNAL_BATTERY_EVALUATION",json.dumps(report,sort_keys=True))
    return report

class MethodTests(unittest.TestCase):
    def toy(self,n=168):
        x=np.arange(1,n+1,dtype=float)
        return np.column_stack((x,1.9-.003*x+.003*np.sin(x/4)))
    def test_no_future_data_in_training(self):
        a=self.toy();r1=fit_and_score(a)
        v=a.copy();v[110:,1]+=.3;r2=fit_and_score(v)
        for key in r1["scores"]:
            self.assertAlmostEqual(r1["scores"][key]["last_test_forecast_ah"],
                                   r2["scores"][key]["last_test_forecast_ah"])
        self.assertGreater(abs(r1["scores"]["linear_student_t"]["mae_ah"]-
                               r2["scores"]["linear_student_t"]["mae_ah"]),.05)
    def test_split_counts(self):
        self.assertEqual(fit_and_score(self.toy())["test_n"],68)
        self.assertEqual(fit_and_score(self.toy(132))["test_n"],53)
    def test_gaussian_linear_t_calculation(self):
        r=fit_and_score(self.toy())
        self.assertLess(r["scores"]["linear_student_t"]["mae_ah"],.01)
        self.assertTrue(math.isfinite(r["scores"]["linear_student_t"]["mean_neg_log_score"]))
    def test_dont_accept_wrong_sha(self):
        with self.assertRaises(ValueError):ingest(b"not the pinned dataset")
    def test_reject_scrambled_order(self):
        a=self.toy();a[[0,1]]=a[[1,0]]
        with self.assertRaises(ValueError):fit_and_score(a)
    def test_different_actuals_change_scores_not_predictions(self):
        a=self.toy();r=fit_and_score(a)
        a[120:,1]-=.1;r2=fit_and_score(a)
        self.assertEqual(r["scores"]["quadratic_point_only"]["last_test_forecast_ah"],
                         r2["scores"]["quadratic_point_only"]["last_test_forecast_ah"])
        self.assertNotEqual(r["scores"]["quadratic_point_only"]["mae_ah"],
                            r2["scores"]["quadratic_point_only"]["mae_ah"])
    def test_marginal_coverage_is_probability(self):
        a=self.toy();r=fit_and_score(a)
        c=r["scores"]["linear_student_t"]["coverage_90pct"]
        self.assertGreaterEqual(c,0);self.assertLessEqual(c,1)

if __name__=="__main__":
    if "--self-test" in sys.argv:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    else:
        with urlopen(Request(URL,headers={"User-Agent":"Vulcan-Research-2026-10"}),timeout=40) as response:
            raw=response.read(300001)
        if len(raw)>300000:raise ValueError("Dataset too large")
        run(raw)
