pipeline {
    agent {
        docker { 
            // Use the Docker image that has all the necessary tools installed for building and deploying the Django app
            image 'docker/compose:1.29.2'
            // Mount the Docker socket from the host to the container to allow Docker-in-Docker (DinD)
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

     environment {
        AWS_DEFAULT_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')
        SSH_CREDENTIALS = credentials("SSH_CREDENTIALS")
        DOMAIN_NAME = "rehgien.crunchgarage.com"
    }

    stages {
        stage('Install AWS CLI') {
            steps {
                // Install AWS CLI so we can run aws command in the next steps in the pipline
                sh '''
                    apk add --no-cache curl
                    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                    unzip awscliv2.zip
                    sudo ./aws/install
                '''
            }
        }

        stage('Build') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'my-aws-creds', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    // Checkout the source code from the Git repository
                    git 'https://github.com/mutuaMkennedy/rehgien.git'
                    // Copy our .env file to the repository
                    sh "aws s3 cp s3://rehgien/.env" 
                    // Build the Docker images for the Django app and its dependencies using Docker Compose
                    sh 'docker-compose -f docker-compose-prod.yml build'
                }
            }
        }

        stage('Test') {
            steps {
                // Start the Docker containers for the Django app and its dependencies using Docker Compose
                sh 'docker-compose -f docker-compose-prod.yml up -d'
                // Run the tests for the Django app
                sh 'docker-compose -f docker-compose-prod.yml run --rm django python manage.py test'
                // Stop the Docker containers
                sh 'docker-compose -f docker-compose-prod.yml down'
            }
        }
    
        stage('Push to ECR') {
            steps {

                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'my-aws-creds', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    // Authenticate Docker client to Amazon ECR registry
                    sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
                    // Push your Docker image to Amazon ECR repository
                    // We've already tagged the images in our docker-compose-prod.yml so just push
                    sh "docker-compose -f docker-compose-prod.yml push"
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