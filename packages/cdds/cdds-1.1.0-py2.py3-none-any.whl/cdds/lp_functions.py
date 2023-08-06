import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
## Using pd.set_option to display more columns
pd.set_option('display.max_columns',100)

# from lp_styles import *
# ## Customization Options
# plt.style.use(['fivethirtyeight','seaborn-talk'])
# mpl.rcParams['figure.facecolor']='white'

## additional required imports
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import make_column_transformer, make_column_selector, ColumnTransformer
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn import metrics

SEED = 321
np.random.seed(SEED)

def show_code(function):
    import inspect 
    from IPython.display import display,Markdown, display_markdown
    code = inspect.getsource(function)
    md_txt = f"```python\n{code}\n```"
    return display(Markdown(md_txt))



def get_importances(model, feature_names=None,name='Feature Importance',
                   sort=False, ascending=True):
    """Extracts and returns model.feature_importances_ 
    
    Args:
        model (sklearn estimator): a fit model with .feature_importances_
        feature_names (list/array): the names of the features. Default=None.
                                    If None, extract feature names from model
        name (str): name for the panda's Series. Default is 'Feature Importance'
        sort (bool): controls if importances are sorted by value. Default=False.
        ascending (bool): ascending argument for .sort_values(ascending= ___ )
                            Only used if sort===True.
                            
    Returns:
        Pandas Series with Feature Importances
        """
    import pandas as pd
    
    ## checking for feature names
    if feature_names is None:
        feature_names = model.feature_names_in_
        
    ## Saving the feature importances
    importances = pd.Series(model.feature_importances_, index= feature_names,
                           name=name)
    
    # sort importances
    if sort == True:
        importances = importances.sort_values(ascending=ascending)
        
    return importances



def plot_importance(importances, top_n=None,  figsize=(8,6)):
    # sorting with asc=false for correct order of bars
    
    if top_n==None:
        ## sort all features and set title
        plot_importances = importances.sort_values()
        title = "All Features - Ranked by Importance"

    else:
        ## sort features and keep top_n and set title
        plot_importances = importances.sort_values().tail(top_n)
        title = f"Top {top_n} Most Important Features"

    ## plotting top N importances
    ax = plot_importances.plot(kind='barh', figsize=figsize)
    ax.set(xlabel='Importance', 
           ylabel='Feature Names', 
           title=title)
    
    ## return ax in case want to continue to update/modify figure
    return ax


# from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
def evaluate_regression(model, X_train,y_train, X_test, y_test): 
    """Evaluates a scikit learn regression model using r-squared and RMSE"""
    from sklearn import metrics
    
    ## Training Data
    y_pred_train = model.predict(X_train)
    r2_train = metrics.r2_score(y_train, y_pred_train)
    rmse_train = metrics.mean_squared_error(y_train, y_pred_train, 
                                            squared=False)
    
    print(f"Training Data:\tR^2= {r2_train:.2f}\tRMSE= {rmse_train:.2f}")
        
    
    ## Test Data
    y_pred_test = model.predict(X_test)
    r2_test = metrics.r2_score(y_test, y_pred_test)
    rmse_test = metrics.mean_squared_error(y_test, y_pred_test, 
                                            squared=False)
    
    print(f"Test Data:\tR^2= {r2_test:.2f}\tRMSE= {rmse_test:.2f}")
    

    
### COEFFICIENTS 
# def get_coeffs_linreg(lin_reg, feature_names = None, sort=True,ascending=True,
#                      name='LinearRegression Coefficients'):
#     if feature_names is None:
#         feature_names = lin_reg.feature_names_in_

#     ## Saving the coefficients
#     coeffs = pd.Series(lin_reg.coef_, index= feature_names)
#     coeffs['intercept'] = lin_reg.intercept_
    
#     if sort==True:
#         coeffs = coeffs.sort_values(ascending=ascending)
    
