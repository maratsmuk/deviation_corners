import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
import numpy as np
from numpy import interp
#import urllib.request
class plotlib:
    def __init__(self):
        self.df = pd.DataFrame()
        self.plot_paths = set()
        self.path_name = ''
    def clear(self):
        self.__init__()
    def __draw_roc(self):
        y_true = label_binarize(self.df[['gt_corners']], classes=self.cats)
        y_pr = label_binarize(self.df[['rb_corners']], classes=self.cats)
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        n_classes = len(self.cats)
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_true[:, i], y_pr[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
        mean_tpr = np.zeros_like(all_fpr)
        for i in range(n_classes):
            mean_tpr += interp(all_fpr, fpr[i], tpr[i])
        mean_tpr /= n_classes
        fpr["macro"] = all_fpr
        tpr["macro"] = mean_tpr
        roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
        fpr["micro"], tpr["micro"], _ = roc_curve(y_true.ravel(), y_pr.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
        f = plt.figure(figsize=(10,10))
        ax = f.add_subplot(111)
        ax.plot(fpr["micro"],
                tpr["micro"],
                label="micro-average ROC curve (area = {0:0.2f})".format(roc_auc["micro"]),
                linestyle=":",
                linewidth=4)
        ax.plot(fpr["macro"],
                tpr["macro"],
                label="macro-average ROC curve (area = {0:0.2f})".format(roc_auc["macro"]),
                linestyle=":",
                linewidth=4)
        for i in range(n_classes):
            ax.plot(fpr[i],
                    tpr[i],
                    lw=2,
                    label="ROC curve of class ``{0} corners'' (area = {1:0.2f})".format(self.cats[i],roc_auc[i]))
        ax.plot([0, 1], [0, 1], color="black", lw=2, linestyle="--")
        ax.set_xlim([0.0,1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel("False Positive Rate",fontsize = 18)
        ax.set_ylabel("True Positive Rate",fontsize = 18)
        ax.set_title("Multiclass receiver operating characteristic",fontsize = 24)
        ax.legend(loc="lower right")
        fname = self.path_name + '[roc][][].png'
        f.savefig(fname)
        #plt.show()
        plt.close(f)
        return os.path.abspath(fname)

    def __draw_matrix(self,type):
        # f,ax = plt.subplots(figsize=(5*corr_mat.shape[0],5*corr_mat.shape[0]))
        if type=='corr':
            mat = self.df.corr()
            fname = self.path_name + '[corr_matrix][][].png'
            title = 'Correlation Matrix'
            figsize = (30, 30)
            xlabel = 'Columns'
            ylabel = 'Columns'
        elif type=='conf':
            mat = pd.DataFrame(confusion_matrix(self.df['gt_corners'], self.df['rb_corners']),
                                    columns=self.df['gt_corners'].unique())
            mat['corners'] = self.df['gt_corners'].unique()
            mat.set_index('corners', inplace=True)
            fname = self.path_name + '[confusion_matrix][][].png'
            title = 'Confusion Matrix'
            figsize = (10,10)
            xlabel = 'Actual values'
            ylabel = 'Predicted values'
        f = plt.figure(figsize=figsize)
        ax = f.add_subplot(111)
        ms = ax.matshow(mat, cmap=plt.cm.Blues)
        ax.set_xticks(range(mat.shape[0]))
        ax.set_yticks(range(mat.shape[1]))
        ax.set_xticklabels(mat.columns, rotation=45, fontsize=18)
        ax.set_yticklabels(mat.columns, fontsize=18)
        ax.set_xlabel(xlabel,fontsize = 18)
        ax.set_ylabel(ylabel, fontsize=18)
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                c = round(mat.iloc[i, j], 2)
                ax.text(i, j, str(c), va='center', ha='center', color='red', fontsize=18)
        f.colorbar(ms).ax.tick_params(labelsize=18)
        ax.set_title(title, fontsize=24);
        # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        #     print(self.df.corr())
        f.savefig(fname)
        # self.plot_paths.add(os.path.abspath(fname))
        plt.close(f)
        return os.path.abspath(fname)
    def __draw_corr_matrix(self):
        return self.__draw_matrix('corr')
    def __draw_conf_matrix(self):
        return self.__draw_matrix('conf')
    def __draw_scatter(self,col1 = '',col2=''):
        fname = ''
        if not (col1 or col2):
            sm = sns.pairplot(data = self.df,
                              kind = 'scatter',
                              diag_kind = 'hist',
                              vars = self.df.select_dtypes(['number']).columns,
                              hue=self.df.select_dtypes(['number']).columns[0])
            fname = self.path_name+'scatterplots/[scatter_matrix][][].png'
            plt.savefig(fname,dpi=300)
            #self.plot_paths.add(os.path.abspath(fname))
            return os.path.abspath(fname)
        elif not col2:
            #f, ax = plt.subplots(figsize=(10, 10))
            f = plt.figure(figsize=(10,10))
            ax = f.add_subplot(111)
            sns.scatterplot(data = self.df,
                            x=range(self.df.select_dtypes(['number']).shape[0]),
                            y=col1,
                            ax = ax,
                            markers=True,
                            hue=self.df.select_dtypes(['number']).columns[0],
                            style = self.df.select_dtypes(['number']).columns[1],
                            palette = plt.cm.brg)
            if 'int' in str(self.df[col1].dtype):
                ax.set_yticks(self.df[col1].unique())
            ax.set_ylabel(ax.get_ylabel(), fontsize=18, rotation=90, ha='center')
            ax.set_title('Scatter plot, column: '+col1, fontsize=24);
            fname = self.path_name + 'scatterplots/[scatter]['+col1+'][].png'
            f.savefig(fname)
            # self.plot_paths.add(os.path.abspath(fname))
        else:
            if col1==col2:
                return self.__draw_scatter(col1)
            else:
                #f, ax = plt.subplots(figsize=(10, 10))
                f = plt.figure(figsize=(10,10))
                ax = f.add_subplot(111)
                sns.scatterplot(data=self.df,
                                x=col1,
                                y=col2,
                                ax=ax,
                                markers=True,
                                hue=self.df.select_dtypes(['number']).columns[0],
                                style=self.df.select_dtypes(['number']).columns[1],
                                palette=plt.cm.brg)
                if 'int' in str(self.df[col1].dtype):
                    ax.set_xticks(self.df[col1].unique())
                if 'int' in str(self.df[col2].dtype):
                    ax.set_yticks(self.df[col2].unique())
                ax.set_xlabel(ax.get_xlabel(), fontsize=18, rotation=0, ha='center')
                ax.set_ylabel(ax.get_ylabel(), fontsize=18, rotation=90, ha='center')
                ax.set_title('Scatter plot, columns: ' + col1 + ' vs ' + col2, fontsize=24);
                fname = self.path_name + 'scatterplots/[scatter][' + col1 + ']['+col2+'].png'
                f.savefig(fname)
                # self.plot_paths.add(os.path.abspath(fname))
        #f.savefig(fname)
        plt.close(f)
        return os.path.abspath(fname)
    def __draw_boxplot(self,col,x=''):
        f = plt.figure(figsize=(10,10))
        ax = f.add_subplot(111)
        if not x:
            sns.boxplot(data=self.df[col], ax=ax)
        else:
            sns.boxplot(data = self.df,x = x,y = col,ax = ax,
                        hue = self.df.select_dtypes(['number']).columns[0])
        ax.set_title('Boxplot, column: '+ col, fontsize=24)
        ax.set_xlabel(x, fontsize=18, rotation=0, ha='center')
        ax.set_ylabel(col, fontsize=18, rotation=90, ha='center')
        fname = self.path_name + 'boxplots/[boxplot][' + x + '][' + col + '].png'
        f.savefig(fname)
        #self.plot_paths.add(os.path.abspath(fname))
        plt.close(f)
        return os.path.abspath(fname)
    def __draw_displot(self,col,col_cat):
        f, axs = plt.subplots(1, len(self.cats), figsize=(10*len(self.cats), 10))
        plt.suptitle('Histograms', size=24)
        for i in range(len(self.cats)):
            self.df[self.df[col_cat]==self.cats[i]][col].plot(kind = 'hist',ax = axs[i])
            axs[i].set_xlabel(col,fontsize = 18)
            axs[i].set_ylabel('frequency', fontsize=18)
            axs[i].set_title(col_cat +' = '+ str(self.cats[i]),fontsize = 22)
        fname = self.path_name + 'histograms/[hisplot][' + col_cat + '][' + col + '].png'
        f.savefig(fname)
        #self.plot_paths.add(os.path.abspath(fname))
        plt.close(f)
        return os.path.abspath(fname)
    def __draw_hisplot(self,col1,col2):
        name_target = col1[3:] if len(col1)>3 else 'Target'
        #f1, ax1 = plt.subplots(figsize=(10, 10))
        f1 = plt.figure(figsize=(10, 10))
        ax1 = f1.add_subplot(111)
        sns.histplot(data=self.df[[col1,col2]],multiple="dodge", discrete = True,ax = ax1)
        ax1.set_xticks(self.cats)
        ax1.set_xlabel(name_target,fontsize = 18)
        ax1.set_ylabel('Frequency', fontsize=18)
        ax1.set_title('Histogram of the target variable',fontsize = 22)
        #f2, ax2 = plt.subplots(figsize=(10, 10))
        f2 = plt.figure(figsize=(10, 10))
        ax2 = f2.add_subplot(111)
        sns.histplot(data=self.df[col1]-self.df[col2], multiple="dodge",discrete = True, ax=ax2)
        ax2.set_xlabel('Error = gt_target - pr_target', fontsize=18)
        ax2.set_ylabel('Frequency', fontsize=18)
        ax2.set_title('Histogram of the error', fontsize=22)
        fname1 = self.path_name + '[hisplot][' + col1 + '][' + col2 + '].png'
        f1.savefig(fname1)
        fname2 = self.path_name + '[hisplot_error][' + col1 + '][' + col2 + '].png'
        f2.savefig(fname2)
        # self.plot_paths.add(os.path.abspath(fname))
        plt.close(f1)
        plt.close(f2)
        return os.path.abspath(fname1),os.path.abspath(fname2)
    def draw_plots(self,data,kind = 'corr'):
        dataname = re.sub('.json','',re.sub('.*/','',data))
        self.path_name = 'plots/[' + dataname + ']'
        self.df = pd.read_json(data)
        cols = self.df.select_dtypes(['number']).columns
        #self.df[cols[1]] = self.df[cols[0]]+self.df[cols[0]]
        col_cat = cols[0]
        self.cats = self.df[col_cat].unique()
        self.cats.sort()
        os.makedirs(self.path_name+'scatterplots/',exist_ok = True)
        os.makedirs(self.path_name + 'boxplots/',exist_ok = True)
        os.makedirs(self.path_name + 'histograms/',exist_ok = True)
        path_files = set()
        if kind=='corr':
            path_files.add(self.__draw_corr_matrix())
        elif kind=='conf':
            path_files.add(self.__draw_conf_matrix())
        elif kind=='hist':
            p1,p2 = self.__draw_hisplot(cols[0],cols[1])
            path_files.add(p1)
            path_files.add(p2)
        elif kind=='roc':
            path_files.add(self.__draw_roc())
        else:
            for i in range(len(cols)):
                if kind=='scatter':
                    for j in range(len(cols)):
                        path_files.add(self.__draw_scatter(cols[i],cols[j]))
                elif kind=='boxplot':
                    if cols[i]!=col_cat:
                        path_files.add(self.__draw_boxplot(cols[i]))
                        path_files.add(self.__draw_boxplot(cols[i],col_cat))
                else:
                    path_files.add(self.__draw_displot(cols[i], col_cat))
        self.plot_paths = self.plot_paths.union(path_files)
        self.cats = None
        return path_files

if __name__=='__main__':
    json_name= 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
    #urllib.request.urlretrieve(json_link,'json_data.json')
    #plotlib().draw_plots('json_data.json')
    newpl = plotlib()
    #newpl.draw_plots(json_link,'corr')
    #paths_corr = newpl.draw_plots(json_name, 'corr')
    #paths_conf = newpl.draw_plots(json_name, 'conf')
    paths_roc = newpl.draw_plots(json_name, 'roc')
    #paths_hist = newpl.draw_plots(json_name, 'hist')
    #paths_scatter = newpl.draw_plots(json_name, 'scatter')
    #paths_box = newpl.draw_plots(json_name, 'boxplot')
    #paths_his_all = newpl.draw_plots(json_name, 'hisplot')
    #print(newpl.df.head(), newpl.path_name, newpl.plot_paths)
    newpl.clear()