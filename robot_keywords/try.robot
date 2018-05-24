*** Settings ***
Documentation    Tests assume MockServer is running on localhost:8000
...              If not, issue `manage.py runserver`.
Resource      mock_server.robot

*** Variables ***
${mockserver_ip}    localhost:8000

*** Test Cases ***
Try Init Without Parameters
    Init MockServer

Try Init With Json
    Init MockServer    ${mockserver_ip}    ${CURDIR}/../example.json

Try Load MockAnswers
    [Setup]    Init MockServer
    Load MockAnswers JSONs    ${CURDIR}/../example.json    ${CURDIR}/../example2.json

Try Prepare Answer
    [Setup]    Init MockServer
    Prepare MockAnswer    url=deploy/    ans_body={"status":"ongoing"}    use_up=4
    Prepare MockAnswer    url=deploy/    ans_body={"status":"done"}    ans_status=201
    :FOR    ${i}    IN RANGE    5
    \    ${response}=    MockServer API    GET    /deploy/
    \    Log    ${response}
