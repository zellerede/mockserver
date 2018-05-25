Yet Another Mock API Server
===========================

Run in docker
-------------

#### HTTP
    docker run -p 80:8000 -d zellerede/mockserver
#### HTTPS
    docker run -p 443:443 -e HTTPS=True -d zellerede/mockserver

Set up on own machine
---------------------

    pip install django djangorestframework django-url-filter django-sslserver
    git clone https://github.com/zellerede/mockserver.git
    cd mockserver

#### Set up database
Create/adjust the SQlite3 database by the `migrate` command, then run unittests to see if all works as intended:

    python manage.py migrate
    python manage.py test

#### Start HTTP server
    python manage.py runserver
or, for external reachability,

    python manage.py runserver 0.0.0.0:8000

#### Start HTTPS server
    python manage.py runsslserver 0.0.0.0:443

Usage
-----

For the following examples, set the environment variable `MS` to the actual base URL where Mock Server is listening. E.g.

    export MS="localhost:8000"
For HTTPS, as the certificates are self signed, the curl commands require additional `-k` option. So that, in that case, set

    export MS="-k https://localhost" 

#### Manage mock answers
##### From django rest's webpage
Check out url `localhost:8000/__mock/` in your browser. (Use the actual address and port of the running Mock Server.)

You can _post_ a new mock answer record there by typing in the values for the fields. All fields are optional, though the `url` should be given.

**Note:** All answer bodies must be in *valid json* format.

The mock answers preset this way can also be tested in the browser: 
Say, a record with `url`: `abc/` and `ans_body`: `"success"` was posted, then getting the path `/abc/` should show the json string `"success"` as result.

##### From command line
    curl $MS/__mock/
    curl -v $MS/abc/
    curl -X POST -d "url=abc/&ans_body=\"success\"" $MS/__mock/
    curl -v $MS/abc/

Note that records can also be posted/patched in _json_ format, using header parameter `-H "content-type: application/json"` with curl.

##### Retrieve request details
The mock answer records also remember the *query parameters* and *request body* of the last handled request.
The **id** of a record is returned upon creation. After its mock happened, `curl $MS/__mock/`**id** will return with the details of the actual request that the mock server received.

The records can also be searched by `url` and `req_method`, e.g. `curl $MS/__mock/?url=abc/&req_method=PATCH`.

##### Bulk operations
Bulk creation, deletion and partial update are supported, and can be achieved either on webpage, or by curl of `/__mock/bulk/`, using possibly filters for fields `url` and `req_method`.

     curl -X POST -d "@example.json" -H "content-type: application/json" $MS/__mock/bulk/
     curl -X DELETE $MS/__mock/bulk/
     curl -X DELETE $MS/__mock/bulk/?req_method=POST
     curl -X PATCH -d "ans_status=402" $MS/__mock/bulk/
     curl -X PATCH -d "ans_status=500" $MS/__mock/bulk/?url__icontains=error
     
##### Various answers to same request
The field `use_up` can be set to an integer to indicate how many times the answer given in the record should be used. When set, `use_up` will simply decrease until reaches `0` when the record will be deleted and a next record with same url+method can act.

    curl -X POST -d "url=poll/&ans_status=404&use_up=2" $MS/__mock/
    curl -X POST -d "url=poll/&ans_body=\"appeared\"&use_up=1" $MS/__mock/
    curl -X POST -d "url=poll/&ans_body=\"done\"" $MS/__mock/
    curl -v $MS/poll/   # 404
    curl -v $MS/poll/   # 404
    curl -v $MS/poll/   # appeared
    curl -v $MS/poll/   # done
    curl -v $MS/poll/   # done

