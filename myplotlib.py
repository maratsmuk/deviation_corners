import pandas as pd
import matplotlib.pyplot as plt
import re
#import urllib.request
class plotlib:
    def __init__(self):
        pass
    def draw_plots(self,input_data):
        fname = input_data[:]
        fname = re.sub('.json','',re.sub('.*/','',input_data))
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
        plt.savefig('plots/[corr_matrix]'+fname+'.png')
        f2 = pd.plotting.scatter_matrix(df, alpha=0.2)
        plt.savefig('plots/[scatter_matrix]'+fname+'.png')


if __name__=='__main__':
    json_link = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
    #urllib.request.urlretrieve(json_link,'json_data.json')
    #plotlib().draw_plots('json_data.json')
    plotlib().draw_plots(json_link)
