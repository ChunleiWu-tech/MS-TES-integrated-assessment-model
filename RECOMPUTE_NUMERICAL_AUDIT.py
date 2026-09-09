"""Recompute the numerical questions in the supplied 36-item editorial review.

Reads the released inputs and outputs without changing them. Additional tables
describe existing comparisons or explicitly labelled evidence-rule sensitivities.
"""
from pathlib import Path
from hashlib import sha256
import importlib.util
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
UP = ROOT / 'upstream_reproducible_code'
T = UP / 'outputs/tables'
OUT = ROOT / 'AUDIT/checklist_review_20260909'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run():
    OUT.mkdir(exist_ok=True, parents=True)
    checks, facts = [], {}
    def check(name, ok, detail=None):
        checks.append(dict(check=name, passed=bool(ok), detail=detail))

    screen = pd.read_csv(T/'expanded_v3_candidate_service_screen.csv')
    candidates = pd.read_csv(T/'expanded_v3_exact_composition_candidate_summary.csv')
    mc = pd.read_csv(T/'expanded_v3_domain_validated_thermophysical_mc.csv')
    cols = ['candidate_key','service_id','display_system','composition_basis','normalized_composition',
            'current_registry_system_id','physical_window_pass','service_domain_supported',
            'engineering_registry_linked','formal_assessment_status']
    mapping = screen[cols].merge(mc[['candidate_key','service_id','thermophysical_rank1_frequency']],
                                how='left', on=['candidate_key','service_id'],validate='one_to_one')
    mapping.to_csv(OUT/'candidate_set_mapping.csv',index=False)
    nk = mapping[mapping.current_registry_system_id.eq('nkca') & mapping.service_id.eq('pcm_target_500C')]
    facts['nkca_pcm500'] = nk.to_dict('records')
    check('NKCA is present in the expanded PCM500 set under Cl-reference',len(nk)==1 and nk.service_domain_supported.all())
    check('supported-pair and registry-intersection counts',int(screen.service_domain_supported.sum())==11 and
          int((screen.service_domain_supported & screen.engineering_registry_linked).sum())==8)

    drawcols = ['scenario','draw_id','system_id','strict_complete','is_balanced_winner','gate_failure_count']
    draws = pd.read_csv(T/'core_monte_carlo_draws_balanced.csv',usecols=drawcols)
    check('engineering selection is a subset of same-draw complete-duty support',
          not (draws.is_balanced_winner & ~draws.strict_complete).any())
    check('selected candidates have no failed gates',not(draws.is_balanced_winner & draws.gate_failure_count.gt(0)).any())
    grouped=draws.groupby(['scenario','system_id'],sort=False).agg(
        draws=('draw_id','size'),formal_count=('is_balanced_winner','sum'),complete_count=('strict_complete','sum')).reset_index()
    grouped['formal_frequency']=grouped.formal_count/grouped.draws
    grouped['complete_frequency']=grouped.complete_count/grouped.draws
    grouped['mc_standard_error']=np.sqrt(grouped.formal_frequency*(1-grouped.formal_frequency)/grouped.draws)
    grouped.to_csv(OUT/'formal_frequency_denominators.csv',index=False)
    facts['solar_frequencies']=grouped[grouped.system_id.eq('solar_salt_ss60')].to_dict('records')

    # Sensitivity changes only the full-window density evidence condition.
    # Phase-change rules, Cp coverage, identity and physical gates remain fixed.
    expanded=module('expanded_checklist',UP/'src/run_expanded_library_v3.py')
    bykey=candidates.set_index('candidate_key')
    density=[]
    for r in screen.itertuples():
        c=bykey.loc[r.candidate_key]; s=expanded.SERVICES[r.service_id]
        full=bool(r.service_domain_supported)
        relaxed=full
        cpok=rhook=False
        if s['mode']=='sensible' and bool(r.physical_window_pass) and bool(r.quantitative_thermophysical_complete):
            lo,hi=float(s['cold_C']),float(s['hot_C'])
            if expanded.clean_text(c.get('current_registry_system_id','')):
                cpok=expanded.domain_covers(c,'cp',lo,hi)
                rhook=expanded.domain_covers(c,'rho',hi,hi)
            else:
                cpok=expanded.conditions_cover(c.get('cp_J_gK_conditions',''),lo,hi)
                rhook=expanded.conditions_cover(c.get('density_kg_m3_conditions',''),hi,hi)
            relaxed=bool(cpok and rhook)
        density.append(dict(candidate_key=r.candidate_key,service_id=r.service_id,display_system=r.display_system,
                            baseline_full_window_support=full,hot_end_density_rule_support=relaxed,
                            cp_full_window_supported=cpok,density_hot_end_supported=rhook))
    density=pd.DataFrame(density)
    density.to_csv(OUT/'density_evidence_rule_sensitivity.csv',index=False)
    facts['density_sensitivity']=density.groupby('service_id')[['baseline_full_window_support','hot_end_density_rule_support']].sum().astype(int).to_dict('index')
    altered=screen.copy()
    altered['service_domain_supported']=density.hot_end_density_rule_support.to_numpy()
    alternate_mc=expanded.monte_carlo_opportunity(candidates,altered,domain_validated_only=True)
    alternate_mc.to_csv(OUT/'density_hot_end_thermophysical_ranking.csv',index=False)
    facts['density_industrial_ranking']=alternate_mc[alternate_mc.service_id.eq('industrial_medium_heat')][
        ['display_system','thermophysical_rank1_frequency','robust_physical_pass_probability']].to_dict('records')

    data=json.loads((UP/'data/input/application_experiments.json').read_text())
    cfg=json.loads((UP/'config/application_assessment.json').read_text())
    condition=pd.read_csv(T/'application_device_conditions.csv')
    pair=pd.read_csv(T/'application_paired_response.csv')
    foam=pair[pair.material.eq('alumina_copper_foam')]
    check('15 of 18 foam heat-release upper sensitivity bounds below one',int(foam.discharge_ratio_high.lt(1).sum())==15 and len(foam)==18)
    check('power sensitivity upper-bound formula',np.allclose(pair.discharge_ratio_high,pair.discharge_ratio*(1+.0236)/(1-.0236),rtol=1e-12))
    boundary=[]
    for study in data['studies']:
        for j,hot in enumerate(study['hot_C']):
            for mi,mat in enumerate(data['material_order']):
                ambient=(13,15) if mat=='base' or (study['source_id']=='XIAO_2023' and mat=='alumina_2wt') else (16,18)
                for k,cold in enumerate(study['cold_C']):
                    ec=study['device_energy']; vol=ent=cap=None
                    if ec:
                        vol=ec['fill_fraction']*np.pi*(ec['diameter_m']**2-ec['inner_pipe_diameter_m']**2)/4*ec['height_m']
                        ent=ec['discharge'][k][j][mi]; cap=ent/(3600*vol)
                    boundary.append(dict(source_id=study['source_id'],doi=study['doi'],material=mat,hot_C=hot,
                        discharge_end_C=cold,charge_initial_C=study['charge_initial_C'],ambient_low_C=ambient[0],ambient_high_C=ambient[1],
                        charge_condition_key=f"{study['source_id']}|{mat}|{hot}|{study['charge_initial_C']}",
                        discharge_condition_key=f"{study['source_id']}|{mat}|{hot}|{cold}",
                        pair_key=f"{study['source_id']}|{mat}|{hot}|{cold}",charge_power_kW_m3=study['charge_power'][j][mi],
                        discharge_power_kW_m3=study['discharge_power'][k][j][mi],effective_filled_volume_m3=vol,
                        source_calculated_discharge_enthalpy_kJ=ent,capacity_kWh_m3=cap,
                        source_locator=study['locator'],boundary=study['boundary'],source_conflict=study['source_conflict'],
                        ambient_locator='printed p.81, Section 3.3' if study['source_id']=='XIAO_2023' else 'accepted manuscript p.21, Section 3.2'))
    pd.DataFrame(boundary).to_csv(OUT/'device_boundary_and_capacity_ledger.csv',index=False)
    app=module('application_checklist',UP/'src/run_application_assessment.py')
    chrono=[]
    for r in condition[condition.capacity_kWh_m3.notna()].itertuples():
        for archetype in cfg['application_archetypes']:
            for dt in cfg['chronological_dt_h']:
                tc,td=archetype['charge_h'],archetype['discharge_h']
                v,res,state,qc,qd=app.dispatch_lp(r.charge_power_kW_m3,r.discharge_power_kW_m3,r.capacity_kWh_m3,tc,td,dt)
                ein,eout=float(qc.sum()*dt),float(qd.sum()*dt)
                chrono.append(dict(source_id=r.source_id,material=r.material,hot_C=r.hot_C,cold_C=r.cold_C,
                    archetype=archetype['id'],dt_h=dt,charge_h=tc,delivery_h=td,charge_to_delivery_energy_ratio=1,
                    input_energy_kWh=ein,output_energy_kWh=eout,loss_kWh=0,initial_inventory_kWh=state[0],
                    terminal_inventory_kWh=state[-1],energy_balance_residual_kWh=abs(ein-eout),
                    maximum_step_residual_kWh=res,lp_volume_m3=v,solver_status='optimal'))
    chrono=pd.DataFrame(chrono)
    chrono.to_csv(OUT/'chronological_energy_balance.csv',index=False)
    check('162 rerun LP cases close energy with zero endpoints',len(chrono)==162 and
          chrono.energy_balance_residual_kWh.max()<1e-10 and chrono.maximum_step_residual_kWh.max()<1e-10 and
          np.allclose(chrono.initial_inventory_kWh,0) and np.allclose(chrono.terminal_inventory_kWh,0))
    facts['chronology']=dict(cases=len(chrono),max_balance_residual=float(chrono.energy_balance_residual_kWh.max()),
                            max_step_residual=float(chrono.maximum_step_residual_kWh.max()),factorization='3 materials x 3 hot endpoints x 3 discharge endpoints x 3 time windows x 2 time steps')
    facts['input_hashes']={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in
                          [UP/'data/input/application_experiments.json',UP/'config/application_assessment.json',T/'core_monte_carlo_draws_balanced.csv']}
    result=dict(checks=checks,facts=facts,status='PASS' if all(c['passed'] for c in checks) else 'FAIL',
                scope='Targeted numerical and evidence-boundary audit; not independent transient validation or empirical calibration of engineering scores.')
    def finite_json(value):
        if isinstance(value,dict):return {k:finite_json(v) for k,v in value.items()}
        if isinstance(value,list):return [finite_json(v) for v in value]
        if isinstance(value,float) and not np.isfinite(value):return None
        return value
    result=finite_json(result)
    (OUT/'NUMERICAL_REVIEW.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--project-root',type=Path,default=ROOT)
    parser.add_argument('--output',type=Path,default=OUT)
    args=parser.parse_args()
    ROOT=args.project_root.resolve();UP=ROOT/'upstream_reproducible_code';T=UP/'outputs/tables';OUT=args.output.resolve()
    run()
