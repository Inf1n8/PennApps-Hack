# PennApps-Hack

## Inspiration
Recent mass shooting events are indicative of a rising, unfortunate trend in the United States. During a shooting, someone may be killed every 3 seconds on average, while it takes authorities an average of 10 minutes to arrive on a crime scene after a distress call. In addition, cameras and live closed circuit video monitoring are almost ubiquitous now, but are almost always used for post-crime analysis. Why not use them immediately? With the power of Google Cloud and other tools, we can use camera feed to immediately detect weapons real-time, identify a threat, send authorities a pinpointed location, and track the suspect - all in one fell swoop.

## What it does
At its core, our intelligent surveillance system takes in a live video feed and constantly watches for any sign of a gun or weapon. Once detected, the system immediately bounds the weapon, identifies the potential suspect with the weapon, and sends the authorities a snapshot of the scene and precise location information. In parallel, the suspect is matched against a database for any additional information that could be provided to the authorities.

## How we built it
The core of our project is distributed across the Google Cloud framework. A camera (most commonly a CCTV) presents a live feed to a model, which is constantly looking for anything that looks like a gun using GCP's Vision API. Once detected, we bound the gun and nearby people and identify the shooter through a distance calculation. The backend captures all of this information and sends this to check against a cloud-hosted database of people. Then, our frontend pulls from the identified suspect in the database and presents all necessary information to authorities in a concise dashboard which employs the Maps API. As soon as a gun is drawn, the authorities see the location on a map, the gun holder's current scene, and if available, his background and physical characteristics.

## Challenges we ran into
There are some careful nuances to the idea that we had to account for in our project. For one, few models are pre-trained on weapons, so we experimented with training our own model in addition to using the Vision API. Additionally, identifying the weapon holder is a difficult task - sometimes the gun is not necessarily closest to the person holding it. This is offset by the fact that we send a scene snapshot to the authorities, and most gun attacks happen from a distance. Testing is also difficult, considering we do not have access to guns to hold in front of a camera.

## Accomplishments that we're proud of
A clever geometry-based algorithm to predict the person holding the gun. Minimized latency when running several processes at once. Clean integration with a database integrating in real-time.

## What we learned
It's easy to say we're shooting for MVP, but we need to be careful about managing expectations for what features should be part of the MVP and what features are extraneous.

## What's next for HawkCC
As with all machine learning based products, we would train a fresh model on our specific use case. Given the raw amount of CCTV footage out there, this is not a difficult task, but simply a time-consuming one. This would improve accuracy in 2 main respects - cleaner identification of weapons from a slightly top-down view, and better tracking of individuals within the frame. SMS alert integration is another feature that we could easily plug into the surveillance system as well, and further compound the reaction improvement time.


## Link to Devpost: 

 https://devpost.com/software/hawkcc 

