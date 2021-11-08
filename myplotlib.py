import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
#import urllib.request
class plotlib:
    def __init__(self):
        self.df = pd.DataFrame()
        self.plot_paths = set()
        self.path_name = ''
    def __draw_corr_matrix(self):
        corr_mat = self.df.corr()
        f,ax = plt.subplots(figsize=(5*corr_mat.shape[0],5*corr_mat.shape[0]))
        ms = ax.matshow(corr_mat,cmap=plt.cm.Blues)
        ax.set_xticks(range(self.df.select_dtypes(['number']).shape[1]))
        ax.set_yticks(range(self.df.select_dtypes(['number']).shape[1]))
        ax.set_xticklabels(self.df.select_dtypes(['number']).columns,rotation=90,fontsize=18)
        ax.set_yticklabels(self.df.select_dtypes(['number']).columns,fontsize=18)
        for i in range(self.df.select_dtypes(['number']).shape[1]):
            for j in range(self.df.select_dtypes(['number']).shape[1]):
                c = round(corr_mat.iloc[i,j],2)
                ax.text(i, j, str(c), va='center', ha='center',color = 'red',fontsize=18)
        f.colorbar(ms).ax.tick_params(labelsize=18)
        ax.set_title('Correlation Matrix', fontsize=24);
        # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        #     print(self.df.corr())
        fname = self.path_name+'[corr_matrix][][].png'
        f.savefig(fname)
        #self.plot_paths.add(os.path.abspath(fname))
        plt.close('all')
        return os.path.abspath(fname)
    def __draw_scatter(self,col1 = '',col2=''):
        fname = ''
        if not (col1 or col2):
            sm = sns.pairplot(data = self.df,
                              kind = 'scatter',
                              diag_kind = 'hist',
                              vars = self.df.select_dtypes(['number']).columns,
                              hue=self.df.select_dtypes(['int']).columns[0])
            fname = self.path_name+'scatterplots/[scatter_matrix][][].png'
            plt.savefig(fname,dpi=300)
            #self.plot_paths.add(os.path.abspath(fname))
            return os.path.abspath(fname)
        elif not col2:
            f, ax = plt.subplots(figsize=(10, 10))
            sns.scatterplot(data = self.df,
                            x=range(self.df.select_dtypes(['number']).shape[0]),
                            y=col1,
                            ax = ax,
                            markers=True,
                            hue=self.df.select_dtypes(['int']).columns[0],
                            style = self.df.select_dtypes(['int']).columns[1],
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
                f, ax = plt.subplots(figsize=(10, 10))
                sns.scatterplot(data=self.df,
                                x=col1,
                                y=col2,
                                ax=ax,
                                markers=True,
                                hue=self.df.select_dtypes(['int']).columns[0],
                                style=self.df.select_dtypes(['int']).columns[1],
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
        plt.close('all')
        #print(col1, col2,fname)
        return os.path.abspath(fname)
    def __draw_boxplot(self,col,x=''):
        f, ax = plt.subplots(figsize=(10, 10))
        if not x:
            sns.boxplot(data=self.df[col], ax=ax)
        else:
            sns.boxplot(data = self.df,x = x,y = col,ax = ax,
                        hue = self.df.select_dtypes(['int']).columns[0])
        ax.set_title('Boxplot, column: '+ col, fontsize=24)
        ax.set_xlabel(x, fontsize=18, rotation=0, ha='center')
        ax.set_ylabel(col, fontsize=18, rotation=90, ha='center')
        fname = self.path_name + 'boxplots/[boxplot][' + x + '][' + col + '].png'
        f.savefig(fname)
        #self.plot_paths.add(os.path.abspath(fname))
        plt.close('all')
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
        plt.close('all')
        return os.path.abspath(fname)
    def draw_plots(self,data,kind = 'corr'):
        dataname = re.sub('.json','',re.sub('.*/','',data))
        self.path_name = 'plots/[' + dataname + ']'
        self.df = pd.read_json(data)
        cols = self.df.select_dtypes(['number']).columns
        col_cat = cols[0]
        self.cats = self.df[col_cat].unique()
        self.cats.sort()
        os.makedirs(self.path_name+'scatterplots/',exist_ok = True)
        os.makedirs(self.path_name + 'boxplots/',exist_ok = True)
        os.makedirs(self.path_name + 'histograms/',exist_ok = True)
        path_files = set()
        if kind=='corr':
            path_files.add(self.__draw_corr_matrix())
        else:
            for i in range(len(cols)):
                if kind=='scatter':
                    for j in range(len(cols)):
                        path_files.add(self.__draw_scatter(cols[i],cols[j]))
                elif kind=='boxplot':
                    path_files.add(self.__draw_boxplot(cols[i]))
                    path_files.add(self.__draw_boxplot(cols[i],col_cat))
                else:
                    path_files.add(self.__draw_displot(cols[i], col_cat))
            #plt.close('all')
        self.plot_paths = self.plot_paths.union(path_files)
        return path_files

if __name__=='__main__':
    json_link = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
    #urllib.request.urlretrieve(json_link,'json_data.json')
    #plotlib().draw_plots('json_data.json')
    newpl = plotlib()
    paths = newpl.draw_plots(json_link,'corr')
    print(paths,newpl.plot_paths)
    paths = newpl.draw_plots(json_link, 'displot')
    print(paths, newpl.plot_paths)