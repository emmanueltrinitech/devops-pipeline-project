pipeline {

    agent any

    environment {

        IMAGE_NAME = "trinitech-devops-app"

        APP_SERVER = "devops@deploy01"

        APP_PORT = "8081"

    }

    stages {

        stage('Checkout') {

            steps {

                checkout scm

            }
        }


        stage('Environment Info') {

            steps {

                sh '''
                echo "Job Name: ${JOB_NAME}"
                echo "Build Number: ${BUILD_NUMBER}"
                echo "Workspace: ${WORKSPACE}"

                hostname
                whoami
                '''

            }
        }


        stage('Install Dependencies') {

            steps {

                sh '''
                rm -rf venv

                python3 -m venv venv

                . venv/bin/activate

                pip install --upgrade pip

                pip install -r requirements.txt
                '''

            }
        }


        stage('Application Validation') {

            steps {

                sh '''
                . venv/bin/activate

                python -m py_compile app.py
                '''

            }
        }


        stage('Docker Build') {

            steps {

                sh '''
                docker build \
                -t ${IMAGE_NAME}:${BUILD_NUMBER} .

                docker images \
                ${IMAGE_NAME}:${BUILD_NUMBER}
                '''

            }
        }


        stage('Save Image') {

            steps {

                sh '''
                docker save \
                ${IMAGE_NAME}:${BUILD_NUMBER} \
                -o ${IMAGE_NAME}.tar
                '''

            }
        }


        stage('Transfer Image') {

            steps {

                sh '''
                scp \
                ${IMAGE_NAME}.tar \
                ${APP_SERVER}:/home/devops/deployments/
                '''

            }
        }


        stage('Deploy') {

            steps {

                sh '''
                ssh ${APP_SERVER} "

                docker load \
                -i /home/devops/deployments/${IMAGE_NAME}.tar

                docker rm -f ${IMAGE_NAME} || true

                docker run -d \
                --name ${IMAGE_NAME} \
                --restart unless-stopped \
                -p ${APP_PORT}:8081 \
                ${IMAGE_NAME}:${BUILD_NUMBER}

                "
                '''

            }
        }


        stage('Health Check') {

            steps {

                sh '''
                sleep 5

                curl -f \
                http://deploy01:${APP_PORT}/health
                '''

            }
        }

    }


    post {

        success {

            echo 'DEPLOYMENT SUCCESSFUL'

        }

        failure {

            echo 'PIPELINE FAILED'

        }

        always {

            sh '''
            rm -f ${IMAGE_NAME}.tar
            '''

        }

    }

}
