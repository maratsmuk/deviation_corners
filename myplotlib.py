import pandas as pd
import matplotlib.pyplot as plt
import re
import os
#import urllib.request
class plotlib:
    def __init__(self):
        self.plot_paths = set()
    def draw_plots(self,input_data):
        dataname = re.sub('.json','',re.sub('.*/','',input_data))
        df = pd.read_json(input_data)
        print(df.head())
        print(df.shape)
        print(df.info())
        print(df['gt_corners'].unique())
        print(df['rb_corners'].unique())
        corr = df.corr()
        f = plt.figure(figsize=(19, 15))
        plt.matshow(df.corr(), fignum=f.number)
        plt.xticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=14,
                   rotation=45)
        plt.yticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=14)
        cb = plt.colorbar()
        cb.ax.tick_params(labelsize=14)
        plt.title('Correlation Matrix', fontsize=16);
        #plt.show()
        fname = 'plots/['+dataname+']'+'[corr_matrix][][].png'
        plt.savefig(fname)
        self.plot_paths.add(os.path.abspath(fname))
        f2 = plt.figure(figsize=(19, 15))
        pd.plotting.scatter_matrix(df, alpha=0.2)
        fname = 'plots/['+dataname+']'+'[scatter_matrix][][].png'
        plt.savefig(fname,dpi=300)
        self.plot_paths.add(os.path.abspath(fname))
        cols = df.select_dtypes(['float']).columns
        #print(df[[cols[0]]])
        plt.close('all')
        for i_col in range(0,len(cols)-1):
            for j_col in range(i_col+1,len(cols)):
                f3 = plt.figure(figsize=(19, 15))
                df.plot(kind= 'scatter',x = cols[i_col],y=cols[j_col])
                fname = 'plots/['+dataname+']'+'[scatter]['+cols[i_col]+']['+cols[j_col]+'].png'
                plt.savefig(fname)
                self.plot_paths.add(os.path.abspath(fname))
            plt.close('all')
            for y_cat_col in df.select_dtypes(['int']).columns:
                f4 = plt.figure(figsize=(19, 15))
                df.plot(kind='scatter', x=cols[i_col], y=y_cat_col)
                fname = 'plots/['+dataname+']'+'[scatter]['+cols[i_col]+']['+y_cat_col+'].png'
                plt.savefig(fname)
                self.plot_paths.add(os.path.abspath(fname))
                plt.close(f4)
        #plt.show()
        plt.close('all')
        return self.plot_paths

if __name__=='__main__':
    json_link = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
    #urllib.request.urlretrieve(json_link,'json_data.json')
    #plotlib().draw_plots('json_data.json')
    newpl = plotlib()
    newpl.draw_plots(json_link)
    print(newpl.plot_paths)
