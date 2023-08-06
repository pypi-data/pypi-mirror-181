这是用于拉齐原创、活跃、产能的python包，通过输入两个群体的原创率、活跃度、发文量，通过PSM的方式得到可匹配的两群体样本，并进行返回。
下面是该程序包的使用介绍：
#数据处理
data = pd.read_csv('D:\\项目\\X项目\\拉齐原创、活跃、产能\\X_创作号拉齐宽表.csv', encoding='utf-8')

data.set_index('cpid', drop=1, inplace=True)

data = data[['cp_type','active_index','pubnum','rate_org']].sample(20000)

data['treatment'] = data['cp_type'].map({'X': 1, 'creator': 0})
#实例化
mt = PsmData(data,treatment='treatment',exclude_vars=['cp_type'])
#获取评分
print(mt.propensity_score(method=LogisticRegression()))
#得到匹配的index
print(mt.matching(left_match=1, right_match=0, k=1, caliper=None, replace=True).head())
#得到匹配后的两群体样本
print(mt.full_matched_data(left_match=1, right_match=0, k=1, caliper=None, replace=True).head())
#绘制分布图
matchdata = mt.full_matched_data()
mt.plot_distribution_list(matchdata)
plt.show()
