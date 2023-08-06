import pandas as pd
from sklearn.model_selection import  cross_validate

def enhance_cross_validate(model, X_train, y_train, with_sd = True,**kwargs):
    scores = cross_validate(model, X_train, y_train, **kwargs)
    
    mean_scores = pd.DataFrame(scores).mean()
    if with_sd:
        std_scores = pd.DataFrame(scores).std()
    out_col = []
    if (with_sd):
        for i in range(len(mean_scores)):
            out_col.append((f"%0.3f (+/- %0.3f)" % (mean_scores[i], std_scores[i])))
    else:
        for i in range(len(mean_scores)):
            out_col.append((f"%0.3f" % (mean_scores[i])))
    return pd.Series(data=out_col, index=mean_scores.index)


def getInfo():
    return "mltz"