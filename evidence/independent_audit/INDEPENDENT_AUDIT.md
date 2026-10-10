# Project Vulcan — Second Independent Adversarial Audit

**Cutoff:** October 9, 2026. **Submitted materials:** `Vulcan_Decision_Research(1).zip`, `SPEC(1).md` and `RUN_REPORT(1).md` in the original review exchange. **Historical verdict:** conditional acceptance of mathematical implementation; **not** acceptable as empirical inference of actual Vulcan flight safety. Independent reviewer, unaffiliated with ULA, Northrop Grumman, SSC or mission operators.

*English translation of a dated external research artifact. Numeric findings and qualifications are preserved; the original Portuguese audit remains visible in the Git history. Historical claims about tests, publication status and missing files must not be represented as current status.*

## Executive summary

1. **The central arithmetic was independently reproduced** with a separate adaptive-integration implementation (`independent_numeric_check.py`) that does not import the original model. Maximum 4×3 joint error: 4.16e−17. Pure EVSI: **USD 3.98985117488024 million**; wait cost: **USD 44.47099915780434 million**; net waiting gain: **−USD 8.72099915780434 million**.
2. **Test set received:** 14 tests. In this particular audit environment, 13 passed and the pgmpy test could not run because the package was absent (`ModuleNotFoundError`). The submitted package asserted 14/14 in another environment; the auditor could not reproduce that one test locally. This is **not** an inference-code bug diagnosis.
3. **Structural sensitivity:** among 360 grid scenarios at L=USD 1,000 million and C_D=USD 10 million, 359 favor immediate reallocation and one waiting. Over the enlarged 61 loss consequences ×51 delay costs =3,111-cell map: 2,775 cells prefer reallocation **in every one of the 360 scenarios**, 336 exhibit disagreement and **zero** favor waiting under every scenario. The much narrower original two-prior map had 98 wait-in-both cells. This difference reflects widening the uncertainty set; it is not a mathematical contradiction.
4. **Atlas V history:** the earlier record explicitly stops in July 2024, but a further ULA schedule review identified nine 2025–July 2026 Atlas V 551 flights, adding 45 SRB flight exposures. These are **not** 45 physically verified anomaly-free motors and are **GEM 63**, not GEM 63XL. No new exposures were incorporated into the submitted prior.
5. **Inference blockers:** unknown historic revisions/lots, uncalibrated mission and reporting CPTs, abstract backup option with no established contract/compatibility/slot, authorization gate G initially assumed to contain no private information, no verified actual VC4S/3,000 kg direct-GEO compatibility for hypothetical M*, and a highly compressed operational window after LV-01.
6. **Historical publication blocker:** a local Git commit is not public proof of prospective timing. `SHA256SUMS` and `BUILD_RECORD.json` were outside the submitted commit, and no public version release or DOI had then been issued.

## 1. Severity-ranked findings

| ID | Severity | Finding | Classification | Required control |
| --- | --- | --- | --- | --- |
| F01 | High | Beta(3,11) pools 12 booster exposures as one base population despite unknown revisions/lots | Strong inferential assumption; not an algebra bug | Flight/revision/detection contrasts; identify non-identifiability |
| F02 | High | Approval G represented only by P(G given Y), preventing any regulator's private telemetry from informing the decision | Missing information channel | Compare G given Y,Theta,R against G given Y; distinguish decision and undisclosed information |
| F03 | High | Abstract alternative always available now or later for only USD 5m additional charge; slot loss/integration ignored | Operational decision-model discrepancy | Reservation action, lost-slot chance, interface lead time, nonrecoverable cost |
| F04 | High | M* Nov 15–Dec 15, 2026 original window vs LV-01 main signal only at T+14 days | Schedule feasibility constraint | Require Y and G before action D1, plus nonzero integration time |
| F05 | High | Published indeterminacy plot compares only two priors even though 360 scenarios exist | Incomplete presentation | Add full supplied structural envelope; never claim global robustness |
| F06 | Medium-high | M* K>=2 has an assumed 55% loss CPT with no direct stress of that specific cell | Dominant unmeasured assumption | Vary K>=2 consequence and severity CPTs |
| F07 | Medium-high | Secondary Atlas evidence stops July 30, 2024, omitting 45 more 2025–26 exposures | Legitimate historic cutoff, incomplete if describing current record | Separate appendix, no automatic addition to powered prior |
| F08 | Medium | lambda=0 removes all shared p/Theta transfer; lambda=1 assumes maximal conditional sharing | Epistemic mixture choice | Do not treat lambda as measured physical probability |
| F09 | Medium | Booster-free option is excluded, and VC4S direct GEO at 3,000 kg is not proven feasible for M* | Unverified mission feasibility | Keep flag false; identify payload/provider as hypothetical |
| F10 | Medium | Reference missing-at-random disclosure and zero false positives | Observation-model simplification | Add MNAR and flight-dependent historical detection |
| F11 | Medium | LV-01 October 29 tentative date differs from monthly and October 31 secondary listings | Schedule uncertainty | Call it aggregator NET, not ULA-confirmed T0 |
| F12 | Low/publication | Two untracked files, generic 'Research build' author | Incomplete provenance | New commit, verified authorship/license/tag/release, Zenodo configured first |
| F13 | Controlled | 13/14 tests ran; 14th blocked by missing pgmpy | Environment dependency | Pin/install environment and rerun |
| F14 | Acceptable | Gauss–Jacobi integrates polynomial Beta terms rather than replacing p by its mean; joint numerical checks agree | Computationally verified | Keep as mathematical baseline |

