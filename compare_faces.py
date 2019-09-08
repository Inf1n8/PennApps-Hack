import boto3
import cv2
import numpy as np
import os
import json

path = '/home/vikrame/Desktop/images/'
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
    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) 
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        print('Here are the other attributes:')
        print(json.dumps(faceDetail, indent=4, sort_keys=True))


    imageTarget.close()  

    print(ob)
    

