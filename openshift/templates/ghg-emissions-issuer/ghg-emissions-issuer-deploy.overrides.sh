#!/bin/bash
_includeFile=$(type -p overrides.inc)
if [ ! -z ${_includeFile} ]; then
  . ${_includeFile}
else
  _red='\033[0;31m'; _yellow='\033[1;33m'; _nc='\033[0m'; echo -e \\n"${_red}overrides.inc could not be found on the path.${_nc}\n${_yellow}Please ensure the openshift-developer-tools are installed on and registered on your path.${_nc}\n${_yellow}https://github.com/BCDevOps/openshift-developer-tools${_nc}"; exit 1;
fi

# ======================================================
# Special Deployment Parameters needed for Deployment
# ------------------------------------------------------
# The results need to be encoded as OpenShift template
# parameters for use with oc process.
# ======================================================

if createOperation; then
  # readParameter "CR_ADMIN_API_KEY - Please provide the key for the credential registry admin api.\nThe default is an empty string:" "CR_ADMIN_API_KEY" "" "false"
  readParameter "ISSUER_SECRET_KEY - Please provide the key for the issuers's protected API.  If left blank, a 32 character long base64 encoded value will be randomly generated using openssl:" "ISSUER_SECRET_KEY" $(generateKey 32) "false"
else
  # Secrets are removed from the configurations during update operations ...
  printStatusMsg "Update operation detected ...\nSkipping the prompts for the CR_* secrets ...\n"
  # Prompted
  # writeParameter "CR_ADMIN_API_KEY" "generation_skipped" "false"
  writeParameter "ISSUER_SECRET_KEY" "generation_skipped" "false"

fi

SPECIALDEPLOYPARMS="--param-file=${_overrideParamFile}"
echo ${SPECIALDEPLOYPARMS}
