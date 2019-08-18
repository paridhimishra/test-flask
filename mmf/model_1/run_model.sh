#!/bin/bash

usage () {
    echo "Usage"
    echo "   -m|--model <model_path> - Absolute path to the Model directory"
    echo "   -p|--path <S3_path> - Path to read/store model artefacts in S3"
    echo "   -v|--version <model_version> - Version of model"
}

parse_arguments () {

    # saner programming env: these switches turn some bugs into errors
    set -o pipefail -o noclobber -o nounset

    # -allow a command to fail with !’s side effect on errexit
    # -use return value from ${PIPESTATUS[0]}, because ! hosed $?
    ! getopt --test > /dev/null
    if [[ ${PIPESTATUS[0]} -ne 4 ]]; then
        echo 'I’m sorry, `getopt --test` failed in this environment.'
        exit 1
    fi

    OPTIONS=m:p:v:
    LONGOPTS=model:,path:,version:

    # -regarding ! and PIPESTATUS see above
    # -temporarily store output to be able to check for errors
    # -activate quoting/enhanced mode (e.g. by writing out “--options”)
    # -pass arguments only via   -- "$@"   to separate them correctly
    ! PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTS --name "$0" -- "$@")
    if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
        # e.g. return value is 1
        #  then getopt has complained about wrong arguments to stdout
        exit 2
    fi
    # read getopt’s output this way to handle the quoting right:
    eval set -- "$PARSED"

    model_path=""
    s3_path=""
    version=""
    # now enjoy the options in order and nicely split until we see --
    while true; do
        case "$1" in
            -m|--model)
                model_path="$2"
                shift 2
                ;;
            -p|--path)
                s3_path="$2"
                shift 2
                ;;
            -v|--version)
                version="$2"
                shift 2
                ;;
            --)
                shift
                break
                ;;
            *)
                echo "Unknown argument passed"
                exit 3
                ;;
        esac
    done

    # Handle missing arguments
    cmdline_errors=""
    if [ -z "${model_path}" ]; then
       cmdline_errors+="   Model Path not specified\n"
    else
       if [ ! -e "${model_path}/master.yml" ]; then
          cmdline_errors+="   No master.yml found in ${model_path}\n"
       else
          export MODEL_HOME="${model_path}"
       fi
    fi

    if [ -z "${version}" ]; then
       cmdline_errors+="   Model version not passed\n"
    else
       export MODEL_VERSION="${version}"
    fi

    if [ -z "${s3_path}" ]; then
       cmdline_errors+="   Path in S3 not specified\n"
    else
       export MODEL_RUN_DATE="${s3_path}"
    fi

    if [ ! -z "${cmdline_errors}" ]; then
       echo "Errors parsing arguments"
       echo -e "${cmdline_errors}"
       usage
       exit 255
    fi
}

