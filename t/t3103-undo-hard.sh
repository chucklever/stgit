#!/bin/sh

test_description='Simple test cases for "stg undo"'

. ./test-lib.sh

# Ignore our own output files.
cat > .git/info/exclude <<EOF
/expected.txt
/actual.txt
EOF

test_expect_success 'Initialize StGit stack with three patches' '
    stg init &&
    echo 000 >> a &&
    git add a &&
    git commit -m a &&
    echo 111 >> a &&
    git commit -a -m p1 &&
    echo 222 >> a &&
    git commit -a -m p2 &&
    echo 333 >> a &&
    git commit -a -m p3 &&
    stg uncommit -n 3
'

cat > expected.txt <<EOF
C a
EOF
test_expect_success 'Pop middle patch, creating a conflict' '
    conflict_old stg pop p2 &&
    stg status a > actual.txt &&
    test_cmp expected.txt actual.txt &&
    test "$(echo $(stg series))" = "+ p1 > p3 - p2"
'

test_expect_success 'Try to undo without --hard' '
    command_error stg undo &&
    stg status a > actual.txt &&
    test_cmp expected.txt actual.txt &&
    test "$(echo $(stg series))" = "+ p1 > p3 - p2"
'

cat > expected.txt <<EOF
EOF
test_expect_success 'Try to undo with --hard' '
    stg undo --hard &&
    stg status a > actual.txt &&
    test_cmp expected.txt actual.txt &&
    test "$(echo $(stg series))" = "> p1 - p3 - p2"
'

test_done
