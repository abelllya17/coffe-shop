import pandas as pd
from efficient_apriori import apriori

def get_subcategory_sales(csv_path, top_n=10):
    df = pd.read_excel(csv_path)

    counts = (
        df['product_category']
        .value_counts()
        .head(top_n)
    )

    labels = counts.index.tolist()
    values = counts.values.tolist()

    return labels, values


def generate_rules(csv_path, min_support, min_confidence):
    df = pd.read_excel(csv_path)
    df = df[['transaction_date','transaction_time', 'product_category']]

    items = sorted(df['product_category'].dropna().unique().tolist())

    grouped = df.groupby(
        ['transaction_date', 'transaction_time']
    )['product_category'].apply(list)
    trx = grouped.tolist()

    itemsets, rules = apriori(
        trx,
        min_support=min_support,
        min_confidence=min_confidence
    )

    rules_dict_1to1 = {}
    rules_dict_2to1 = {}

    for r in rules:
        if len(r.lhs) == 1 and len(r.rhs) == 1:
            lhs = list(r.lhs)[0]
            rhs = list(r.rhs)[0]
            rules_dict_1to1.setdefault(lhs, []).append(rhs)

        if len(r.lhs) == 2 and len(r.rhs) == 1:
            lhs = tuple(sorted(r.lhs))
            rhs = list(r.rhs)[0]
            rules_dict_2to1.setdefault(lhs, []).append(rhs)

    return rules_dict_1to1, rules_dict_2to1, items