#     return coeffs
def get_coeffs_linreg(lin_reg, feature_names = None, intercept=False,
                      sort=True,ascending=True,
                     name='LinearRegression Coefficients'):
    if feature_names is None:
        feature_names = lin_reg.feature_names_in_

    ## Saving the coefficients
    coeffs = pd.Series(lin_reg.coef_, index= feature_names)
    
    if intercept == True:
        coeffs['intercept'] = lin_reg.intercept_
    
    if sort==True:
        coeffs = coeffs.sort_values(ascending=ascending)
    
    return coeffs

    
def get_coeffs(model, feature_names=None,name='Coefficients',
                   sort=False, ascending=True):
    import warnings
    warnings.warn('Function has been replaced with: get_coeffs_linreg and get_coeffs_logreg')
    
    ## checking for feature names
    if feature_names == None:
        feature_names = model.feature_names_in_

    ## Saving the coefficients
    coeffs = pd.Series(model.coef_, index= feature_names)
    coeffs['intercept'] = model.intercept_
    coeffs.name = name

    # sort importances
    if sort == True:
        coeffs = coeffs.sort_values(ascending=ascending)
        
    return coeffs


# def get_coeffs_logreg(logreg, feature_names = None, sort=True,ascending=True,
#                       name='LogReg Coefficients', class_index=0, 
#                       include_intercept=False, as_odds=False):
#     if feature_names is None:
#         feature_names = logreg.feature_names_in_
        
    
#     ## Saving the coefficients
#     coeffs = pd.Series(logreg.coef_[class_index],
#                        index= feature_names, name=name)
    
#     if include_intercept:
#         # use .loc to add the intercept to the series
#         coeffs.loc['intercept'] = logreg.intercept_[class_index]
        
#     if as_odds==True:
#         coeffs = np.exp(coeffs)

#     if sort == True:
#         coeffs = coeffs.sort_values(ascending=ascending)
    
        
#     return coeffs
def get_coeffs_logreg(logreg, feature_names = None, sort=True,ascending=True,
                      name='LogReg Coefficients', class_index=0):
    
    if feature_names is None:
        feature_names = logreg.feature_names_in_
        

    ## Saving the coefficients
    coeffs = pd.Series(logreg.coef_[class_index],
                       index= feature_names, name=name)
    
    # use .loc to add the intercept to the series
    coeffs.loc['intercept'] = logreg.intercept_[class_index]

    if sort == True:
        coeffs = coeffs.sort_values(ascending=ascending)
        
    return coeffs


# def plot_coeffs(coeffs, top_n=None,  figsize=(8,6)):

#     if top_n==None:
#         ## sort all features and set title
#         plot_vals = coeffs.sort_values()
#         title = "All Coefficients - Ranked by Magnitude"

#     else:
#         ## rank the coeffs and select the top_n
#         coeff_rank = coeffs.abs().rank().sort_values(ascending=False)
#         top_n_features = coeff_rank.head(top_n)

#         plot_vals = coeffs.loc[top_n_features.index].sort_values()
#         ## sort features and keep top_n and set title
#         title = f"Top {top_n} Largest Coefficients"

#     ## plotting top N importances
#     ax = plot_vals.plot(kind='barh', figsize=figsize)
#     ax.set(xlabel='Coefficient', 
#            ylabel='Feature Names', 
#            title=title)
#     ax.axvline(0, color='k')
    
#     ## return ax in case want to continue to update/modify figure
#     return ax
def plot_coeffs(coeffs, top_n=None,  figsize=(4,5), intercept=False,
                annotate=False, ha='left', va='center', size=12, xytext=(4,0),
                textcoords='offset points'):
    
    if intercept==False:
        coeffs = coeffs.drop('intercept')
        
    if top_n==None:
        ## sort all features and set title
        plot_vals = coeffs#.sort_values()
        title = "All Coefficients - Ranked by Magnitude"

    else:
        ## rank the coeffs and select the top_n
        coeff_rank = coeffs.abs().rank().sort_values(ascending=False)
        top_n_features = coeff_rank.head(top_n)

        plot_vals = coeffs.loc[top_n_features.index].sort_values()
        ## sort features and keep top_n and set title
        title = f"Top {top_n} Largest Coefficients"

    ## plotting top N importances
    ax = plot_vals.plot(kind='barh', figsize=figsize)
    ax.set(xlabel='Coefficient', 
           ylabel='Feature Names', 
           title=title)
    ax.axvline(0, color='k')
    
    if annotate==True:
        annotate_hbars(ax, ha=ha,va=va,size=size,xytext=xytext,
                       textcoords=textcoords)
    ## return ax in case want to continue to update/modify figure
    return ax


