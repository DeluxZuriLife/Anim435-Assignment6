export PROJECT_ROOT="$HOME/shows"

project() {
    export PROJECT="$1"
}

shot() {
    export SHOT="$1"
    export TASK="$2"
    export PROJECT_DIR="$PROJECT_ROOT/$PROJECT/shots/$SHOT/$TASK"
    cd "$PROJECT_DIR"
    export MAYA_PROJECT="$PROJECT_DIR"
}

