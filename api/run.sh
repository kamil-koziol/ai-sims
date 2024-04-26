#!/bin/bash

POSITIONAL_ARGS=()
DEVICES=""

while [[ $# -gt 0 ]]; do
    case $1 in 
        -d|--devices)
        DEVICES=$2
        shift
        shift
        ;;
        -h|--help)
        echo "Run model api. Flags:
        -d | --devices  -> select CUDA devices
        -h | --help     -> print help"
        exit
    esac
done

if [[ "$DEVICES" == "" ]]; then
    echo "YOU MUST SELECT CUDA DEVICE"
    exit
fi

CUDA_VISIBLE_DEVICES=$DEVICES uvicorn main:app --host 0.0.0.0 --reload