def annotate_hbars(ax, ha='left',va='center',size=12,  xytext=(4,0),
                  textcoords='offset points'):
    for bar in ax.patches:
        
        ## get the value to annotate
        val = bar.get_width()

        if val<0:
            x=0
        else:
            x=val


        ## calculate center of bar
        bar_ax = bar.get_y() + bar.get_height()/2

        # ha and va stand for the horizontal and vertical alignment
        ax.annotate(f"{val:.3f}", (x,bar_ax),ha=ha,va=va,size=size,
                    xytext=xytext, textcoords=textcoords)

        
        

def get_importances(model, feature_names=None,name='Feature Importance',
                   sort=False, ascending=True):
    """Extracts and returns model.feature_importances_ 
    
    Args:
        model (sklearn estimator): a fit model with .feature_importances_
        feature_names (list/array): the names of the features. Default=None.
                                    If None, extract feature names from model
        name (str): name for the panda's Series. Default is 'Feature Importance'
        sort (bool): controls if importances are sorted by value. Default=False.
        ascending (bool): ascending argument for .sort_values(ascending= ___ )
                            Only used if sort===True.
                            
    Returns:
        Pandas Series with Feature Importances
        """
    
    ## checking for feature names
    if feature_names == None:
        feature_names = model.feature_names_in_
        
    ## Saving the feature importances
    importances = pd.Series(model.feature_importances_, index= feature_names,
                           name=name)

    # sort importances
    if sort == True:
        importances = importances.sort_values(ascending=ascending)
        
    return importances




def plot_importance_color(importances, top_n=None,  figsize=(8,6), 
                          color_dict=None):
    """Plots series of feature importances
    
    Args:
        importances (pands Series): importance values to plot
        top_n (int): The # of features to display (Default=None). 
                        If None, display all.
                        otherwise display top_n most important
                        
        figsize (tuple): figsize tuple for .plot
        color_dict (dict): dict with index values as keys with color to use as vals
                            Uses series.index.map(color_dict).
                            
    Returns:
        Axis: matplotlib axis
        """
    # sorting with asc=false for correct order of bars
    if top_n==None:
        ## sort all features and set title
        plot_vals = importances.sort_values()
        title = "All Features - Ranked by Importance"

    else:
        ## sort features and keep top_n and set title
        plot_vals = importances.sort_values().tail(top_n)
        title = f"Top {top_n} Most Important Features"


    ## create plot with colors, if provided
    if color_dict is not None:
        ## Getting color list and saving to plot_kws
        colors = plot_vals.index.map(color_dict)
        ax = plot_vals.plot(kind='barh', figsize=figsize, color=colors)
        
    else:
        ## create plot without colors, if not provided
        ax = plot_vals.plot(kind='barh', figsize=figsize)
        
    # set titles and axis labels
    ax.set(xlabel='Importance', 
           ylabel='Feature Names', 
           title=title)
    
    ## return ax in case want to continue to update/modify figure
    return ax



def get_color_dict(importances, color_rest='#006ba4' , color_top='green', 
                   top_n=7):
    """Constructs a color dictionary where the index of the top_n values will be 
    colored with color_top and the rest will be colored color_rest"""
    ## color -coding top 5 bars
    highlight_feats = importances.sort_values(ascending=True).tail(top_n).index
    colors_dict = {col: color_top if col in highlight_feats else color_rest for col in importances.index}
    return colors_dict
    
