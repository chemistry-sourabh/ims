# Rest API

We have a basic set of API as of now. All of the services as of now are taking the arguments as parameters and return response.

BMI API assumes that you know the image which you are interested in. BMI has an driver which can communicate with Ceph(the file storage system that we are using for storing our images). Please make sure that you understand Ceph concepts before you play with the API. 

To have a clear understanding of the API, we wish to provide the following terminology:
* project - A project is the HaaS project that has been allocated to tenant.
* node - A node that is allocated to project by HaaS. This node should be present in HaaS.
* img - The name of image which will be used for provisioning.
* snap_name - The snapshot of the image from which you want to provision a node.
* network - The provisioning network created in HaaS.
* nic - The nic which should be used to connect the node to provisioning network
* channel - The vlan that should be used to connect the node to provisioning network

The convention that we are following for requests is:
* PUT - for resource creation like node creation 
* DELETE - for resource deletion for node deletion
* POST - for rest of operations

**The username and password for HaaS needs to be passed along using HTTP Basic Auth to each possible API call.**

Each possible API call has:
* an HTTP method and URL path
* Request body(which will always be form encoded parameters)
* A list of possible responses
* An example

---
###Provision:
Provision API is needed for provisioning a node from MOC cluster as of now. Provision operation internally calls a ceph clone operation. Ceph clone operation usually takes a snap_

Following is the call for API:

####Link:
http://BMI_SERVER:PORT/provision/

####Request Type:
PUT

####Request Body:
```json
{
 "project" : "<project_name>",
 "node" : "<node_name>" , 
 "img" : "<image_name>" ,
 "network" : "<network_name>" ,
 "channel" : "<channel in haas>" ,
 "nic" : "<nic to connect on>"
}
```

####Responses:
* 200. This means the provision call is successful.
* Internal 500 with some junk characters. This means the request body is not proper.
* 401. This means unauthorized access to ceph image or snapshot or image already exists in ceph.
* 403. This means a ceph connection problem.
* 409. Image busy exception.
* 444. You used a wrong request method like PUT instead of POST etc.
 
####Example:
Send a PUT Request with following body to http://<BMI_SERVER>:<PORT>/provision/

```json
{
 "project" : "bmi_infra",
 "node" : "cisco-2016" , 
 "img" : "hadoopMaster.img" ,  
 "network" : "provision-net" ,
 "channel" : "vlan/native",
 "nic" : "nic01"
}
```
**Make sure to use HTTP Basic Auth to pass HaaS Credentials**

This should return a 200 or other errors as explained above.

---
###Deprovision:

Following is the call for API:

####Link:
http://BMI_SERVER:PORT/deprovision/

####Request Type:
DELETE

####Request Body:
```json
{
 "project" : "<project_name>",
 "node" : "<node_name>" ,
 "network" : "<network_name>" ,
 "nic" : "<nic to connect on>"
}
```

####Responses:
* 200. This means the delete node call is successful.
* Internal 500 with some junk characters. This means the request body is not proper.
* 401. This means unauthorized access to ceph image or snapshot or image already exists in ceph.
* 403. This means a ceph connection problem.
* 409. Image busy exception.
* 405. Image has snapshots. (We need to delete them before we delete image).
* 404. Image not found exception.
* 444. You used a wrong request method like PUT instead of POST etc.

####Example:
Send a DELETE Request with following body to http://<BMI_SERVER>:<PORT>/deprovision/
```json
{
 "project" : "bmi_infra",
 "node" : "cisco-2016" ,
 "network" : "provision-net" ,
 "nic" : "nic01"
}
```

**Make sure to use HTTP Basic Auth to pass HaaS Credentials**

This should return a 200 or other errors as explained above.

---
###List Images:

Following is the call for API:

####Link:
http://BMI_SERVER:PORT/list_images/

####Request Type:
POST

####Request Body:
```json
{
 "project" : "<project_name>" 
}
```

####Respones:
* 200. This means list node call is successful and it returns list of images available in your project.
* Internal 500 with some junk characters. This means the request body is not proper.
* 401. This means unauthorized access to project.
* 403. This means a ceph connection problem.
* 444. You used a wrong request method like PUT instead of POST etc.

This returns either a list of images in response body along with 200 response or other exceptions. 

####Example:
Send a POST Request with following body to http://BMI_SERVER:PORT/list_images/
```json
{
 "project" : "bmi_infra"
}
```

**Make sure to use HTTP Basic Auth to pass HaaS Credentials**

The list of images which are in your project - if it is successful with a status code of 200.

---
###Create Snapshot:
Snapshot is feature which is available to preserve the state of your node. Using ceph as backend we can preserve the state of your node as a snapshot and use this snapshot for further cloning.

**The Node should be provisioned and powered down before calling this function**

Following is the call for API:

####Link:
http://BMI_SERVER:PORT/create_snapshot/

####Request Type:
PUT

####Request Body:
```json
{
 "project" : "<project_name>",
 "node" : "<node_name>" ,
 "snap_name" : "<snapshot_name>" 
}
```

####Response:
* 200. This means the create snapshot call is successful.
* Internal 500 with some junk characters. This means the request body is not proper.
* 401. This means unauthorized access to ceph image or snapshot or image already exists in ceph.
* 403. This means a ceph connection problem.
* 409. Image busy exception.
* 404. Image not found exception.
* 444. You used a wrong request method like PUT instead of POST etc.

####Example:
Send a PUT Request with following body to http://BMI_SERVER:PORT/create_snapshot/
```json
{
"project":"bmi_infra", 
"node": "cisco-2016", 
"snap_name":"test_snap2016" 
}
```

**Make sure to use HTTP Basic Auth to pass HaaS Credentials**

This should return a 200 or other errors as explained above.

---
###List Snapshots:
This returns all the snapshots associated with a project

Following is the call for API:

####Link:
http://BMI_SERVER:PORT/list_snapshots/

####Request Type:
POST

####Request Body:
```json
{
 "project" : "<project_name>"
}
```

####Response:
* 200. This means the list snapshot call is successful.
* Internal 500 with some junk characters. This means the request body is not proper.
* 401. This means unauthorized access to ceph image or snapshot or image already exists in ceph.
* 403. This means a ceph connection problem.
* 409. Image busy exception.
* 404. Image not found exception.
* 444. You used a wrong request method like PUT instead of POST etc.

####Example:
Send a POST Request with following body to http://BMI_SERVER:PORT/list_snapshots/
```json
{
 "project" : "bmi_infra"
}
```

**Make sure to use HTTP Basic Auth to pass HaaS Credentials**

The list of snapshots for given image which is in your project - if it is successful with a status code of 200.

---
###Remove Image:
Following is the call for API:

####Link:
http://BMI_SERVER:PORT/remove_image/

####Request Type:
DELETE

####Request Body:
```json
{
 "project" : "<project_name>" ,
 "img" : "<img_name>"
}
```

####Response:
* 200. This means the remove snapshot call is successful.
* Internal 500 with some junk characters. This means the request body is not proper.
* 401. This means unauthorized access to ceph image or snapshot or image already exists in ceph.
* 403. This means a ceph connection problem.
* 409. Image busy exception.
* 404. Image not found exception.
* 444. You used a wrong request method like PUT instead of POST etc.

####Example:
Send a DELETE Request with following body to http://BMI_SERVER:PORT/remove_image/
```json
{
 "project" : "bmi_infra",
 "img" : "test.img"
}
```

**Make sure to use HTTP Basic Auth to pass HaaS Credentials**

If the call is successful, we will get a 200 as status code and test.img should be removed.

---