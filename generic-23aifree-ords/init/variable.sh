#!/bin/bash

#make sure you have .env file stored in opc user home directory
# you need to provide your an placeholder for relevant passwords, and ocids, etc.
#use the demo.env and adjust values
if [[ -f /home/opc/.env ]]; then
  source /home/opc/.env
fi

export public_ip=$(curl -s ifconfig.me)
if [[ ${#public_ip} -le 5 || ${public_ip} =~ '<html>' ]]; then
 export public_ip="127.0.0.1"
fi


export vncpwd=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/vncpwd)

if [[ ${#vncpwd} -ne 10 ]]; then
 export vncpwd="$vncpwdlocal"
fi


export dbconnection=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/dbconnection|tr -d ' ')

if [[ ${#dbconnection} -le 5 || ${dbconnection} =~ '<html>' ]]; then
  export dbconnection="$dbconnectionlocal"
fi

if [[ "$dbinst" == "free" ]]; then
  export dbinst="23ai"
fi


export mongodbapi=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/mongodbapi|tr -d ' ')

if [[ ${#mongodbapi} -le 5 || ${mongodbapi} =~ '<html>' ]]; then
 export mongodbapi="$mongodbapilocal"
fi


export graphurl=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/graphurl|tr -d ' ')

if [[ ${#graphurl} -le 5 || ${graphurl} =~ '<html>' ]]; then
 export graphurl="$graphurllocal"
fi


export dbpassword=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/dbpassword)

if [[ ${#dbpassword} -le 5 || ${dbpassword} =~ '<html>' ]]; then
 export dbpassword="$dbpasswordlocal"
fi

export pem_key=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/pem_key)

if [[ ${#pem_key} -le 5 || ${pem_key} =~ '<html>' ]]; then
 export pem_key="$pem_keylocal"
fi

export pem_key_fingerprint=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/pem_key_fingerprint)

if [[ ${#pem_key_fingerprint} -le 5 || ${pem_key_fingerprint} =~ '<html>' ]]; then
 export pem_key_fingerprint="$pem_key_fingerprintlocal"
fi

export user_ocid=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/user_ocid)

if [[ ${#user_ocid} -le 5 || ${user_ocid} =~ '<html>' ]]; then
 export user_ocid="$user_ocidlocal"
fi

export tenancy_ocid=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/tenancy_ocid)

if [[ ${#tenancy_ocid} -le 5 || ${tenancy_ocid} =~ '<html>' ]]; then
 export tenancy_ocid="$tenancy_ocidlocal"
fi

export region_identifier=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/region_identifier)

if [[ ${#region_identifier} -le 5 || ${region_identifier} =~ '<html>' ]]; then
 export region_identifier="$region_identifierlocal"
fi

export ai_endpoint_region=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/ai_endpoint_region)

if [[ ${#ai_endpoint_region} -le 5 || ${ai_endpoint_region} =~ '<html>' ]]; then
 export ai_endpoint_region="$ai_endpoint_regionlocal"
fi


export compartment_ocid=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/compartment_ocid)

if [[ ${#compartment_ocid} -le 5 || ${compartment_ocid} =~ '<html>' ]]; then
 export compartment_ocid="$compartment_ocidlocal"
fi

#workshopfiles must be a URL pointing to a zip file
export workshopfiles=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/workshopfiles)

if [[ ${#workshopfiles} -ne 10 ]]; then
 export workshopfiles="https://c4u04.objectstorage.us-ashburn-1.oci.customer-oci.com/p/EcTjWk2IuZPZeNnD_fYMcgUhdNDIDA6rt9gaFj_WZMiL7VvxPBNMY60837hu5hga/n/c4u04/b/livelabsfiles/o/labfiles/vec_chunk.zip"
fi

export endpoint="https://inference.generativeai.${ai_endpoint_region}.oci.oraclecloud.com"

if [[ ${#endpoint} -le 5 || "$endpoint" =~ ai_endpoint_region ]]; then
 export endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
fi

export adb_ocid=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/adb_ocid)

if [[ ${#adb_ocid} -le 5 || ${adb_ocid} =~ '<html>' ]]; then
 export adb_ocid="$adb_ocidlocal"
fi

export bucket_par=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/bucket_par)

if [[ ${#bucket_par} -le 5 || ${bucket_par} =~ '<html>' ]]; then
 export bucket_par="https://par.par.par"
fi

export ordsurl=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/ordsurl)

if [[ ${#ordsurl} -le 5 || ${ordsurl} =~ '<html>' ]]; then
 export ordsurl="$ordsurllocal"
fi

export dbname=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/dbname)

if [[ ${#dbname} -le 5 || ${dbname} =~ '<html>' ]]; then
 export dbname="$dbnamelocal"
fi

export bucket_name=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/bucket_name)

if [[ ${#bucket_name} -le 5 || ${bucket_name} =~ '<html>' ]]; then
 export bucket_name="bucket_name"
fi

export object_namespace=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/object_namespace)

if [[ ${#object_namespace} -le 5 || ${object_namespace} =~ '<html>' ]]; then
 export object_namespace="ocid567890"
fi

export baseurl=$(curl -s -H "Authorization: Bearer Oracle" -L http://169.254.169.254/opc/v2/instance/metadata/baseurl)

if [[ ${#baseurl} -le 5 || ${baseurl} =~ '<html>' ]]; then
 export baseurl="$baseurllocal"
fi
