import pandas as pd
import matplotlib.pyplot as plt
from src.util.config_loader import Config

def upload_plot():    
    data = {'year': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
            'unemployment_rate': [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
        }        
    df = pd.DataFrame(data)

    f = plt.figure()
    plt.plot(df['year'], df['unemployment_rate'], color='red', marker='o')

    file_path = Config.value('root_folder')+Config.value('folderpath')+Config.value('filepath')['pdf']
    print(file_path)
    f.savefig(file_path)