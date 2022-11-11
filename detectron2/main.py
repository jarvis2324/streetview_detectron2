from detectron2_run import pred
from street_view_class import StreetViewer

api_key = '####'
gwu_viewer = StreetViewer(api_key=api_key,
                        location='800 21st St NW, Washington, DC 20052')
lat, lon = gwu_viewer.get_meta()
im = gwu_viewer.get_pic()
df = pred(im,lat,lon)
print(df)
df.to_csv('./file.csv')
