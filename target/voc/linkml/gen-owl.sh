#!/bin/env bash

gen-linkml -f yaml domain.linkml.yaml > domain.linkml.induced.yaml
gen-owl domain.linkml.induced.yaml > domain.owl.ttl
