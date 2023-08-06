#!/bin/bash

SCRIPT=$(readlink -f "$0")
FOLDER=$(dirname "$SCRIPT")
VENV="${FOLDER}/py3venv"

# ================================================================================================
# Helper functions
# ================================================================================================
function errexit(){
  echo "🔥 [Error]: $*" 1>&2
  exit 1
}

# ------------------------------------------------------------------------------------------------
function warn(){
  echo "⚠️ [Warning]: $*" 1>&2
}

# ------------------------------------------------------------------------------------------------
function action(){
  local save=no
  local timing=no
  local logmode=on_error
  local details=no
  local showlog=no
  local ctx=
  local ctxlbl=
  local title="Running action"
  while [ $# -gt 0 ] && [[ "$1" =~ ^-.* ]]; do
    local param="$1"
    shift
    case "$param" in
      -s|--save)          local save=yes;               ;;
      -T|--timing)        local timing=yes              ;;
      -t|--title)         local title="$1";       shift ;;
      -a|--log-always)    local logmode=always          ;;
      -n|--log-never)     local logmode=never           ;;
      -e|--log-on-error)  local logmode=on_error        ;;
      -d|--details)       local details=yes             ;;
      -v|--verbose)       local details=yes
                          local logmode=always
                          local timing=yes
                          local save=yes
      ;;
      *)                  errexit "Unknown option to action command: '$param'" ;;
    esac
  done

  local title="${title:-\"Running '$1' command\"}"
  local tmplog=$(mktemp /tmp/action.XXXXXX)

  T_START="$(date -u --iso-8601 )"
  T_START_S="$(date -u +"%s" )"
  echo -n "$T_START ✨ $title ... "  1>&2
  "$@" >${tmplog} 2>&1
  local RC=$?
  T_END="$(date -u --iso-8601 )"
  T_END_S="$( date -u +"%s" )"
  T_ELAPSED=$(( T_END_S - T_START_S ))

  if [ $RC -ne 0 ] ; then
    local msg="❌ Failed." 1>&2
  else
    local msg="✅ Succeeded." 1>&2
  fi

  echo "$msg" 1>&2
  if [ "$timing" == yes ]; then
    echo "  🕑 Start time:   ${T_START}" 1>&2
    echo "  🕑 End time:     ${T_END}" 1>&2
    echo "  ⌛  Duration:     ${T_ELAPSED} s" 1>&2
  fi
  if [ "${details}" == yes ];  then
    echo "  〈/〉 Command line: $*" 1>&2
    echo "  ⏎  Return code:  $RC" 1>&2
  fi
  if [ "${RC}" -eq 0 ]; then
    if [ "${logmode}" == always ]; then
      local showlog=yes
    fi
  else
    if [ "${logmode}" != never ]; then
      local showlog=yes
    fi
  fi
  if [ "${showlog}" == yes ]; then
    echo "  ⦿ Output:" 1>&2
    cat ${tmplog} | sed 's/^/    | /' 1>&2
  fi
  if [ "$save" == yes ]; then
    logfile="./op-${T_START_S}.log"
    cp ${tmplog} "${logfile}"
    echo "📁 Log file saved to ${logfile}" 1>&2
  fi
  return $RC
}

