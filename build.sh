#!/bin/bash

docker build \
    --secret id=HUGGING_TOKEN,src=.env \
    -t capstone .