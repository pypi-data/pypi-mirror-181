"""
module plots.py
----------------------
 Utility functions for creatings commonly used plots.
"""
from sklearn import metrics
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# %matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns



def clock_time_plot(fig, ax, df, col_name, fill_color='gray', line_color='black'):
    with plt.style.context('default') as ctx:
        sns.set_context(ctx)
        sns.set_style('darkgrid', {'axes.facecolor': '0.9'})
        if ax is None:
            fig, ax = plt.subplots(
                1, 1, 
                figsize=(40, 8), 
                subplot_kw=dict(projection='polar', polar=True)
            )  # plt.subplot(111, polar=True)

        aux = df.groupby(
            df.loc[:, col_name].dt.hour
        )[col_name].count() / df.shape[0]

        # 24 angulos de 0 a 360
        equals = np.linspace(0, 360, 24, endpoint=False) #np.arange(24)
        # Alternatively, you could have changed your definition of equals to produce angles in terms of radians: 
        # equals = np.linspace(0, 2*np.pi, 24, endpoint=False)
        radians = np.deg2rad(equals)

        # ones = np.ones(24)
        ax.plot(
            np.concatenate([radians,  [0.] ]), 
            np.concatenate([aux.values, [aux.values[0]] ]),
            "-o",
            color = line_color,
        )       
        ax.fill(
            np.concatenate([radians,  [0.]]), 
            np.concatenate([aux.values, [aux.values[0]]]),
            color=fill_color,
            alpha=0.5
        )

        # Set the circumference labels
        # np.linspace(0, 2*np.pi, 24, endpoint=False) = radians
        ax.set_xticks(radians)
        ax.set_xticklabels(range(24))

        ax.set_rlabel_position(190.5)
        # Make the labels go clockwise
        ax.set_theta_direction(-1)       

        # Place 0 at the top
        ax.set_theta_offset(np.pi/2.0)    

        del aux
        # plt.show()
        return fig, ax


def plot_roc_curve(FPR, TPR, random=True, fig=None, ax=None):
    
    with plt.style.context('default') as ctx:
        sns.set_context(ctx)
        sns.set_style('darkgrid', {'axes.facecolor': '0.9'})
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(5,5))

        ax.set_title("Receiver Operating Characteristic (ROC) Curve", fontsize=15)
        ax.set_xlim([-0.01, 1.01])
        ax.set_ylim([-0.01, 1.01])

        ax.set_xlabel('False Positive Rate', fontsize=15)
        ax.set_ylabel('True Positive Rate', fontsize=15)

        if random:
            ax.plot([0, 1], [0, 1],'r--',label="AUC ROC Random = 0.5")

        ROC_AUC = metrics.auc(FPR, TPR)    

        ax.plot(
            FPR, TPR, 
            color='blue', 
            label = 'AUC ROC Classifier = {0:0.3f}'.format(ROC_AUC)
        )

        ax.legend(loc = 'lower right')
        return fig, ax


def plot_pr_curve(precisions, recalls, AP=None, baseline=0.5, fig=None, ax=None):
    with plt.style.context('default') as ctx:
        sns.set_context(ctx)
        sns.set_style('darkgrid', {'axes.facecolor': '0.9'})
        # baseline=sum(true_labels)/len(true_labels)
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(5,5))

        ax.set_title("Precision-Recall (PR) Curve", fontsize=15)
        ax.set_xlim([-0.01, 1.01])
        ax.set_ylim([-0.01, 1.01])

        ax.set_xlabel('Recall (True Positive Rate)', fontsize=15)
        ax.set_ylabel('Precision', fontsize=15)

        ax.plot([0, 1], [baseline, baseline],'r--',label='AP Random = {0:0.3f}'.format(baseline))
        ax.step(
            recalls, 
            precisions, 
            color='blue', 
            label = 'AP Classifier = {0:0.3f}'.format(AP)
        )
        ax.legend(loc ='lower right')
        return fig, ax


def plot_confusion_matrix(cm, labels, cmap=plt.cm.Blues, fig=None, ax=None):
    # plt.style.use('classic')
    with plt.style.context('default'):
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(5,5))

        disp = metrics.ConfusionMatrixDisplay(
            cm, 
            display_labels=labels
        )

        disp = disp.plot(
            include_values=True,
            cmap=cmap,
            ax=ax

        )
        disp.ax_.set_title('Confusion Matrix', fontsize=17)
        disp.ax_.set_ylabel(disp.ax_.get_ylabel(), fontsize=15)
        disp.ax_.set_xlabel(disp.ax_.get_xlabel(), fontsize=15)
        return disp.figure_, disp.ax_