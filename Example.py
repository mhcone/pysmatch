import warnings

warnings.filterwarnings('ignore')
from pysmatch.Matcher import Matcher
import pandas as pd
import numpy as np

print('get data')
path = "misc/loan.csv"
data = pd.read_csv(path)

test = data[data.loan_status == "Default"]
control = data[data.loan_status == "Fully Paid"]
print('get data')

test['loan_status'] = 1
control['loan_status'] = 0

m = Matcher(test, control, yvar="loan_status", exclude=[])

# for reproducibility
np.random.seed(20240919)

m.fit_scores(balance=True, nmodels=10,n_jobs=3,model_type='knn')
# m.fit_scores(balance=True, nmodels=10, n_jobs=3, model_type='tree', max_iter=100)
# m.fit_scores(balance=True, nmodels=10,n_jobs=3,model_type='linear', max_iter=200)


m.predict_scores()

m.plot_scores()
m.tune_threshold(method='random')
m.match(method="min", nmatches=1, threshold=0.0001, replacement=False)

m.record_frequency()
m.assign_weight_vector()
print("top 6 matched data")
print(m.matched_data.sort_values("match_id").head(6))
categorical_results = m.compare_categorical(return_table=True, plot_result=True)
print(categorical_results)
cc = m.compare_continuous(return_table=True, plot_result=True)
print(cc)
