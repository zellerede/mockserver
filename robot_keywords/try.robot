*** Settings ***
Documentation    Tests assume MockServer is running on localhost:8000
...              If not, issue `manage.py runserver`.
Resource      mock_server.robot

*** Variables ***
${Fixtures}    ${CURDIR}/..

*** Test Cases ***
Try Init Without Parameters
    Init MockServer

Try Init With Json
    Init MockServer    ${Fixtures}/example.json

Try Load JSON MockAnswers
    [Setup]    Init MockServer
    MockServer API    GET    /abce/    status=404
    Load MockAnswers    JSON    ${Fixtures}/example.json    ${Fixtures}/example2.json
    MockServer API    GET    /abce/    status=204

Try Load YAML MockAnswers
    [Setup]    Init MockServer
    MockServer API    DELETE    /my/api/v2/job/    status=404
    Load MockAnswers    YAML    ${Fixtures}/example.yaml    ${Fixtures}/example2.yaml
    MockServer API    DELETE    /my/api/v2/job/    status=412
    MockServer API    DELETE    /my/api/v2/job/    status=204

Try Prepare Answer
    [Setup]    Init MockServer
    Prepare MockAnswer    url=deploy/    ans_body={"status":"ongoing"}    use_up=4
    Prepare MockAnswer    url=deploy/    ans_body={"status":"done"}    ans_status=201
    :FOR    ${i}    IN RANGE    5
    \    ${response}=    MockServer API    GET    /deploy/
    \    Log    ${response}
