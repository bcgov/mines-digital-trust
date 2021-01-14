FROM frolvlad/alpine-glibc:latest

RUN apk update && apk upgrade && \
    apk add --no-cache bash git curl jq tar openssl

ARG OC_VERSION=4.6
ARG BUILD_DEPS='tar gzip'
ARG RUN_DEPS='curl ca-certificates gettext bash git jq'

ENV src_dir /usr/src
WORKDIR $src_dir

#
# download and install the openshift command-line interface
#
RUN apk --no-cache add $BUILD_DEPS $RUN_DEPS && \
    curl -sLo /tmp/oc.tar.gz https://mirror.openshift.com/pub/openshift-v$(echo $OC_VERSION | cut -d'.' -f 1)/clients/oc/$OC_VERSION/linux/oc.tar.gz && \
    tar xzvf /tmp/oc.tar.gz -C /usr/local/bin/ && \
    rm -rf /tmp/oc.tar.gz && \
    apk del $BUILD_DEPS

#
# get the openshift developer tools... and add to the path
#
RUN git clone https://github.com/BCDevOps/openshift-developer-tools.git
ENV PATH "$PATH:$src_dir/openshift-developer-tools/bin"


CMD ["bash"]
