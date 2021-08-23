#!/bin/bash

export PROJECT_NAMESPACE="a3e512"
export GIT_URI="https://github.com/bcgov/mines-digital-trust.git"
export GIT_REF="develop"

# The templates that should not have their GIT references(uri and ref) over-ridden
# Templates NOT in this list will have they GIT references over-ridden
# with the values of GIT_URI and GIT_REF
export -a skip_git_overrides="db-build.yaml ghg-emissions-agent-build.yaml mines-permitting-agent-build.yaml backup-build.yaml"

export APPLICATION_DOMAIN_POSTFIX=.apps.silver.devops.gov.bc.ca