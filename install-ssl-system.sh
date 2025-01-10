#!/usr/bin/env bash

#https://github.com/micnigh/linux-workstation-bootstrap

apt-get -y install libnss3-tools libpcsclite1 pcscd pcsc-tools curl

rm -rf /usr/share/ca-certificates/dod
rm -rf /usr/local/share/ca-certificates/dod

TEMP_DIR=$(mktemp -d) && \
wget --no-check-certificate http://apt.cs.usna.edu/ssl/system-certs-5.6-pa.tgz -P $TEMP_DIR && \
tar -C $TEMP_DIR -xpf $TEMP_DIR/system-certs-5.6-pa.tgz && \
mkdir -p /usr/local/share/ca-certificates/dod/ && \
cp $TEMP_DIR/*.crt /usr/local/share/ca-certificates/dod/ && \
rm -rf $TEMP_DIR && \
update-ca-certificates -f