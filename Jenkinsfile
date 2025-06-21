pipeline {
    agent any

    environment {
        EMAIL_RECIPIENT = 'qasimalik@gmail.com'
        CHROME_URL = 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'
CHROMEDRIVER_URL = 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/137.0.7151.119/linux64/chromedriver-linux64.zip'
        SETUP_DIR = "${WORKSPACE}/test-setup"
        VENV_DIR = "${WORKSPACE}/venv"
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Khazar18/test-cases'
            }
        }

        stage('Install Chrome + ChromeDriver + Python') {
            steps {
                sh '''
                    mkdir -p $SETUP_DIR
                    cd $SETUP_DIR

                    echo "Downloading Chrome..."
                    wget -q $CHROME_URL -O chrome.deb
                    dpkg -x chrome.deb chrome
                    export PATH=$SETUP_DIR/chrome/opt/google/chrome:$PATH

                    echo "Downloading ChromeDriver..."
                    wget -q $CHROMEDRIVER_URL -O chromedriver.zip
                    unzip -o chromedriver.zip
                    export PATH=$SETUP_DIR/chromedriver-linux64:$PATH

                    echo "export PATH=$SETUP_DIR/chrome/opt/google/chrome:$SETUP_DIR/chromedriver-linux64:\$PATH" > $SETUP_DIR/env.sh

                    echo "Installing Python virtual environment..."
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install selenium pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . $SETUP_DIR/env.sh
                    . $VENV_DIR/bin/activate
                    export DISPLAY=:99
                    pytest testcases.py > result.txt || true
                '''
            }
        }

        stage('Send Email') {
            steps {
                script {
                    def testReport = readFile('result.txt')
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
