#!/bin/bash
wget https://adwc4pm.objectstorage.us-ashburn-1.oci.customer-oci.com/p/VBRD9P8ZFWkKvnfhrWxkpPe8K03-JIoM5h_8EJyJcpE80c108fuUjg7R5L5O7mMZ/n/adwc4pm/b/OML-Resources/o/all_MiniLM_L12_v2_augmented.zip

unzip all_MiniLM_L12_v2_augmented.zip

sudo docker cp all_MiniLM_L12_v2.onnx 23ai:/tmp/.

rm all_MiniLM_L12_v2*

rm READ*
