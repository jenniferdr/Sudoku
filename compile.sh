#! /bin/bash

export MROOT=$(pwd)/minisat
cd minisat/core
make rs
cp minisat_static ../../