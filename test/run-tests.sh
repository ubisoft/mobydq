#!/usr/bin/env bash
# Use this script to trigger tests

TEST_CASE=$1
TEST_HOST=$2
TEST_PORT=$3

if [ ! -z "$TEST_CASE" ]; then
    echo "Execute test case $TEST_CASE"
    if [ ! -z "$TEST_HOST" ]; then
        echo "Wait for $TEST_HOST:$TEST_PORT"
        ./wait-for-it.sh -t 180 $TEST_HOST:$TEST_PORT -- nose2 -v $TEST_CASE
    else
        nose2 -v "$TEST_CASE"
    fi
else
    echo "Positional argument 1 TEST_CASE is empty"
fi