run_model () {

    export MODEL_ENV=${ENVIRONMENT}
    export MODEL_DLR=$(echo ${TEAM_KEY} | sed -e "s/^M_//" )
    export MODEL_STATE='sit'
    export MODEL_S3_BUCKET_BASE_KEY="${MODEL_STATE}/v${MODEL_VERSION}/model_run_${MODEL_RUN_DATE}"

    # Not required only used with Artifactory
    # But defined to not cause errors
    export MODEL_NAME='not_needed'
    export MODEL_REPO='not_needed'
    export ARTIFACTORY_BRANCH='not_needed'

    # Used when executed via Airflow
    export SNS_TOPIC='not_needed'

    validation_errors=""
    if [ -z "${MODEL_ENV}" ]; then
       validation_errors+="MODEL_ENV not passed\n"
    fi

    if [ -z "${MODEL_DLR}" ]; then
       validation_errors+="variable MODEL_DLR not passed\n"
    fi

    if [ -z "${MODEL_S3_BUCKET_BASE_KEY}" ]; then
       validation_errors+="varible MODEL_S3_BUCKET_BASE_KEY not set\n"
    fi

    if [ -z "${SNS_TOPIC}" ]; then
       validation_errors+="varible SNS_TOPIC not passed\n"
    fi

    if [ ! -z "${validation_errors}" ]; then

        rc=255
        response="${validation_errors}"

    else

        ######
        # Some globals

        # Team name should always be lower
        export AWS_TEAM=$(echo ${MODEL_DLR} | tr '[:upper:]' '[:lower:]')
        export AWS_ENV=$(echo ${MODEL_ENV} | tr '[:upper:]' '[:lower:]')

        # Model Related
        export MODEL_VARS_FILE=${MODEL_HOME}/vars.yml

        # AWS Related
        run_type="team"
        bucket_prefix=""
        if [[ ${TEAM_KEY} == M_* ]]; then
            run_type="model"
            bucket_prefix="-model"
        fi

        export MODEL_S3_BUCKET="ndc${AWS_ENV}-ndc${bucket_prefix}-${AWS_TEAM}"
        export MODEL_KMS_KEY="alias/ndc${AWS_ENV}-${run_type}-${AWS_TEAM}"

        # Redshift
        export REDSHIFT_USER="${AWS_TEAM}_model_read_user"
        export REDSHIFT_DB="${AWS_TEAM}_modeldb"

        # Audit Related
        export MODEL_S3_BUCKET_BASE=${MODEL_S3_BUCKET_BASE_KEY}
        export MODEL_S3_BUCKET_ARTIFACT="${MODEL_S3_BUCKET_BASE}/model"
        export MODEL_S3_BUCKET_SOURCE="${MODEL_S3_BUCKET_BASE}/source"
        export MODEL_S3_BUCKET_INPUT="${MODEL_S3_BUCKET_BASE}/input"
        export MODEL_S3_BUCKET_OUTPUT="${MODEL_S3_BUCKET_BASE}/output"
        export MODEL_S3_BUCKET_LOGS="${MODEL_S3_BUCKET_BASE}/logs"

        echo "S3 path for model run will be s3://${MODEL_S3_BUCKET}/${MODEL_S3_BUCKET_BASE}"

        # Local directories
        export LOCAL_LOGS="${MODEL_HOME}/artifacts/logs"
        if [ -e "${LOCAL_LOGS}" ]; then
            rm -rf "${LOCAL_LOGS}"
        fi
        mkdir -p "${LOCAL_LOGS}"

        # Setup Ansible Logging
        export ANSIBLE_DEBUG=False
        export ANSIBLE_LOG_PATH="${LOCAL_LOGS}/model_exec_${MODEL_RUN_DATE}.log"
        echo "Logging to ${ANSIBLE_LOG_PATH}"

        # Remove previous log
        if [ -e "${ANSIBLE_LOG_PATH}" ]; then
            rm ${ANSIBLE_LOG_PATH}
        fi

        # Setup ansible vars file to make environment vars available to ansible
        if [ -e "${MODEL_VARS_FILE}" ]; then
            rm ${MODEL_VARS_FILE}
        fi

        touch ${MODEL_VARS_FILE}
        for x in \
                 MODEL_HOME MODEL_NAME MODEL_VERSION MODEL_RUN_DATE \
                 MODEL_S3_BUCKET MODEL_KMS_KEY MODEL_STATE \
                 MODEL_S3_BUCKET_BASE MODEL_S3_BUCKET_SOURCE MODEL_S3_BUCKET_INPUT MODEL_S3_BUCKET_OUTPUT MODEL_S3_BUCKET_LOGS\
                 LOCAL_LOGS \
                 MODEL_ENV; \
        do
            echo "${x}: \"${!x}\"" >> ${MODEL_VARS_FILE}
        done

        # Call Ansible with multiple verbose (-vvv)
        ansible_error=$(ansible-playbook -vvv --connection=local --inventory 127.0.0.1, ${MODEL_HOME}/master.yml --extra-vars="@${MODEL_VARS_FILE}" 2>&1 >/dev/null)
        rc=$?

        if [ ${rc} -gt 0 ]; then
            echo "Job failed"
            echo $ansible_error
        else
            echo "Job passed"
        fi
    fi
}


parse_arguments $@
echo "model: $model_path, S3: $s3_path, Version: $version"
run_model
