pipeline {
    agent none
    environment {
        GIT_REPO = 'Ev-1/ShiteMusicBot'
        DOCKER_REPO = 'rnorge/music'
        TAG=""
        TEST_FILES = "bot.py cogs/*.py cogs/utils/*.py"
    }
    stages {
        stage('Tests') {
            agent { label 'amd64'}
            steps {
                sh """
                    python3.7 -m venv venv && venv/bin/pip install flake8 && venv/bin/python -m flake8 ${TEST_FILES}
                    rm -rf venv/
                """
                script {
                    TAG = sh(returnStdout: true, script: 'grep -i bot_version cogs/utils/bot_version.py | cut -d" " -f3 | tr -d \\"').trim()
                    SBranch = sh(returnStdout: true, script: 'echo ${GIT_BRANCH} | sed "s#/#_#"').trim()
                }
                sh """
                    python3.7 -m venv venv && venv/bin/pip install isort && venv/bin/python -m isort -c ${TEST_FILES}
                    rm -rf venv/
                """
            }
        }
        stage('Docker Builds') {
            parallel {
                stage('branch') {
                    agent { label 'amd64'}
                    when {
                        not {
                            changeRequest()
                        }
                    }
                    steps {
                        script {
                            if (BRANCH_NAME == 'master') {
                                def image = docker.build("${DOCKER_REPO}:${TAG}-amd64")
                                image.push()
                                }
                                def image = docker.build("${DOCKER_REPO}:${SBranch}-amd64")
                                image.push()
                            }
                        }
                    }
                stage('pr') {
                    agent { label 'amd64'}
                    when {
                        changeRequest()
                    }
                    steps {
                        script {
                            def image = docker.build("${DOCKER_REPO}:PR_$GIT_BRANCH-amd64")
                        }
                    }
                }
            }
        }
    }
}
