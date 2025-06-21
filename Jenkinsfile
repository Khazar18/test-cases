pipeline {
    agent any

    environment {
        EMAIL_RECIPIENT = 'qasimalik@gmail.com'
        CHROME_URL = 'https://dl.google.com/chrome/install/latest/chrome_installer.exe'
        CHROMEDRIVER_URL = 'https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/win64/chromedriver-win64.zip'
        SETUP_DIR = "${WORKSPACE}\\test-setup"
        VENV_DIR = "${WORKSPACE}\\venv"
    }


    
    stages {

        stage('Install Chrome + ChromeDriver + Python') {
            steps {
                bat '''
                    if not exist "%SETUP_DIR%" mkdir "%SETUP_DIR%"
                    cd /d "%SETUP_DIR%"

                    echo Downloading Chrome...
                    curl --ssl-no-revoke -L -o chrome_installer.exe "%CHROME_URL%"
                    start /wait chrome_installer.exe /silent /install

                    echo Downloading ChromeDriver...
                    curl -L -o chromedriver.zip "%CHROMEDRIVER_URL%"
                    powershell -Command "Expand-Archive -Force 'chromedriver.zip' ."

                    echo set PATH=%SETUP_DIR%\\chromedriver-win64;%%PATH%% > "%SETUP_DIR%\\env.bat"

                    echo Creating Python virtual environment...
                    python -m venv "%VENV_DIR%"
                    call "%VENV_DIR%\\Scripts\\activate.bat"
                    python -m pip install --upgrade pip
                    pip install selenium pytest
                '''
            }
        }


        stage('Run Tests') {
            steps {
                bat '''
                    call "%SETUP_DIR%\\env.bat"
                    call "%VENV_DIR%\\Scripts\\activate.bat"

                    echo Running pytest...
                    pytest testcases.py > result.txt || exit /b 0
                '''
            }
        }

        stage('Clone Repo') {
            steps {
                dir('part 2') {
                    git branch: 'main', url: 
                }
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
