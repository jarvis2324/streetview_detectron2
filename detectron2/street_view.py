# using Python
import requests
meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
pic_base = 'https://maps.googleapis.com/maps/api/streetview?'
api_key = '####'
# using my graduate school almar mater, GWU, as an example
#location = 'Mandi King,Gachibowli, Hyderabad, India'
locations = ["DLF Road,Gachibowli, Hyderabad", "Mandi King, Gacchibowli, Hyderabad" , "Tenet Diagnostics, Gachibowli, Hyderabad"]
for location in locations:
    # define the params for the metadata reques
    meta_params = {'key': api_key,
                'location': location}
    # define the params for the picture request
    pic_params = {'key': api_key,
                'location': location,
                'size': "640x640",
                'radius' : 1000}
    print(pic_params)
    # obtain the metadata of the request (this is free)
    meta_response = requests.get(meta_base, params=meta_params)

    print(meta_response.json())
    #print(meta_response.json()['location'])
    if meta_response.json()['status'] == 'OK':
        pic_response = requests.get(pic_base, params=pic_params)

        for key, value in pic_response.headers.items():
            print(f"{key}: {value}")
            
        print(pic_response.ok)

        with open('test.jpg', 'wb') as file:
            file.write(pic_response.content)
        # remember to close the response connection to the API
        pic_response.close()

        # using matpltolib to display the image
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        plt.figure(figsize=(10, 10))
        img=mpimg.imread('test.jpg')
        imgplot = plt.imshow(img)
        plt.show()