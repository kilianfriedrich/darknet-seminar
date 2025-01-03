import pandas as pd

def get_tracked_status(all_groups, only_active, indexer_dict: dict):
    tracking_status = { 'Group': [] }
    for i in indexer_dict.keys():
        tracking_status[i] = []

    concatted = all_groups
    if only_active:
        concatted = concatted[concatted['Available']]
    total = concatted['Group'].unique()

    for i in indexer_dict.keys():
        indexer = indexer_dict[i]
        if only_active:
            indexer = indexer[indexer['Available']]
        for group in total:
            tracking_status[i].append((indexer['Group'] == group).any())

    for group in total:
        tracking_status['Group'].append(group)

    return pd.DataFrame(tracking_status)