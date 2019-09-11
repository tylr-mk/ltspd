#!/bin/bash
#
# define colors:
COLOR_RESET="\033[0m"
COLOR_BLACK="\033[1m\033[30m"
COLOR_RED="\033[1m\033[31m"
COLOR_GREEN="\033[1m\033[32m"
COLOR_YELLOW="\033[1m\033[33m"
COLOR_BLUE="\033[1m\033[34m"
COLOR_MAGENTA="\033[1m\033[35m"
COLOR_CYAN="\033[1m\033[36m"
COLOR_WHITE="\033[1m\033[37m"

# Run all our unit tests and style conformance tests.
# Exit code is the number of those tests which failed.

# Don't exit immediately on a shell error, or we'll die
# on tests that fail.
set +e

# Change to our containing directory, so all tests can be
# run relative to this.
scriptname=$0
scriptdir=`dirname $scriptname`
echo "Changing to $scriptdir to run tests."
cd $scriptdir

# We keep track of how many tests fail, and use that
# as our exit code.
failed=0
ran=0

failed_commands=()

runtest() {
    cmd=$1;

    printf "${COLOR_YELLOW}Running \`$cmd\` ... ${COLOR_RESET}\n"
    # Run each test in a subshell so each can change directory (or
    # indeed do most other things) without affecting subsequent tests.
    eval "($cmd)"
    retcode=$?

    ran=`expr $ran + 1`

    if [ $retcode -ne 0 ]; then
        printf "${COLOR_RED}FAILED \`$cmd\` with code $retcode.${COLOR_RESET}\n"
      failed=`expr $failed + 1`
      failed_commands+=("$cmd")
    fi
}

# checking python requirements are up-to-date
runtest "flake8  ltspd/"
runtest "flake8  tests/test_ltspd/"
runtest "pip install -e '.[test, dev]' -q "
runtest "pytest --cov=ltspd tests/test_ltspd/"

# And exit cleanly, saying if anything failed.
 if [ $failed -gt 0 ]; then
     echo "!!!"
     echo "!!! Ran $ran tests but $failed failed."
     echo "!!!"
     echo "!!! Failed commands were: "
     echo "!!!"

     for cmd in "${failed_commands[@]}"; do
       echo "!!!   $cmd"
     done
     echo "!!!"
 else
     echo
     echo "Ran and passed $ran tests."
     echo
 fi

 exit $failed
