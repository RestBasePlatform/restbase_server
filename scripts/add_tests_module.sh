#!/bin/bash
# Script to create folder in tests module with project structure

mkdir ./tests/$1 && cd ./tests/$1 && touch conftest.py && mkdir static && mkdir static/requests && mkdir static/responses
