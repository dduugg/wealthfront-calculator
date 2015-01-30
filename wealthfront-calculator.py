#!/usr/bin/env python

import math
import sys
import locale
locale.setlocale(locale.LC_ALL, 'en_US')

# allocations for taxable accounts, by increasing level of risk
TAXABLE_ALLOCATIONS = [
    {'VTI':  8, 'VEA':  5, 'VWO':  5, 'VIG': 15, 'DJP':  7, 'MUB': 35, 'SCHP': 25},  # 0.5
    {'VTI': 20, 'VEA':  5, 'VWO':  5, 'VIG':  7, 'DJP':  5, 'MUB': 35, 'SCHP': 23},  # 1.0
    {'VTI': 23, 'VEA':  7, 'VWO':  5, 'VIG':  7, 'DJP':  5, 'MUB': 35, 'SCHP': 18},  # 1.5
    {'VTI': 25, 'VEA':  9, 'VWO':  5, 'VIG':  8, 'DJP':  5, 'MUB': 35, 'SCHP': 13},  # 2.0
    {'VTI': 26, 'VEA': 11, 'VWO':  5, 'VIG':  8, 'DJP':  6, 'MUB': 35, 'SCHP':  9},  # 2.5
    {'VTI': 27, 'VEA': 12, 'VWO':  6, 'VIG':  8, 'DJP':  6, 'MUB': 35, 'SCHP':  6},  # 3.0
    {'VTI': 30, 'VEA': 13, 'VWO':  8, 'VIG':  8, 'DJP':  6, 'MUB': 35},              # 3.5
    {'VTI': 30, 'VEA': 13, 'VWO':  9, 'VIG':  7, 'DJP':  6, 'MUB': 35},              # 4.0
    {'VTI': 32, 'VEA': 14, 'VWO': 11, 'VIG':  5, 'DJP':  5, 'MUB': 33},              # 4.5
    {'VTI': 33, 'VEA': 15, 'VWO': 12, 'VIG':  6, 'DJP':  5, 'MUB': 29},              # 5.0
    {'VTI': 34, 'VEA': 16, 'VWO': 13, 'VIG':  6, 'DJP':  5, 'MUB': 26},              # 5.5
    {'VTI': 35, 'VEA': 17, 'VWO': 14, 'VIG':  6, 'DJP':  5, 'MUB': 23},              # 6.0
    {'VTI': 35, 'VEA': 18, 'VWO': 15, 'VIG':  6, 'DJP':  5, 'MUB': 21},              # 6.5
    {'VTI': 35, 'VEA': 20, 'VWO': 15, 'VIG':  7, 'DJP':  5, 'MUB': 18},              # 7.0
    {'VTI': 35, 'VEA': 21, 'VWO': 16, 'VIG':  8, 'DJP':  5, 'MUB': 15},              # 7.5
    {'VTI': 35, 'VEA': 22, 'VWO': 17, 'VIG':  8, 'DJP':  5, 'MUB': 13},              # 8.0
    {'VTI': 35, 'VEA': 24, 'VWO': 18, 'VIG':  9, 'DJP':  5, 'MUB':  9},              # 8.5
    {'VTI': 35, 'VEA': 25, 'VWO': 19, 'VIG': 10, 'DJP':  5, 'MUB':  6},              # 9.0
    {'VTI': 35, 'VEA': 26, 'VWO': 22, 'VIG':  7, 'DJP':  5, 'MUB':  5},              # 9.5
    {'VTI': 35, 'VEA': 22, 'VWO': 28, 'VIG':  5, 'DJP':  5, 'MUB':  5}]             # 10.0