# def get_report(model,X_test,y_test,as_df=False,label="TEST DATA"):
#     """Get classification report from sklearn and converts to DataFrame"""
#     ## Get Preds and report
#     y_hat_test = model.predict(X_test)
#     scores = metrics.classification_report(y_test, y_hat_test,
#                                           output_dict=as_df) 
#     ## convert to df if as_df
#     if as_df:
#         report = pd.DataFrame(scores).T.round(2)
#         report.iloc[2,[0,1,3]] = ''
#         return report
#     else:
#         header="\tCLASSIFICATION REPORT"
#         if len(label)>0:
#             header += f" - {label}"
#         dashes='---'*20
#         print(f"{dashes}\n{header}\n{dashes}")
#         print(scores)
        
        
        
def evaluate_classification(model, X_train,y_train,X_test,y_test,
                            normalize='true',cmap='Blues', figsize=(10,5)):
    header="\tCLASSIFICATION REPORT"
    dashes='--'*40
    print(f"{dashes}\n{header}\n{dashes}")

    ## training data
    print(f"[i] Training Data:")
    y_pred_train = model.predict(X_train)
    report_train = metrics.classification_report(y_train, y_pred_train)
    print(report_train)

    fig,ax = plt.subplots(figsize=figsize,ncols=2)
    metrics.ConfusionMatrixDisplay.from_estimator(model,X_train,y_train,
                                                  normalize=normalize, 
                                                  cmap=cmap,ax=ax[0])
    metrics.RocCurveDisplay.from_estimator(model,X_train,y_train,ax=ax[1])
    ax[1].plot([0,1],[0,1],ls=':')
    ax[1].grid()
    fig.tight_layout()
    plt.show()
    
    print(dashes)
    ## training data
    print(f"[i] Test Data:")
    y_pred_test = model.predict(X_test)
    report_test = metrics.classification_report(y_test, y_pred_test)
    print(report_test)

    fig,ax = plt.subplots(figsize=figsize,ncols=2)
    metrics.ConfusionMatrixDisplay.from_estimator(model,X_test,y_test,
                                                  normalize=normalize, 
                                                  cmap=cmap, ax=ax[0])
    metrics.RocCurveDisplay.from_estimator(model,X_test,y_test,ax=ax[1])
    ax[1].plot([0,1],[0,1],ls=':')
    ax[1].grid()
    fig.tight_layout()
    plt.show()
    
    
def get_colors_gt_lt(coeffs, threshold=1, color_lt ='darkred', 
                    color_gt='forestgreen',color_else='gray'):
    """Creates a dictionary of features:colors based on if value is > or < threshold"""
    
    colors_dict = {}

    for i in coeffs.index:

        rounded_coeff = np.round( coeffs.loc[i],3)

        if rounded_coeff < threshold:
            color = color_lt

        elif rounded_coeff > threshold:
            color = color_gt

        else:
            color=color_else

        colors_dict[i] = color
        
    return colors_dict