## 2. Fact checking and causal distinctions

- **Space Systems Command / GPS III-8:** a March 20, 2026 statement confirms reassignment from ULA to SpaceX during an investigation, with USSF-70 assigned to Vulcan no earlier than summer 2028. It provides **no price for the reallocation**. Source: https://www.ssc.spaceforce.mil/DesktopModules/ArticleCS/Print.aspx?Article=4439687&ModuleId=705&PortalId=3 . Direct HTML access may be blocked; indexed public text was available.
- **Northrop Grumman Q2 2026 10-Q:** USD 71m Q1 unfavorable estimate-at-completion impact for studying/implementing corrective actions; USD 91m in Q2 principally forecast increased GEM 63XL material costs and quantities. Their USD 162m sum is an accounting impact, **not per-mission cash investigation cost**. https://www.sec.gov/Archives/edgar/data/1133421/000113342126000034/noc-20260630.htm
- **Vulcan flights and public counts:** Cert-1 (2/0), Cert-2 (2/1), USSF-106 (4/0), USSF-87 (4/1). ULA acknowledged a significant motor-performance anomaly on one of USSF-87's four solids while the mission still achieved direct GEO insertion: https://www.ulalaunch.com/about/news-detail/2026/02/12/ula-vulcan-rocket-successfully-launches-the-future-of-defense ; mission configuration: https://www.ulalaunch.com/missions/next-launch/vulcan-ussf-87
- **LV-01:** Next Spaceflight secondary records proposed VC6L/six SRBs and an LEO-optimized Centaur, with October 29, 2026 NET in one interface and October 2026 only in another. Other launch mirrors gave October 31 as an approximation; none was a confirmed T0. ULA has separately described an LEO Centaur variant distinct from the higher-energy version. Sources: https://api.nextspaceflight.com/launches/details/7425 ; https://www.nextspaceflight.com/launches/details/7425 ; https://blog.ulalaunch.com/blog/vulcan-new-centaur-v-version-readies-for-amazon-leo?hs_amp=true
- **Vega-C:** December 21, 2022 to December 5, 2024 equals 715 calendar days; a modified motor test failed June 28, 2023. This provides a schedule-tail/correction-failure **analogy**, not an empirical Vulcan failure likelihood. Sources: https://www.esa.int/Newsroom/Press_Releases/Flight_VV22_failure_Arianespace_and_ESA_appoint_an_independent_inquiry_commission ; https://www.esa.int/Newsroom/Press_Releases/Vega-C_Zefiro40_Test_Independent_Enquiry_Commission_announces_conclusions ; https://www.esa.int/Newsroom/Press_Releases/Double_win_for_Europe_Sentinel-1C_and_Vega-C_take_to_the_skies
- **Post-2024 Atlas:** nine Atlas V 551 missions (Kuiper 1–3, ViaSat-3 F2, Leo 4–8) with five SRBs each add **45 observed booster exposures**. The original 32 exposures through 2024 plus 45 yield a possible 77 exposures, subject to date, ascertainment and GEM 63/GEM 63XL comparability checks. Per-flight sources appear in `atlas_2025_2026_extension.csv`. ULA explicitly identifies GEM 63 on Atlas V 551: https://blog.ulalaunch.com/blog/kuiper-2-atlas-v-to-launch-amazons-next-step-in-journey
- **M* direct GEO:** USSF-106 achieved direct GEO delivery on VC4S. This does not certify M*'s separate 3,000 kg payload or exact orbital requirements. https://www.ulalaunch.com/missions/missions-details/2025/08/13/vulcan-rocket-ushers-in-new-era-of-national-security-space-launch

