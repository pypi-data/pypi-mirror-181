# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: psm_two_group.py
# @AUthor: Fei Wu
# @Time: 12月, 07, 2022
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, f1_score
from matplotlib import pyplot as plt
from scipy import stats
from lightgbm import LGBMClassifier
sns.set(style='darkgrid', context='talk')
import statsmodels.api as sm
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
import numba as nb

class PsmData(object):
    def __init__(self, data, treatment='treatment', exclude_vars=[]):
        self.data = data.copy()
        self.treatment = treatment
        self.select_vars = self.data.drop(columns=[treatment] + exclude_vars).columns.tolist()
        if self.data[treatment].nunique() != 2:
            raise Warning('treatment has {} different values not 2'.format(self.data[treatment].nunique()))
        elif self.data[treatment].max() != 1 and self.data[treatment].max() != 0:
            raise Warning('treament has other values not 0 and 1, please mapping it to be 0 and 1')
        return

    def propensity_score(self, method=LogisticRegression()):
        X = self.data[self.select_vars]
        t = self.data[self.treatment]
        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('method', method)
        ])
        pipe.fit(X,t)
        self.data['proba'] = pipe.predict_proba(X)[:,1]
        self.data['logit'] = np.log(self.data['proba'] / (1 - self.data['proba']))
        print(f"AUC: {roc_auc_score(self.data[self.treatment], self.data['proba']):.4f}" )
        return pipe

    @nb.jit()
    def matching(self, left_match=1, right_match=0, k=1, caliper=None, replace=True):
        g1, g2 = self.data[self.data[self.treatment] == left_match]['proba'], self.data[self.data[self.treatment] == right_match]['proba']
        m_order = list(np.random.permutation(self.data[self.data[self.treatment]==left_match].index))
        matches={}
        #按评分距离匹配
        for m in m_order:
            dist = abs(g1[m] - g2)
            array = np.array(dist)
            if k < len(array):
                k_smallest = np.partition(array, k)[:k].tolist()
                if caliper:
                    caliper = float(caliper)
                    keep_diffs = [i for i in k_smallest if i <= caliper]
                    keep_ids = np.array(dist[dist.isin(keep_diffs)].index)
                else:
                    keep_ids = np.array(dist[dist.isin(k_smallest)].index)
                if len(keep_ids) > k:
                    matches[m] = list(np.random.choice(keep_ids, k, replace=False))
                elif len(keep_ids) < k:
                    while len(matches[m]) <= k:
                        matches[m].append("NA")
                else:
                    matches[m] = keep_ids.tolist()
                if not replace:
                    try:
                        tem = [i for i in matches[m] if i != 'NA']
                        g2 = g2.drop(tem)
                    except:
                        pass
        matches = pd.DataFrame.from_dict(matches, orient='index')
        matches = matches.reset_index()
        column_names = {}
        column_names['index'] = '基准组'
        for i in range(k):
            column_names[i] = str('匹配_'+str(i+1))
        matches = matches.rename(columns=column_names)
        return matches

    def full_matched_data(self,left_match=1, right_match=0, k=1, caliper=None, replace=True):
        matches = self.matching(left_match,right_match,k,caliper,replace)
        matched_data = matches[['基准组']].merge(self.data, how='left', left_on='基准组', right_index=True)
        matched_data.set_index('基准组', drop=1, inplace=True)
        for i in range(k):
            data2 = matches[['匹配_{}'.format(i+1)]].merge(self.data, how='left', left_on='匹配_{}'.format(i+1), right_index=True)
            data2.set_index('匹配_{}'.format(i+1), drop=1, inplace=True)
            matched_data = pd.concat([matched_data, data2], axis=0)
        return matched_data

    @nb.jit()
    def var_test(self, matchdata):
        results = {}
        matched_data = matchdata.copy()
        print("开始评估匹配...")
        for var in self.select_vars:
            crosstable = pd.crosstab(matched_data['treatment'], matched_data[var])
            if len(matched_data[var].unique().tolist()) <= 10:
                result = stats.chi2_contingency(np.array([crosstable.iloc[0].values, crosstable.iloc[1].values]))[0:3]
                p_val = result[1]
            else:
                p1 = stats.levene(crosstable.iloc[0], crosstable.iloc[1])[1]
                if p1 > 0.05:
                    p_val = stats.ttest_ind(crosstable.iloc[0], crosstable.iloc[1], equal_var=True)[1]
                else:
                    p_val = stats.ttest_ind(crosstable.iloc[0], crosstable.iloc[1], equal_var=False)[1]
            results[var] = p_val
            print("\t" + var + "(" + str(p_val) + ")", end="")
            if p_val < 0.05:
                print(": 未通过")
            else:
                print(": 通过")
        if True in [i < 0.05 for i in results.values()]:
            print("\n变量未全部通过匹配")
        else:
            print("\n变量全部通过匹配")
        return results

    def plot_distribution_single(self,
                            matchdata,
                            varname,
                            c_color='grey',
                            t_color='green',
                            c_label='concrol',
                            t_label='treatment',
                            ):
        if matchdata[varname].nunique() == 2:
            origin = 100 * pd.crosstab(matchdata[self.treatment].replace({1: t_label, 0: c_label}), matchdata[varname], normalize='index')
            origin['all'] = 100
            sns.barplot(data=origin, x=origin.index.astype('str'), y='all',
                        color=c_color, label=matchdata[varname].unique()[0])
            sns.barplot(data=origin, x=origin.index.astype('str'), y='treatment',
                        color=t_color, label=matchdata[varname].unique()[1])
            plt.legend()
            plt.xlabel('')
            plt.ylabel('Percentage');
        else:
            sns.kdeplot(data=matchdata[(matchdata[self.treatment] == 0)], x=varname, shade=True,
                        color=c_color, label=c_label)
            sns.kdeplot(data=matchdata[(matchdata[self.treatment] == 1)], x=varname, shade=True,
                        color=t_color, label=t_label)
            plt.legend()
        return True

    @nb.jit()
    def plot_distribution_list(self,
                               data,
                               c_color='grey',
                               t_color='green',
                               c_label='concrol',
                               t_label='treatment',
                               figsize=(20, 10),
                               subplot_size=None
                               ):
        plt.figure(figsize=figsize)
        if subplot_size is None:
            subplot_size = (1,len(self.select_vars))
        for i in range(len(self.select_vars)):
            plt.subplot(subplot_size[0],subplot_size[1],i+1)
            self.plot_distribution_single(data, self.select_vars[i],)
        return True

if __name__ == '__main__':
    data = pd.read_csv('D:\\项目\\X项目\\拉齐原创、活跃、产能\\match_group_model\\X_创作号拉齐宽表.csv', encoding='utf-8')
    data.set_index('cpid', drop=1, inplace=True)
    data = data[['cp_type','active_index','pubnum','rate_org']].sample(20000)
    data['treatment'] = data['cp_type'].map({'X': 1, 'creator': 0})
    mt = PsmData(data,treatment='treatment',exclude_vars=['cp_type'])
    print(mt.propensity_score(method=LogisticRegression()))
    # print(mt.data.head())
    print(mt.matching().head())
    print(mt.full_matched_data().head())
    matchdata = mt.full_matched_data()
    mt.plot_distribution_list(matchdata)
    plt.show()
    mt.var_test(matchdata)
