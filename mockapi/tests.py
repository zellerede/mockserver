import json

from django.test import TestCase, Client

client = Client()

#
class TestMockDataManipulation(TestCase):
    
    def test_get_mock__empty(self):
        response = client.get('/__mock/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [])
    
    def test_add_mock(self):
        mock_ans = {
            'url': 'sas/',
            'ans_body': '[2,3,4]'
        }
        response = client.post('/__mock/', mock_ans)
        self.assertEqual(response.status_code, 201)

        response = client.get('/__mock/1/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['url'], 'sas/')
    
    def test_add_polling_mock(self):
        mock_ans = {
            'url': 'sas/',
            'ans_body': '[1,2,3,4]',
            'use_up': 4
        }
        response = client.post('/__mock/', mock_ans)
        self.assertEqual(response.status_code, 201)

        mock_ans = {
            'url': 'sas/',
            'ans_body': '[5,6,7,"..."]'
        }
        response = client.post('/__mock/', mock_ans)
        self.assertEqual(response.status_code, 201)

        response = client.get('/__mock/1/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['use_up'], 4)
        
        response = client.get('/__mock/2/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['use_up'], None)
        self.assertEqual(content['url'], 'sas/')
        self.assertEqual(content['ans_body'], '[5,6,7,"..."]')

#
class TestBulkMockData(TestCase):
    
    fixtures = ['fixtures/mock_answers.json']
    
    def test_bulk_delete_all(self):
        response = client.delete('/__mock/bulk/')
        self.assertEqual(response.status_code, 200)
        
        response = client.get('/__mock/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [])
    
    def test_bulk_delete_filtered(self):
        response = client.delete('/__mock/bulk/?url=sas/')
        self.assertEqual(response.status_code, 200)
        
        response = client.get('/__mock/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual( len(json.loads(response.content)), 2 )
    
    def test_bulk_patch_filtered(self):
        data = {'ans_status': 402}
        response = client.patch('/__mock/bulk/?url=sas/error/',
                                json.dumps(data),
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)
        
        response = client.get('/__mock/?url=sas/error/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual( content[0]['ans_status'], 402 )
        self.assertEqual( content[1]['ans_status'], 402 )
    
    def test_bulk_post(self):
        data = [{'url': 'x/yy/', 'ans_body': '[]'},
                {'url': 'yy/z/', 'ans_status': 500},
                {'url': 'yy/z/', 'req_method': 'PUT'}]
        response = client.post('/__mock/bulk/',
                                json.dumps(data),
                                content_type="application/json")
        self.assertEqual(response.status_code, 201)
        
        response = client.get('/__mock/?url__contains=yy/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual( content[0]['url'], 'x/yy/' )
        self.assertEqual( content[1]['ans_status'], 500 )
        self.assertEqual( content[2]['req_method'], 'PUT' )

#
class TestMockAnswering(TestCase):
    
    fixtures = ['fixtures/mock_answers.json']
    
    def test_get_unknown(self):
        response = client.get('/unknown/?with=params')
        self.assertEqual(response.status_code, 404)
    
    def test_get_mocked_simple(self):
        response = client.get('/sas/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [2,3,4])
    
    def test_get_mocked_error(self):
        response = client.get('/sas/error/')
        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.content, '"oh boy"')
    
    def test_delete_mocked_error(self):
        response = client.delete('/sas/error/')
        self.assertEqual(response.status_code, 597)
        self.assertEqual(response.content, '"fatal"')
    
    def test_get_mocked_with_params(self):
        response = client.get('/sas/?my=parameter&is=nice')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [2,3,4])
        
        response = client.get('/__mock/?url=sas/&req_method=GET')
        content = json.loads(response.content)
        self.assertJSONEqual( content[0]['query_params'],
                          {'my':'parameter', 'is':'nice'} )
    
    def test_post_mocked(self):
        data = {'many': {'lines': 'full', 'with': 'data'}, 'in': ['a', 'dict']}
        response = client.post('/sas/', json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        
        response = client.get('/__mock/?url=sas/&req_method=POST')
        content = json.loads(response.content)
        self.assertJSONEqual( content[0]['req_body'], data )
    
class TestPollingMockAnswers(TestCase):
    
    fixtures = ['fixtures/mock_polling_answers.json']
    
    def test_get_polling(self):
        for _ in range(4):
            response = client.get('/sas/?a=b')
            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual( response.content, [1,2,3,4] )
        for _ in range(2):
            response = client.get('/sas/?x=y')
            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual( response.content, [5,6,7,"..."] )
    