# ------------------------------------------------------------------------------------------------
function usage(){
  cat <<EOF
Usage:
    ops.sh COMMAND [arg [arg [...]]]

Where COMMAND is one of the following:
  Environment set-up commands
    build-venv          - Build the development environment.
    rebuild-venv        - Delete and reuild the development environment.

  Documentation
    docs                - Generate documentation (Note 4,5)

  Unit testing and static analysis
    unit-test           - Run unit testing directly in current environment (Note 3).
    coverage            - Generate code coverage data (Note 3).
    quality             - Run code quality analysis (Note 4,6)
    style               - Run code style analysis and tests (Note 6)

  Regression testing
    test                - Run tox testing (Note 1).
    test-envs           - Run tox testing on specified environments (Note 2).
    test-py-all         - Run tox testing on python unit test environments (Note 1).
    test-style-quality  - Run tox testing on style and quality test environments (Note 1).
    test-coverage       - Run tox testing on coverage test environment (Note 1).

  Release
    prerelease-tests    - Run a quick set of tests required for release.
    prerelease          - Ensure the working directory is clean, and run prerelease tests.
    release-major       - Perform a release upgrading the major version of the repository.
    release-minor       - Perform a release upgrading the minor version of the repository.
    release-patch       - Perform a release upgrading the patch version of the repository.

  -h|--help|help      - Display this help and exit.

Notes:
1) additional args passed directly to tox
2) additional args specify desired tox test environments to run
3) additional args passed directly to pytest
4) automatically generates coverage data first
5) additional args passed directly to setup.py
6) extra args ignored.
EOF
  exit 0
}

# ------------------------------------------------------------------------------------------------
function activate_venv(){
  # shellcheck disable=SC1091
  if ! . "${VENV}/bin/activate"; then
    errexit "Error: can't activate python3 environment."
  fi
}

# ------------------------------------------------------------------------------------------------
function has_untracked_files(){
  [ "$(git status --porcelain 2>/dev/null | grep -Ec '^(M| [MD]|\?\?|u) ')" != 0 ]
}

# ------------------------------------------------------------------------------------------------
function require_working_directory_clean(){
  if has_untracked_files; then
    echo "Working directory is not clean." 1>&2
    git status
    false
  else
    true
  fi
}

