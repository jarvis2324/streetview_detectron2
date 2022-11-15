from detectron2_run import pred
from street_view_class import StreetViewer
import pandas as pd
api_key = '####'
df = df = pd.DataFrame(columns = ['Class', 'Lat', 'Long'])
locations = ["DLF Road,Gachibowli, Hyderabad", "Mandi King, Gacchibowli, Hyderabad" , "Tenet Diagnostics, Gachibowli, Hyderabad"]
for location in locations:
    gwu_viewer = StreetViewer(api_key=api_key,
                            location=location)
    lat, lon = gwu_viewer.get_meta()
    im = gwu_viewer.get_pic()
    df_temp = pred(im,lat,lon)
    print("df_temp",df_temp)
    # if df.empty:
    #     df = df_temp
    # else:
    #     print("Else")
    df = df.append(df_temp,ignore_index=True)
    print("F",df)
df.to_csv('./file.csv')