def plot_coeffs_color(coeffs, top_n=None,  figsize=(8,6), intercept=False,
                      legend_loc='best', threshold=None, 
                      color_lt='darkred', color_gt='forestgreen',
                      color_else='gray', label_thresh='Equally Likely',
                      label_gt='More Likely', label_lt='Less Likely',
                      plot_kws = {}):
    """Plots series of coefficients
    
    Args:
        ceoffs (pands Series): importance values to plot
        top_n (int): The # of features to display (Default=None). 
                        If None, display all.
                        otherwise display top_n most important
                        
        figsize (tuple): figsize tuple for .plot
        color_dict (dict): dict with index values as keys with color to use as vals
                            Uses series.index.map(color_dict).
        plot_kws (dict): additional keyword args accepted by panda's .plot
                            
    Returns:
        Axis: matplotlib axis
        """
    
    # sorting with asc=false for correct order of bars
    
    if intercept==False:
        coeffs = coeffs.drop('intercept')
    
    if top_n is None:
        ## sort all features and set title
        plot_vals = coeffs.sort_values()
        title = "All Coefficients"

    else:
        ## rank the coeffs and select the top_n
        coeff_rank = coeffs.abs().rank().sort_values(ascending=False)
        top_n_features = coeff_rank.head(top_n)

        plot_vals = coeffs.loc[top_n_features.index].sort_values()
        ## sort features and keep top_n and set title
        title = f"Top {top_n} Largest Coefficients"
        
    ## plotting top N importances
    if threshold is not None:
        color_dict = get_colors_gt_lt(plot_vals, threshold=threshold,
                                      color_gt=color_gt,color_lt=color_lt,
                                      color_else=color_else)
        ## Getting color list and saving to plot_kws
        colors = plot_vals.index.map(color_dict)
        plot_kws.update({'color':colors})
        

    ax = plot_vals.plot(kind='barh', figsize=figsize,**plot_kws)
    ax.set(xlabel='Coefficient', 
           ylabel='Feature Names', 
           title=title)
    
    if threshold is not None:
        ln1 = ax.axvline(threshold,ls=':',color='black')

        from matplotlib.patches import Patch
        box_lt = Patch(color=color_lt)
        box_gt = Patch(color=color_gt)

        handles = [ln1,box_gt,box_lt]
        labels = [label_thresh,label_gt,label_lt]
        ax.legend(handles,labels, loc=legend_loc)
    ## return ax in case want to continue to update/modify figure
    return ax


# def annotate_bars(ax, ha='left',va='center',size=12,
#                 xytext=(4,0), textcoords='offset points'):
#     for bar in ax.patches:

#         ## calculate center of bar
#         bar_ax = bar.get_y() + bar.get_height()/2

#         ## get the value to annotate
#         val = bar.get_width()

#         # ha and va stand for the horizontal and vertical alignment
#         ax.annotate(f"{val:.3f}", (val,bar_ax),ha=ha,va=va,size=size,
#                     xytext=xytext, textcoords=textcoords)


## ADMIN VERSION 
def evaluate_classification_admin(model, X_train=None,y_train=None,X_test=None,y_test=None,
                            normalize='true',cmap='Blues', label= ': (Admin)', figsize=(10,5)):
    header="\tCLASSIFICATION REPORT " + label
    dashes='--'*40
    print(f"{dashes}\n{header}\n{dashes}")
    
    if (X_train is None) & (X_test is None):
        raise Exception("Must provide at least X_train & y_train or X_test and y_test")
    
    if (X_train is not None) & (y_train is not None):
        ## training data
        print(f"[i] Training Data:")
        y_pred_train = model.predict(X_train)
        report_train = metrics.classification_report(y_train, y_pred_train)
        print(report_train)

        fig,ax = plt.subplots(figsize=figsize,ncols=2)
        metrics.ConfusionMatrixDisplay.from_estimator(model,X_train,y_train,
                                                      normalize=normalize, 
                                                      cmap=cmap,ax=ax[0])
        try:
            metrics.RocCurveDisplay.from_estimator(model,X_train,y_train,ax=ax[1])
            ax[1].plot([0,1],[0,1],ls=':')
            ax[1].grid()
        except:
            fig.delaxes(ax[1])
        fig.tight_layout()

        plt.show()

    
        print(dashes)

        
    if (X_test is not None) & (y_test is not None):
        ## training data
        print(f"[i] Test Data:")
        y_pred_test = model.predict(X_test)
        report_test = metrics.classification_report(y_test, y_pred_test)
        print(report_test)

        fig,ax = plt.subplots(figsize=figsize,ncols=2)
        metrics.ConfusionMatrixDisplay.from_estimator(model,X_test,y_test,
                                                      normalize=normalize, 
                                                      cmap=cmap, ax=ax[0])
        try:
            metrics.RocCurveDisplay.from_estimator(model,X_test,y_test,ax=ax[1])
            ax[1].plot([0,1],[0,1],ls=':')
            ax[1].grid()
        except:
            fig.delaxes(ax[1])
        fig.tight_layout()
        plt.show()
        
        