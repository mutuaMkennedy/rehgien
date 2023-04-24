pipeline {
    agent {
        docker { 
            // NOTE: Using ubuntu as it has support for AWS CLI. Other images like Alpine based images will not work with AWS CLI
            image 'ubuntu:latest'
        }
    }

     environment {
        AWS_DEFAULT_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')
        SSH_CREDENTIALS = credentials("SSH_CREDENTIALS")
        DOMAIN_NAME = "rehgien.crunchgarage.com"
    }

    stages {
        stage('Install Docker and Docker Compose'){
            steps{
                // Update packages

                sh "sudo apt-get update"
                
                // Install Docker ref:- https://docs.docker.com/engine/install/ubuntu/

                sh "sudo apt-get install ca-certificates curl gnupg"

                sh '''
                    sudo install -m 0755 -d /etc/apt/keyrings
                    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
                    sudo chmod a+r /etc/apt/keyrings/docker.gpg
                '''

                sh '''
                    echo \
                    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
                    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
                    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
                '''

                sh '''
                    sudo apt-get update
                    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
                '''

                // Verify docker has been installed successfully
                sh '''
                    echo Checking Docker installation
                    sudo docker run hello-world
                '''

                // Verify docker compose has been installed successfully
                sh '''
                    echo Checking Docker compose installation
                    docker compose version
                '''
            }
        }
        stage('Install AWS CLI') {
            steps {
                // Install AWS CLI so we can run aws command in the next steps in the pipline
                sh '''
                    #!/bin/bash -l
                    echo Installing AWS CLI
                    apt-get update
                    apt-get install -y curl unzip
                    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
                    unzip -o awscliv2.zip
                    ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update
                    echo Check aws cli is installed correctly
                    aws --version
                    echo Done checking installation
                '''
            }
        }

        stage('Build') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-account-credentials', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    // Checkout the source code from the Git repository
                    git 'https://github.com/mutuaMkennedy/rehgien.git'
                    // Copy our .env file to the repository
                    sh "aws s3 cp s3://rehgien/.env ."  
                    // Build the Docker images for the Django app and its dependencies using Docker Compose
                    sh 'docker compose -f docker-compose-prod.yml build'
                }
            }
        }

        stage('Test') {
            steps {
                // Start the Docker containers for the Django app and its dependencies using Docker Compose
                sh 'docker compose -f docker-compose-prod.yml up -d'
                // Run the tests for the Django app
                sh 'docker compose -f docker-compose-prod.yml run --rm django python manage.py test'
                // Stop the Docker containers
                sh 'docker compose -f docker-compose-prod.yml down'
            }
        }
    
        stage('Push to ECR') {
            steps {

                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-account-credentials', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    // Authenticate Docker client to Amazon ECR registry
                    sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
                    // Push your Docker image to Amazon ECR repository
                    // We've already tagged the images in our docker-compose-prod.yml so just push
                    sh "docker compose -f docker-compose-prod.yml push"
                }

            }
        }

        stage('Deploy to EC2') {
            steps {
                // Deploy the Docker image to Amazon EC2 instance
                 sshagent(credentials: ['${SSH_CREDENTIALS}']) {
                    // We have tagged the images on our docker compose prod file so just call the pull command
                    sh 'ssh ${SSH_CREDENTIALS_USR}@${DOMAIN_NAME} "docker compose -f docker-compose-prod.yml pull"'
                    // Restart the Docker containers
                    sh 'ssh ${SSH_CREDENTIALS_USR}@${DOMAIN_NAME} "docker compose -f docker-compose-prod.yml up -d --no-deps --remove-orphans"'
                }
            }
        }
        
    }
}