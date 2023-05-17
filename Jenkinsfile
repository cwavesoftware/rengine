def DD_URL = "http://10.251.0.84:8080"
def PRODUCT_NAME = "SampleMultirepoApp"
def TF_URL = "https://10.251.0.84/threadfix"
def TF_APP_ID = "1"
def REPORT_FILE_NAME = "snyk_code_report"

pipeline {
    agent any
    tools {
        nodejs 'nodejs_16.17.0'
    }

    environment {
        SNYK_TOKEN = credentials('snyk_token')
        DD_APIKEY = credentials('defectdojo_apikey')
        TF_APIKEY = credentials('tf_apikey')

    }

    stages {
        stage('SAST scan') {
            steps {
                echo 'Checking node version'
                sh 'node -v'

                echo 'Getting snyk cli ...'
                sh '''
                    #!/bin/bash
                    curl https://static.snyk.io/cli/latest/snyk-linux -o snyk
                    chmod +x ./snyk
                    ./snyk -h
                '''

                echo 'Getting snyk-to-html ...'
                dir('snyk-to-html') {
                    git url: 'https://github.com/cwavesoftware/snyk-to-html.git'
                }
                sh 'npm install ./snyk-to-html/'
                sh 'node snyk-to-html/dist/index.js -h'

                echo 'Scanning code ...'
                sh """
                    ./snyk code test --json > ${REPORT_FILE_NAME}.json || true
                """             
            }
        }
        stage('Upload to DD') {
            steps {
                echo 'Preparing files for upload ...'
                sh "cat ${REPORT_FILE_NAME}.json | node snyk-to-html/dist/index.js -o ${REPORT_FILE_NAME}.html"
                sh "zip ${REPORT_FILE_NAME}.zip ${REPORT_FILE_NAME}* && echo 'zip file created'"
                sh 'echo "Uploading ..."'
                sh """
                    curl -X 'POST' \
                    '${DD_URL}/api/v2/import-scan/' \
                    -H 'accept: application/json' \
                    -H 'Content-Type: multipart/form-data' \
                    -H 'Authorization:  Token $DD_APIKEY' \
                    -F 'minimum_severity=Info' \
                    -F 'active=true' \
                    -F 'verified=false' \
                    -F 'scan_type=Snyk Code Scan' \
                    -F 'file=@${REPORT_FILE_NAME}.zip;type=application/zip' \
                    -F 'product_name=${PRODUCT_NAME}' \
                    -F "engagement_name=\${PWD##*/}" \
                    -F 'deduplication_on_engagement=true' \
                    -F 'close_old_findings=false' \
                    -F 'close_old_findings_product_scope=false' \
                    -F 'push_to_jira=false' \
                    -F 'create_finding_groups_for_all_findings=true' \
                    -F 'auto_create_context=true'
                """
            }
        }
        stage('Upload to TF') {
            steps {
                echo 'Uploading to Threadfix ...'
                echo "Converting to .threadfix format ..."
                echo "Installing converter ..."
                dir('snyk-code-threadfix') {
                    git url: 'https://github.com/cwavesoftware/snyk-code-threadfix.git'
                }
                sh "npm install ./snyk-code-threadfix/"
                echo "Doing conversion ..."
                sh "node ./snyk-code-threadfix/dist/index.js snyk_code_report.json \$(pwd) && ls -al snyk_code_report.threadfix"

                sh """
                    curl --http1.1 --insecure -H "Accept: application/json" -H "Authorization: APIKEY $TF_APIKEY" -X POST --form file=@snyk_code_report.threadfix ${TF_URL}/rest/latest/applications/${TF_APP_ID}/upload
                """
            }
        }
    }
}
