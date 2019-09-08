import boto3
import cv2
import numpy as np
import os
import json

path = '/home/vikrame/Desktop/images/'


from firebase import Firebase

config = {
  "apiKey": "AIzaSyBe2EmNpzsL4YKfHbRk2fTwbFFb5sic4D4",
  "authDomain": "cchawk-23c66.firebaseapp.com",
  "databaseURL": "https://cchawk-23c66.firebaseio.com/",
  "storageBucket": ""
}

firebase = Firebase(config)

ids = {
    "pranav": "1",
    "Vashisth" :"2" , 
    "Saravanan": "3",
    "Vikram" : "4"
} 

# if __name__ == "__main__":
def find(targetFile):
    client=boto3.client('rekognition')

    img = cv2.imread(targetFile)
    (h,w, c) = img.shape
    print(h,w,c)

    imageTarget=open(targetFile,'rb')
    targetImage = imageTarget.read()

    ob = {'name':'','conf':0.0}

    for i in os.listdir(path):
        sourceFile=os.path.join(path,i)
        imageSource=open(sourceFile,'rb')

        response=client.compare_faces(SimilarityThreshold=70,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': targetImage})

        print(response)
        
        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            similarity = str(faceMatch['Similarity'])
            print('The face at ' +
                str(position['Left']) + ' ' +
                str(position['Top']) +
                ' matches with ' + similarity + '% confidence')
            if(float(ob['conf']) < float("{:.2f}".format(float(similarity)))):
                ob['name'] = i[:-4]
                ob['conf'] = similarity

            # cv2.rectangle(img, (int(position['Left']*w), int(position['Top']*h) ), (int((position['Left']+position['Width'])*w), int((position['Top']+position['Height'])*h)), (255,0,0), 2)
            # cv2.imwrite("my.png",img)

            # cv2.imshow("lalala", img)
            # k = cv2.waitKey(0) 

        

        imageSource.close()
    response = client.detect_faces(Image={'Bytes': targetImage},Attributes=['ALL'])

    print('Detected faces for ' + targetFile) 
    print(type(response)) 

    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) 
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        print('Here are the other attributes:')

        keyss = json.dumps(faceDetail, indent=4, sort_keys=True)
        print(keyss)
        
        Beard = faceDetail["Beard"]["Value"]
        Eye_glasses = faceDetail["Eyeglasses"]["Value"]
        age_low = str(faceDetail['AgeRange']['Low']) 
        age_high = str((faceDetail['AgeRange']['High']))
        age = f'{age_low}-{age_high}'
        print(Beard, Eye_glasses, age)

        db = firebase.database()

        db.child("Display")
        db.child("Display").update({"age_range":age})
        # loaded =json.load(keyss)
        # print(loaded)
    imageTarget.close()  

    # print(response["AgeRange"])
    
    # print(beard, glasses)

    print(ob)
    

find('end.jpg')

