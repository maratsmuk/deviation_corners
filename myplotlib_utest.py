import unittest
import pandas as pd
import myplotlib
import os
import matplotlib.pyplot as plt
import matplotlib.image as img
pl = myplotlib.plotlib
def check_img(f):
    try:
        my_img = plt.imread(f)
        fig, ax = plt.subplots()
        ax.imshow(my_img)
        ax.axis('off')
        return True
    except:
        #print(f)
        return False
class MyTestCase(unittest.TestCase):
    def test_generated_files(self):
        json_link = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
        df = pd.read_json(json_link)
        df = df[df.columns[:4]]
        os.makedirs('utest/', exist_ok=True)
        json_name = 'utest/deviation_shortened.json'
        df.to_json(json_name)
        newpl = pl()
        paths_corr = newpl.draw_plots(json_name, 'corr')
        paths_scatter = newpl.draw_plots(json_name, 'scatter')
        paths_box = newpl.draw_plots(json_name, 'boxplot')
        paths_his = newpl.draw_plots(json_name, 'hisplot')
        for f in list(newpl.plot_paths):
            self.assertEqual(True,check_img(f),'Error: images are not available')
        self.assertEqual(len(list(paths_corr))+len(list(paths_box))+len(list(paths_scatter))+len(list(paths_his)), len(list(newpl.plot_paths)),
                         'Error: lengths of lists do not coincide')
        self.assertEqual(1+9+6+3,
                         len(list(newpl.plot_paths)),'Error: not all paths have been generated')
if __name__ == '__main__':
    unittest.main()
