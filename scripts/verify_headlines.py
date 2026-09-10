#!/usr/bin/env python3
"""Verify public headline metrics directly from experiment evidence."""
from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parents[1]

def load(exp,name='summary.json'):
    return json.loads((ROOT/'experiments'/f'{exp:03d}'/'evidence'/name).read_text())

def close(a,b,tol=1e-9):
    if not math.isclose(float(a),float(b),rel_tol=tol,abs_tol=tol):
        raise AssertionError(f'{a} != {b}')

# E016
x=load(16); close(x['primary_result']['final_oracle_tok_s_per_user'],2.6691235692169797); assert x['verdict']=='FAIL'
# E017
x=load(17); close(x['primary_result']['oracle_tok_s_per_user'],3.099405677205971); assert x['verdict']=='FAIL'
# E018
x=load(18); close(x['headline']['tok_s_per_user'],6.702244850841379); close(x['headline']['pipeline_efficiency'],0.837624017144624); assert x['outcome']=='PASS_STRONG'
# E019
x=load(19); assert x['classification']=='MODEL_INVALID'; assert x['throughput_claim_admissible'] is False; close(x['bottom_up_reconstruction_error_percent'],103.9074196885888)
r=json.loads((ROOT/'experiments'/'019'/'evidence'/'correctness'/'full-93-sharded-receipt.public.json').read_text()); assert r['status']=='PASS'; assert r['executed_layers']==93; close(r['maximum_relative_l2_error'],1.270798958977163e-06)
# E020
x=load(20); assert x['classification']=='E021_NOT_READY'; assert x['any_gpu_rented'] is False; assert x['projection_validation_status']=='FAIL'
# E021
x=load(21); assert x['outcome']=='MODEL_INVALID'; close(x['model_validation']['median_error']*100,95.5390936021116)
# E022
x=load(22); assert x['verdict']=='MODEL_INVALID'; assert x['statistics']['capacity_unlocks']==6
r=json.loads((ROOT/'experiments'/'022'/'evidence'/'run-result.json').read_text()); close(r['model_validation']['ordered_validation']['median_percent'],2.713617684164345); assert r['model_validation']['normalization_applied'] is False
# E026
x=load(26); assert x['canonical_verdict']=='WAN_SWARM_NOT_VIABLE_UNDER_TESTED_CONDITIONS'; close(x['major_results']['best_exact_wan_tok_s'],1.6150520769635919); close(x['major_results']['sealed_partial_wan_tok_s'],0.5903353469265896); close(x['major_results']['disk_warm_same_shard_speedup'],103.18658650185198); close(x['major_results']['recovery_interruption_s'],9.508302600002935); assert x['major_results']['sealed_completed_of_requested_tokens']==[282,512]
r=json.loads((ROOT/'experiments'/'026'/'evidence'/'final-receipt.json').read_text()); assert r['dataset']['rows']==71; assert r['gates']['interactive_decode']['pass'] is False; assert r['gates']['distributed_correctness']['pass'] is False; assert r['gates']['sealed_512_tokens']['pass'] is False
print('PASS: all public headline metrics match the curated experiment evidence.')
