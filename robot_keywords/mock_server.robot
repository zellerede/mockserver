*** Settings ***
Documentation     Drive and feed the mock server, which is assumed to run.

Library           OperatingSystem
Library           HttpLibrary.HTTP
Library           yaml2json.py

*** Variables ***
${MOCK_URL}    localhost:8000

*** Keywords ***
Init MockServer
    [Arguments]    @{files}
    Delete All MockAnswers
    Load MockAnswers    @{files}

Delete All MockAnswers
    MockServer API    DELETE   /__mock/bulk/

Load MockAnswers
    [Arguments]    @{files}
    :FOR    ${file}    IN    @{files}
    \    ${path}    ${type}=    Split Extension    ${file}
    \    Run Keyword    Create MockAnswers By ${type}   ${file}

Create MockAnswers By JSON
    [Arguments]    ${json}
    ${data}=    Get File    ${json}
    MockServer API    POST   /__mock/bulk/    data=${data}

Create MockAnswers By YAML
    [Arguments]    ${yaml_file}
    ${yaml}=    Get File    ${yaml_file}
    ${yaml}=    Replace Variables    ${yaml}
    ${data}=    Get JSON From YAML    ${yaml}
    MockServer API    POST   /__mock/bulk/    data=${data}

Prepare MockAnswer
    [Arguments]    &{fields}
    ${data}=    Evaluate    json.dumps(${fields})    json
    MockServer API    POST    /__mock/    data=${data}

#
MockServer API
    [Arguments]    ${method}   ${path}    ${data}=${EMPTY}    ${status}=${EMPTY}
    Create Http Context    ${MOCK_URL}
    Run Keyword Unless    """${data}"""==""    Run Keywords
    ...    Set Request Body    ${data}    AND
    ...    Set Request Header    Content-Type    application/json
    Run Keyword Unless    '${status}'==''    Next Request Should Have Status Code    ${status}
    Run Keyword    ${method}    ${path}
    Log Response Status
    ${response}=    Get Response Body
    [Return]    ${response}

