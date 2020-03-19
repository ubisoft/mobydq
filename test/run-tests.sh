#!/usr/bin/env bash
# Use this script to trigger tests

if [[ "$TEST_HOST" == "" || "$TEST_PORT" == "" ]]; then
    nose2 -v $TEST_CASE
else
    ./wait-for-it.sh -t 180 $TEST_HOST:$TEST_PORT -- nose2 -v $TEST_CASE
fi