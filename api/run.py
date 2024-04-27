#!/usr/bin/env python
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Run model api.")
    parser.add_argument("-d", "--devices", help="select CUDA devices", required=True)
    args = parser.parse_args()

    if not args.devices:
        print("YOU MUST SELECT CUDA DEVICE")
        exit()

    os.environ["CUDA_VISIBLE_DEVICES"] = args.devices
    os.system("uvicorn main:app --host 0.0.0.0 --reload")

if __name__ == "__main__":
    main()