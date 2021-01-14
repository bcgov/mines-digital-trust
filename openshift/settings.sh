#!/bin/bash

export PROJECT_NAMESPACE="a3e512"
export GIT_URI="https://github.com/bcgov/mines-digital-trust.git"
export GIT_REF="develop"

# The templates that should not have their GIT referances(uri and ref) over-ridden
# Templates NOT in this list will have they GIT referances over-ridden
# with the values of GIT_URI and GIT_REF
export -a skip_git_overrides="agent-build.yaml db-build.yaml"

export APPLICATION_DOMAIN_POSTFIX=.apps.silver.devops.gov.bc.ca
