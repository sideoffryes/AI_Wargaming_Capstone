#!/bin/bash

docker build \
    --secret id=hugging_token,src=.env \
    --build-arg home=$HOME \
    -t capstone .