# allocations for retirement accounts, by increasing level of risk
RETIREMENT_ALLOCATIONS = [
    {'VTI':  6, 'VEA':  5, 'VWO':  5, 'VIG':  5, 'VNQ':  5, 'LQD': 35, 'EMB': 14, 'SCHP': 25},  # 0.5
    {'VTI':  8, 'VEA':  5, 'VWO':  5, 'VIG': 11, 'VNQ':  5, 'LQD': 35, 'EMB': 12, 'SCHP': 19},  # 1.0
    {'VTI': 12, 'VEA':  5, 'VWO':  5, 'VIG': 12, 'VNQ':  5, 'LQD': 35, 'EMB': 12, 'SCHP': 14},  # 1.5
    {'VTI': 15, 'VEA':  6, 'VWO':  5, 'VIG': 12, 'VNQ':  5, 'LQD': 35, 'EMB': 13, 'SCHP':  9},  # 2.0
    {'VTI': 16, 'VEA':  8, 'VWO':  5, 'VIG': 13, 'VNQ':  5, 'LQD': 35, 'EMB': 13, 'SCHP':  5},  # 2.5
    {'VTI': 17, 'VEA': 10, 'VWO':  6, 'VIG': 14, 'VNQ':  5, 'LQD': 35, 'EMB': 13},              # 3.0
    {'VTI': 17, 'VEA': 11, 'VWO':  7, 'VIG': 15, 'VNQ':  5, 'LQD': 35, 'EMB': 10},              # 3.5
    {'VTI': 18, 'VEA': 12, 'VWO':  8, 'VIG': 15, 'VNQ':  6, 'LQD': 31, 'EMB': 10},              # 4.0
    {'VTI': 18, 'VEA': 13, 'VWO':  9, 'VIG': 15, 'VNQ':  8, 'LQD': 28, 'EMB':  9},              # 4.5
    {'VTI': 18, 'VEA': 14, 'VWO': 10, 'VIG': 15, 'VNQ':  9, 'LQD': 25, 'EMB':  9},              # 5.0
    {'VTI': 19, 'VEA': 15, 'VWO': 11, 'VIG': 15, 'VNQ': 10, 'LQD': 21, 'EMB':  9},              # 5.5
    {'VTI': 19, 'VEA': 16, 'VWO': 12, 'VIG': 15, 'VNQ': 11, 'LQD': 19, 'EMB':  8},              # 6.0
    {'VTI': 20, 'VEA': 17, 'VWO': 13, 'VIG': 15, 'VNQ': 12, 'LQD': 15, 'EMB':  8},              # 6.5
    {'VTI': 20, 'VEA': 17, 'VWO': 14, 'VIG': 15, 'VNQ': 13, 'LQD': 13, 'EMB':  8},              # 7.0
    {'VTI': 21, 'VEA': 18, 'VWO': 15, 'VIG': 15, 'VNQ': 14, 'LQD': 10, 'EMB':  7},              # 7.5
    {'VTI': 22, 'VEA': 19, 'VWO': 16, 'VIG': 15, 'VNQ': 15, 'LQD':  6, 'EMB':  7},              # 8.0
    {'VTI': 23, 'VEA': 19, 'VWO': 17, 'VIG': 15, 'VNQ': 15, 'LQD':  5, 'EMB':  6},              # 8.5
    {'VTI': 21, 'VEA': 18, 'VWO': 22, 'VIG': 13, 'VNQ': 16, 'LQD':  5, 'EMB':  5},              # 9.0
    {'VTI': 21, 'VEA': 18, 'VWO': 27, 'VIG':  8, 'VNQ': 16, 'LQD':  5, 'EMB':  5},              # 9.5
    {'VTI': 20, 'VEA': 18, 'VWO': 31, 'VIG':  5, 'VNQ': 16, 'LQD':  5, 'EMB':  5}]             # 10.0


def dollar_allocation_for_risk(risk_level, allocations, dollars):
    dollar_allocations = {}
    allocations_last_index = len(allocations) - 1
    allocation_index_to_interpolate = risk_level * allocations_last_index
    lower_allocation_level = int(math.floor(allocation_index_to_interpolate))
    upper_allocation_level = min(lower_allocation_level + 1, allocations_last_index)
    lower_weighting = 1 - (allocation_index_to_interpolate - lower_allocation_level)
    upper_weighting = 1 - lower_weighting
    lower_allocation = allocations[lower_allocation_level]
    upper_allocation = allocations[upper_allocation_level]
    _funds = set(lower_allocation) | set(upper_allocation)
    for _fund in _funds:
        interpolated_fund_weight = lower_weighting * lower_allocation.get(_fund, 0) \
            + upper_weighting * upper_allocation.get(_fund, 0)
        dollar_allocations[_fund] = dollars * interpolated_fund_weight / 100.0
    return dollar_allocations

taxable_dollars = float(sys.argv[1])
retirement_dollars = float(sys.argv[2])
other_funds = float(sys.argv[3]) if len(sys.argv) > 3 else 0
goal = float(sys.argv[4]) if len(sys.argv) > 4 else 1000000

risk = 1 - ((taxable_dollars + retirement_dollars + other_funds) / goal)
risk = min(risk, 1)
risk = max(risk, 0)
# rescale to actual wealthfront risk range of 0.5 - 1.0:
wf_risk = (0.95 * risk) + 0.05
print "risk:", locale.format("%.1f", wf_risk * 10)

taxable_dollar_allocation = dollar_allocation_for_risk(risk, TAXABLE_ALLOCATIONS, taxable_dollars)
retirement_dollar_allocation = dollar_allocation_for_risk(risk, RETIREMENT_ALLOCATIONS, retirement_dollars)

combined_dollar_allocation = {}
funds = set(taxable_dollar_allocation.keys()) | set(retirement_dollar_allocation.keys())
max_amount_len = 0
max_fund_len = 0
for fund in funds:
    amount = taxable_dollar_allocation.get(fund, 0) + retirement_dollar_allocation.get(fund, 0)
    amount_str = locale.format("%.0f", amount, grouping=True)
    max_amount_len = max(max_amount_len, len(amount_str))
    max_fund_len = max(max_fund_len, len(fund))
    combined_dollar_allocation[fund] = amount

for fund in sorted(combined_dollar_allocation, key=combined_dollar_allocation.get, reverse=True):
    amount = locale.format("%.0f", combined_dollar_allocation[fund], grouping=True)
    print "%-*s $" % (max_fund_len + 1, fund + ":") + str(amount).rjust(max_amount_len)
