# requests and json are the dependencies
import requests
import json
from PIL import Image
from io import BytesIO 
import cv2
import numpy as np
class StreetViewer(object):
    def __init__(self, api_key, location, size="640x640",
                 folder_directory='./streetviews/', verbose=True):
        """
        This class handles a single API request to the Google Static Street View API
        api_key: obtain it from your Google Cloud Platform console
        location: the address string or a (lat, lng) tuple
        size: returned picture size. maximum is 640*640
        folder_directory: directory to save the returned objects from request
        verbose: whether to print the processing status of the request
        """
        # input params are saved as attributes for later reference
        self._key = api_key
        self.location = location
        self.size = size
        self.folder_directory = folder_directory
        # call parames are saved as internal params
        self._meta_params = dict(key=self._key,
                                location=self.location)
        self._pic_params = dict(key=self._key,
                               location=self.location,
                               size=self.size)
        self.verbose = verbose
    
    def get_meta(self):
        """
        Method to query the metadata of the address
        """
        # saving the metadata as json for later usage
        # "/"s are removed to avoid confusion on directory
        self.meta_path = "{}meta_{}.json".format(
            self.folder_directory, self.location.replace("/", ""))
        self._meta_response = requests.get(
            'https://maps.googleapis.com/maps/api/streetview/metadata?',
            params=self._meta_params)
        # turning the contents as meta_info attribute
        self.meta_info = self._meta_response.json()
        # meta_status attribute is used in get_pic method to avoid
        # query when no picture will be available
        self.meta_status = self.meta_info['status']
        if self._meta_response.ok:
            loc = self._meta_response.json()['location']
            lat = loc['lat']
            lng = loc['lng']
            if self.verbose:
                print(">>> Obtained Meta from StreetView API:")
                print(self.meta_info)
            return lat,lng
        else:
            print(">>> Failed to obtain Meta from StreetView API!!!")
        
        self._meta_response.close()
        return 0,0
    
    def get_pic(self):
        """
        Method to query the StreetView picture and save to local directory
        """
        # define path to save picture and headers
        self.pic_path = "{}pic_{}.jpg".format(
            self.folder_directory, self.location.replace("/", ""))
        self.header_path = "{}header_{}.json".format(
            self.folder_directory, self.location.replace("/", ""))
        # only when meta_status is OK will the code run to query picture (cost incurred)
        if self.meta_status == 'OK':
            if self.verbose:
                print(">>> Picture available, requesting now...")
            self._pic_response = requests.get(
                'https://maps.googleapis.com/maps/api/streetview?',
                params=self._pic_params)
            self.pic_header = dict(self._pic_response.headers)
            if self._pic_response.ok:
                # if self.verbose:
                #     print(f">>> Saving objects to {self.folder_directory}")
                # with open(self.pic_path, 'wb') as file:
                #     file.write(self._pic_response.content)
                # with open(self.header_path, 'w') as file:
                #     json.dump(self.pic_header, file)
                stream = BytesIO(self._pic_response.content)
                img = Image.open(stream)
                img = np.array(img)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                self._pic_response.close()
                if self.verbose:
                    print(">>> COMPLETE!")
                return img
        else:
            print(">>> Picture not available in StreetView, ABORTING!")
            return None
             
    def display_pic(self):
        """
        Method to display the downloaded street view picture if available
        """
        if self.meta_status == 'OK':
            plt.figure(figsize=(10, 10))
            img=mpimg.imread(self.pic_path)
            imgplot = plt.imshow(img)
            plt.show()
        else:
            print(">>> Picture not available in StreetView, ABORTING!")
            
            
if __name__ == "__main__":
    # test with GWU marvin center address
    api_key = '####'
    gwu_viewer = StreetViewer(api_key=api_key,
                            location='800 21st St NW, Washington, DC 20052')
    lat, lon = gwu_viewer.get_meta()
    im = gwu_viewer.get_pic()
    cv2.imshow("im",im)
    cv2.waitKey(0)
    #gwu_viewer.display_pic()