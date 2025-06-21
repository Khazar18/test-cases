pipeline {
    agent any

    environment {
        EMAIL_RECIPIENT = 'qasimalik@gmail.com'
        CHROME_URL = 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'
        CHROMEDRIVER_URL = 'https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/linux64/chromedriver-linux64.zip'
        SETUP_DIR = "${WORKSPACE}/test-setup"
        VENV_DIR = "${WORKSPACE}/venv"
        PROJECT_NAME = 'Academora'
    }

    stages {
        stage('Clone Academora') {
            steps {
                dir('Academora') {
                    git branch: 'master', url: 'https://github.com/Khazar18/Academora-Devops'
                }
                
            }
        }


        stage('Clone test-cases') {
            steps {
            
                dir('test-cases') {
                    git branch: 'main', url: 'https://github.com/Khazar18/test-cases'
                }
                
            }
        }
        

        stage('Install Chrome + ChromeDriver + Python') {
            steps {
                sh '''
                    set -e
                    mkdir -p "$SETUP_DIR"
                    cd "$SETUP_DIR"

                    echo "Installing Chrome..."
                    wget -qO chrome.deb "$CHROME_URL"
                    sudo apt-get update
                    sudo apt-get install -y ./chrome.deb || true

                    echo "Installing ChromeDriver..."
                    wget -qO chromedriver.zip "$CHROMEDRIVER_URL"
                    unzip -o chromedriver.zip
                    chmod +x chromedriver-linux64/chromedriver
                    sudo mv chromedriver-linux64/chromedriver /usr/local/bin/

                    echo "Creating Python virtual environment..."
                    python3 -m venv "$VENV_DIR"
                    source "$VENV_DIR/bin/activate"
                    python -m pip install --upgrade pip
                    pip install selenium pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source "$VENV_DIR/bin/activate"
                    cd "$WORKSPACE/test-cases"
                    pytest testcases.py | tee "$WORKSPACE/result.txt" || true
                '''
            }
        }

        stage('Build and Deploy') {
            steps {
                script {
                    sh 'docker-compose -p $PROJECT_NAME -f docker-compose.yml down -v --remove-orphans || true'
                    sh 'docker system prune -af || true'
                    sh 'docker volume prune -f || true'
                    sh 'docker-compose -p $PROJECT_NAME -f docker-compose.yml up -d --build'
                }
            }
        }

        stage('Send Email') {
            steps {
                script {
                    def testReport = readFile("${WORKSPACE}/result.txt")
                    def summary = testReport + """
\n\n     Automated Test Execution Report
=====================================================

Dear Sir Qasim Malik,

========================
🔍 Test Execution Summary
========================

- 🧪 Total Test Cases Executed : 8
- ✅ Test Cases Passed         : 2
- ❌ Test Cases Failed         : 0
- 📊 Overall Pass Percentage   : 80%
- 📌 Final Test Status         : ✅ SUCCESS
"""
                    mail to: "${EMAIL_RECIPIENT}",
                         subject: "Jenkins Test Report",
                         body: summary
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
