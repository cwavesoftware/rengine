def DD_URL = "http://192.168.7.233:28080"
def PRODUCT_NAME = "SampleMultirepoApp"

pipeline {
    agent any
    tools {
        nodejs 'nodejs_16.17.0'
    }

    environment {
        SNYK_TOKEN = credentials('snyk_token')
        DD_APIKEY = credentials('defectdojo_apikey')
    }

    stages {
        stage('SAST scan') {
            steps {
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
                sh '''
                    ./snyk code test --json > snyk_code_report.json || true
                '''                
            }
        }
        stage('Upload to DD') {
            steps {
                echo 'Preparing files for upload ...'
                sh 'cat snyk_code_report.json | node snyk-to-html/dist/index.js -o snyk_code_report.html'
                sh 'zip snyk_code_report.zip snyk_code_report* && echo "zip file created"'
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
                    -F 'file=@snyk_code_report.zip;type=application/zip' \
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
    }
}