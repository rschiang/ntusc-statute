#!/usr/bin/env bash
scripts/generate.py statute/printing.json
time prince statute.html -v
