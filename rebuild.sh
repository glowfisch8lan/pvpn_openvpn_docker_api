#!/usr/bin/env bash
export PORT=8089;

docker-compose up -d --build --force-recreate

rm -rf ./crt/*

make copykey
