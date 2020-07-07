import pandas as pd
import time

# header=None，不将第一行作为head
dataset = pd.read_csv('./Market_Basket_Optimisation.csv', header = None)
# shape为(7501,20)
print(dataset.shape)


# 采用efficient_apriori工具包
def rule1():
    from efficient_apriori import apriori
    start = time.time()
    transactions = []
    for i in range(0, dataset.shape[0]):
        temp = []
        for j in range(0, 20):
            if str(dataset.values[i, j]) != 'nan':
                temp.append(str(dataset.values[i,j]))
        transactions.append(temp)
    itemsets, rules = apriori(transactions, min_support=0.02, min_confidence=0.4)
    print('频繁项集：', itemsets)
    print('关联规则：', rules)
    end = time.time()
    print("用时：", end - start)


# 采用mlxtend.frequent_patterns工具包
def rule2():
    from mlxtend.frequent_patterns import apriori
    from mlxtend.frequent_patterns import association_rules
    pd.options.display.max_columns = 100
    start = time.time()
    transactions = []
    for i in range(0, dataset.shape[0]):
        temp = ""
        for j in range(0, 20):
            if str(dataset.values[i, j]) != 'nan':
                temp += str(dataset.values[i, j]) + "|"
        transactions.append(temp)
    dataset_new = pd.DataFrame(data=transactions)
    dataset_new.columns = ["Market_Basket"]
    # 对数据进行one-hot编码
    dataset_new_hot_encoded = dataset_new.drop("Market_Basket", 1).join(dataset_new.Market_Basket.str.get_dummies("|"))
    dataset_new_hot_encoded = dataset_new_hot_encoded.dropna(axis=1)
    frequent_itemsets = apriori(dataset_new_hot_encoded, min_support=0.05, use_colnames=True)
    frequent_itemsets = frequent_itemsets.sort_values(by="support",ascending=False)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    rules = rules.sort_values(by="lift", ascending=False)
    print("频繁项集：", frequent_itemsets)
    print("关联规则：", rules)
    end = time.time()
    print("用时：", end - start)


rule1()
print('-' * 100)
rule2()