## 3. Independent reproduction and provenance

| Test | Recorded finding |
| --- | --- |
| 4×3 joint | Independently reconstructed using `scipy.integrate.quad` and Beta(3,11); maximum absolute error 4.16e−17 |
| Pure EVSI | USD 3.98985117488024m, agrees with reference to displayed precision |
| Wait | USD 44.47099915780434m, agrees with source |
| Reallocate now | USD 35.75m, as defined by alternative-provider cost |
| Preferred action | Reallocate in original reference; net waiting gain −USD 8.72099915780434m |
| Test suite | 13/14 passed here; missing pgmpy prevented the remaining run |
| Captures/hashes | 29 raw captures match source manifest SHA-256; 66 checksums match original local files |
| Public registration | No independently verifiable release, DOI or timestamp at that audit cutoff |

**Naming rule:** pure EVSI uses an unchanged counterfactual action set without waiting or authorization costs. Net waiting gain includes modeled approval and costs and can be negative. Arithmetic checks do not authenticate physical CPT probabilities, contracts or detection rates.

### Wider structural envelope

On the original two-prior 3,111-cell map, 98 points favored waiting under both priors; 2,990 favored reallocation under both, and 23 indicated divergence/threshold. Expanding to all 360 structural scenarios gave **zero** cells with unanimous waiting, **2,775** with unanimous reallocation and **336** with disagreement. This is conditional on the stated grid, not a no-go theorem about all possible physically credible scenarios. Deliverables: `structural_envelope.csv`, `structural_envelope.png`.

## 4. Required conceptual changes

**A. Do not infer hardware revision effects from a single Beta posterior.** Four flights treated as 12 exchangeable Bernoulli exposures are defensible only under an explicitly restricted model (stationary hazard, perfect observation, rho=0). Different versions, inspection regimes, lots and physical positions make a broader model partially non-identifiable. Beta(3,11) summarizes a restricted submodel, **not actual revised GEM 63XL hardware reliability**.

**B. Condition decision choices on physically available alternatives.** Reassigning a real sensitive spacecraft requires compatible launcher, certification, schedule, interfaces, integration and contract. GPS III-8 illustrates institutional possibility but does not prove that M* can choose and integrate a backup between LV-01 +14 days and November 15. If G also reflects private evidence, observing G can update risk; treating G independent of Theta given Y as a physical law is unjustified. Model both assumptions explicitly without attributing probabilities to actual Space Force decisions.

## 5. Original October 9–17 freeze plan

- **October 9–11:** source coverage audit; address F01–F05 as documented scenarios or explicit limits; retain strictly hypothetical M*.
- **October 12–13:** vary K>=2 CPT and state-dependent public ascertainment; model private gate information without using future observations to calibrate.
- **October 14:** reproduce pgmpy tests in a pinned environment, checksum results, archive source cutoff.
- **October 15–16:** establish license, actual author, CITATION.cff and tracking commit for build/checksums; complete candidate release review.
- **By October 17:** responsible account enables GitHub–Zenodo repository integration **before** a new release, then publishes and checks an actual version DOI after processing. Without an actual archival record, do not assert independently verifiable ex-ante registration. Documentation: https://help.zenodo.org/docs/github/enable-repository/ and https://help.zenodo.org/docs/github/archive-software/github-upload/

**Explicit scope:** this audit does not perform a hardware safety assessment, establish any anomaly root cause, replace mission authorities or license real launch decisions.

## 6. Methodological literature check

- Heath et al., *Simulating Study Data to Support Expected Value of Sample Information Calculations: A Tutorial*, 2021/2022, https://pmc.ncbi.nlm.nih.gov/articles/PMC8793320/ — distinguishes informational value from net benefit after cost and emphasizes observability. The submitted model uses deterministic enumeration, **not** the tutorial's Monte Carlo estimator.
- Chen & Ibrahim, *Power prior distributions for regression models*, *Statistical Science* 15(1), 46–60 (2000), https://doi.org/10.1214/ss/1009212673 — provides the conceptual framework for likelihood power priors; it does **not** validate physical transfer from GEM 63 to GEM 63XL or correct missing reporting.

## Historical release verdict

**Conditionally accepted:** enumeration core, reference decision arithmetic, initial uncertainty map and value-of-information methods **as a model-conditional decision laboratory**.

**Not approved:** treating modeled CPTs as the real failure probability, recommending certification, claiming causal correction effects, or presenting the study as an already publicly registered prospective forecast.
