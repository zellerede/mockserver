*** Settings ***
Documentation     Drive and feed the mock server, which is assumed to run.

Library           OperatingSystem
Library           HttpLibrary.HTTP

*** Keywords ***
Init MockServer
    [Arguments]    ${url}=localhost:8000    @{jsons}
    Set Global Variable    ${mock_url}     ${url}
    Delete All MockAnswers
    Load MockAnswers JSONs    @{jsons}

Delete All MockAnswers
    MockServer API    DELETE   /__mock/bulk/

Load MockAnswers JSONs
    [Arguments]    @{jsons}
    :FOR    ${json}    IN    @{jsons}
    \    Create MockAnswers By    ${json}

Create MockAnswers By
    [Arguments]    ${json}
    ${data}=    Get File    ${json}
    MockServer API    POST   /__mock/bulk/    data=${data}

Prepare MockAnswer
    [Arguments]    &{fields}
    ${data}=    Evaluate    json.dumps(${fields})    json
    MockServer API    POST    /__mock/    data=${data}

MockServer API
    [Arguments]    ${method}   ${path}    ${data}=${EMPTY}    ${status}=${EMPTY}
    Create Http Context    ${mock_url}
    Run Keyword Unless    """${data}"""==""    Run Keywords
    ...    Set Request Body    ${data}    AND
    ...    Set Request Header    Content-Type    application/json
    Run Keyword Unless    '${status}'==''    Next Request Should Have Status Code    ${status}
    Run Keyword    ${method}    ${path}
    Log Response Status
    ${response}=    Get Response Body
    [Return]    ${response}

