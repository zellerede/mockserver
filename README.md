Yet Another Mock API Server
===========================

Installation
------------
    pip install djangorestframework
    git clone https://github.com/zellerede/mockserver.git
    cd mockserver

#### Set up database
Issue from this directory:

    python manage.py migrate

#### Start server
    python manage.py runserver
or, for external reachability,

    python manage.py runserver 0.0.0.0:8000

Usage
-----

#### Manage mock answers
##### From django rest's webpage
Check out url `localhost:8000/__mock/` in your browser.
You can _post_ new mock answer records.

**Note:** All answer bodies must be in *valid json* format.

The mock answers preset this way can also be tested in the browser: 
Say, a record with `url`: `abc/` and `ans_body`: `"success"` was posted, then the url `localhost:8000/abc/` should show the json string `"success"` as result.

##### From command line
    curl localhost:8000/__mock/
    curl -v localhost:8000/abc/
    curl -X POST -d "url=abc/&ans_body=\"success\"" localhost:8000/__mock/
    curl -v localhost:8000/abc/

Note that records can also be posted/patched in _json_ format, using header parameter `-H "content-type: application/json"` with curl.

##### Retrieve request details
The mock answer records also remember the *query parameters* and *request body* of the last handled request.
The **id** of a record is returned upon creation. After its mock happened, `curl localhost:8000/__mock/`**id** will return with the details of the actual request that the mock server received.

The records can also be searched by `url` and `req_method`, e.g. `curl localhost:8000/__mock/?url=abc/&req_method=PATCH`.

##### Bulk operations
Bulk creation, deletion and partial update are supported, and can be achieved either on webpage, or by curl of `localhost:8000/__mock/bulk/`, using possibly filters for fields `url` and `req_method`.

     curl -X POST -d "@example.json" -H "content-type: application/json" localhost:8000/__mock/bulk/
     curl -X DELETE localhost:8000/__mock/bulk/
     curl -X DELETE localhost:8000/__mock/bulk/?req_method=POST
     curl -X PATCH -d "ans_status=402" localhost:8000/__mock/bulk/
     curl -X PATCH -d "ans_status=500" localhost:8000/__mock/bulk/?url__icontains=error
     
##### Various answers to same request
The field `use_up` can be set to an integer to indicate how many times the answer given in the record should be used. When set, `use_up` will simply decrease until reaches `0` when the record will be deleted and a next record with same url+method can act.

    curl -X POST -d "url=poll/&ans_status=404&use_up=2" localhost:8000/__mock/
    curl -X POST -d "url=poll/&ans_body=\"appeared\"&use_up=1" localhost:8000/__mock/
    curl -X POST -d "url=poll/&ans_body=\"done\"" localhost:8000/__mock/
    curl -v localhost:8000/poll/   # 404
    curl -v localhost:8000/poll/   # 404
    curl -v localhost:8000/poll/   # appeared
    curl -v localhost:8000/poll/   # done
    curl -v localhost:8000/poll/   # done

