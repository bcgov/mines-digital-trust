#!/usr/bin/env bash

#DL, BUILD, RUN, LOCAL HYPERLEDGER
git clone https://github.com/bcgov/von-network.git von-network
./von-network/manage build
./von-network/manage start

#GET LOCAL LEDGER GENESIS FILES AND START RESOLVER
curl --retry-connrefused --retry 5 --retry-delay 2 http://localhost:9000/genesis -o ./localhost_9000.txn

while [ $? -ne 0 ];
do
    sleep 3
    curl --retry-connrefused --retry 5 --retry-delay 2 http://localhost:9000/genesis -o resolver/localhost_9000.txn
done
docker-compose up -d driver-did-sov 

#START BB-PacMans
docker-compose up bpa1 bpa-agent1 bpa2 bpa-agent2