# ------------------------------------------------------------------------------------------------
function do_action(){
  case "$1" in
    rebuild-venv)
      local interpreter=${2-python3}
      action -t "Delete python3 environment." rm -rf "${VENV}" || errexit "Failed to remove Python virtual environment."
      "${SCRIPT}" build-venv "${interpreter}"
    ;;

    build-venv)
      local interpreter=${2-python3}
      if [ ! -d "${VENV}" ]; then
        action -t  "Create python3 environment" "${interpreter}" -m venv "${VENV}" || errexit "Failed to create Python virtual environment."
      fi
      activate_venv
      action -t "Upgrade python3 pip"                pip install --upgrade pip || errexit "Failed to upgrade pip."
      action -t "Install development requirements"   pip install -r "requirements-dev.txt" || errexit "Failed to install development dependencies."
      action -t "Install runtime requirements"       pip install -r "requirements.txt" || errexit "Failed to install dependencies."
      action -t "Install python project"             python "${FOLDER}/setup.py" develop || errexit "Failed to install project to Python virtual environment."
    ;;

    test)
      shift
      action -t "Run tox tests: all" tox -vv "$@" || errexit "Failed tox tests: all."
    ;;

    test-envs)
      shift
      envs="$*"
      # shellcheck disable=SC2086
      action -t "Run tox tests: envs=${envs}" tox -vv -e ${envs// /,} || errexit "Failed tox tests: all/custom."
    ;;

    test-py-all)
      shift
      action -t "Run tox tests: all python" tox -vv "$@" -e py37,py38,py39,py310,py311 || errexit "Failed tox tests: python3.7 - python3.11."
    ;;

    test-style-quality)
      shift
      action -t "Run tox tests: style,quality" tox -vv "$@" -e style,quality || errexit "Failed tox tests: style,quality."
    ;;

    test-coverage)
      shift
      action -t "Run tox tests: coverage" tox -vv "$@" -e coverage || errexit "Failed tox tests: coverage."
    ;;

    unit-test)
      shift
      activate_venv
      export PYTHONUNBUFFERED=yes
      action -t "Run Python unit tests" pytest -vv --basetemp="${FOLDER}/tests" "$@" || errexit "Failed one or more unit tests."
    ;;

    coverage)
      shift
      activate_venv
      action -t "Generate Coverage Data" pytest --cov-config=./.coveragerc --cov=${PROJECT_NAME} --cov-report html -vv --basetemp="${FOLDER}/${PROJECT_NAME}" "$@" || errexit "Failed to generate code coverage report."
    ;;

    docs)
      shift
      if [ "$1" == "--no-coverage" ]; then
        shift
      else
        do_action coverage
      fi
      action -t "Clean autogenerated doc stubs" rm -rf "${FOLDER}/docs/_autosummary" || errexit "Failed to generate documentation stubs."
      action -t "Clean previously built docs" rm -rf "${FOLDER}/docs/build" || errexit "Failed to clean documentation."
      action -t "Build Documentation" python3 setup.py build_sphinx "$@" || errexit "Failed to build documentation."
    ;;

    quality)
      shift
      if [ "$1" == "--no-coverage" ]; then
        shift
      else
        do_action coverage
      fi
      rm ./op.log
      touch ./op.log
      action -t "Compute Cyclomatic Complexity (CC)" radon cc -s -i '__pending*' ./${PROJECT_NAME} || errexit "Failed to compute code complexity."
      action -t "Compute Maintainability Index (MI)" radon mi -s -i '__pending*' ./${PROJECT_NAME} || errexit "Failed to compute code maintainability."
      action -t "Compute raw statistics (RAW)" radon raw -s -i '__pending*' ./${PROJECT_NAME} || errexit "Failed to compute code statistics."
      action -t "Analyze Code Quality" xenon -b C -m A -a A -i '__pending*' ./${PROJECT_NAME} || errexit "Failed to analyze code quality."
    ;;

    style)
      shift
      activate_venv
      export PYTHONUNBUFFERED=yes
      action -t  "Check Source code Style Compliance" flake8 --max-line-length=120 --ignore=E201,E202,E401,E221,E241,E251,E271,W504,E272 --exclude '__pending*' ./${PROJECT_NAME} || errexit "Failed code style checks."
    ;;
    -h|--help|help)
      usage
    ;;

    prerelease-tests)
      do_action unit-test
      do_action coverage
      do_action quality --no-coverage
      do_action style
      do_action docs --no-coverage
    ;;

    prerelease)
      action -t  "Ensure working directory is clean." require_working_directory_clean || errexit "Refusing to release unclean code."
      do_action prerelease-tests
    ;;

    release-major)
      do_action prerelease
      action -t  "Increment the version number (major)." bumpversion major || errexit "Failed to bump version."
      action -t  "Push changes" git push || errexit "Failed to push code."
      action -t  "Push tags"    git push --tags  || errexit "Failed to push tags."
    ;;

    release-minor)
      do_action prerelease
      action -t  "Increment the version number (minor)." bumpversion minor || errexit "Failed to bump version."
      action -t  "Push changes" git push || errexit "Failed to push code."
      action -t  "Push tags"    git push --tags  || errexit "Failed to push tags."
    ;;

    release-patch)
      do_action prerelease
      action -t  "Increment the version number (patch)." bumpversion patch || errexit "Failed to bump version."
      action -t  "Push changes" git push || errexit "Failed to push code."
      action -t  "Push tags"    git push --tags  || errexit "Failed to push tags."
    ;;

    check-clean)
        action -t  "Checking what would be removed with clean" git clean -xdn -e '*venv*/' -e op-*.log
    ;;

    clean)
        action -t  "Removing built files but preserving venv" git clean -xdf -e '*venv*/' -e op-*.log || errexit "Failed to clean working dir."
    ;;

    check-clean-all)
        action -t  "Checking what would be removed with clean-all" git clean -xdn -e op-*.log
    ;;

    clean-all)
        action -t  "Removing built files and venv" git clean -xdf -e op-*.log || errexit "Failed to clean working dir."
    ;;

    *)
      errexit "Unknown action '$1'. Try '$0 --help' for more information."
    ;;
  esac
}

# ================================================================================================
# Main Entrypoint
# ================================================================================================
cd "${FOLDER}" || errexit "Script exists but parent directory doesn't."
. "ops.env"    || errexit "Unable to load ops.env environment file needed by ops.sh"
do_action "$@"
