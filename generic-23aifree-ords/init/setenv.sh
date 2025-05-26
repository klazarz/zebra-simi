#! /bin/bash


source /home/opc/compose2cloud/init/variable.sh

mkdir -p /home/opc/compose2cloud/composescript/envvar/

echo $vncpwd | tee /home/opc/compose2cloud/composescript/envvar/.vncpwd > /dev/null
echo vncpwd=$(cat /home/opc/compose2cloud/composescript/envvar/.vncpwd) > /home/opc/compose2cloud/composescript/envvar/.vncpwd.env


# .env for container build
echo -e "PEM_KEY=\"${pem_key}\"" > /home/opc/compose2cloud/composescript/envvar/.env
echo "USERNAME=admin" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "DBPASSWORD=${dbpassword}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "ORACLE_PWD=${dbpassword}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "DBCONNECTION=${dbconnection}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "MONGODBAPI=${mongodbapi}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "GRAPHURL=${graphurl}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "PUBLIC_IP=${public_ip}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "COMPARTMENT_OCID=${compartment_ocid}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "ENDPOINT=${endpoint}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "dbname=${dbname}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "ORDSURL=${ordsurl}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "SERVICE_NAME=${dbname}_high" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "BUCKET_PAR=${bucket_par}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "BUCKET_NAME=${bucket_name}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "OBJECT_NAMESPACE=${object_namespace}" >> /home/opc/compose2cloud/composescript/envvar/.env
echo "BASEURL=${baseurl}" >> /home/opc/compose2cloud/composescript/envvar/.env


cp /home/opc/compose2cloud/composescript/envvar/.env /home/opc/compose2cloud/composescript/app/simidemo/.

mkdir -p /home/opc/compose2cloud/composescript/envvar/.jupyter

cp -r /home/opc/compose2cloud/composescript/jl_config/* /home/opc/compose2cloud/composescript/envvar/.jupyter/.

mkdir -p /home/opc/compose2cloud/composescript/envvar/.local/share/code-server/User/
cp -r /home/opc/compose2cloud/composescript/vscode-config/* /home/opc/compose2cloud/composescript/envvar/.local/share/code-server/User/. 


# custom scripts that should be called after this

#load stuff into JupterLab
bash /home/opc/compose2cloud/init/prepide.sh