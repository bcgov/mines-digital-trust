#!/bin/bash
# Copyright (c) 2020 - for information on the respective copyright owner
# see the NOTICE file and/or the repository at
# https://github.com/hyperledger-labs/organizational-agent
#
# SPDX-License-Identifier: Apache-2.0


# Check the system the script is running on
ARCHITECTURE="$(uname -s)"
if [[ ${ARCHITECTURE} == "Linux"* ]]; then
    ARCHITECTURE="Linux"
elif [[ ${ARCHITECTURE} == "Darwin"* ]]; then
    ARCHITECTURE="Mac"
fi

if [ "$ARCHITECTURE" != "Linux" ] && [ "$ARCHITECTURE" != "Mac" ]; then
    echo "No Linux or Mac OSX detected. You might need to do some steps manually."
fi

if [ ! -x "$(which curl)" ] ; then
    echo "Couldn't find curl. Please make sure that curl is installed."
    exit 1
fi

SRC_FILE=${SRC_FILE:-".env-example"}
DEST_FILE=${DEST_FILE:-".env"}
# Set URL
URL=${LEDGER_URL:-https://indy-test.bosch-digital.de}

# Set random alias
ALIAS=BPA-$(cat /dev/urandom | env LC_CTYPE=C tr -dc 'a-zA-Z0-9' | fold -w 4 | head -n 1)
# Generate random seed
SEED=$(cat /dev/urandom | env LC_CTYPE=C tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

PAYLOAD='{"alias":"'"$ALIAS"'","seed":"'"$SEED"'","role":"ENDORSER"}'

# Register DID
if curl --fail -s -d $PAYLOAD  -H "Content-Type: application/json" -X POST ${URL}/register; then
    # Registration (probably) successfull
    echo ""
    echo ""Registration on $URL successful""
    echo ""Setting ACAPY_SEED in $DEST_FILE file""
    if [ ! -f $DEST_FILE ]; then
        echo ""$DEST_FILE does not exist""
        echo ""Creating $DEST_FILE from $SRC_FILE""
        cp $SRC_FILE $DEST_FILE
    fi
    # sed on Mac and Linux work differently
    if [ "$ARCHITECTURE" = "Mac" ]; then
        sed -i'.bak' '/ACAPY_SEED=/c\ACAPY_SEED='"${SEED}"'' $DEST_FILE
    else
         sed -i '/ACAPY_SEED=/c\
        ACAPY_SEED='"${SEED}"'
        ' $DEST_FILE
    fi

else
    # Something went wrong
    echo ""
    echo Something went wrong
fi;
