from royal.tests.functional import TestBase

PR_ID = 3
PROJECT_NAME = 'TEST_P3'


class Test(TestBase):

    def setUpModels(self):
        from example.ext.sqla.model.project import Project
        self.session.add(Project(id=PR_ID, name=PROJECT_NAME))

    def tearDownModels(self):
        from example.ext.sqla.model.project import Project
        self.session.query(Project).delete()

    def test_project_index(self):
        response = self.app.get('/projects').json
        self.assertIn('items', response)
        self.assertIn('links', response)
        self.assertEqual(len(response['items']), 1)

        project = response['items'][0]
        self.assertEqual(project['id'], PR_ID)
        self.assertEqual(project['name'], PROJECT_NAME)

    def test_project_create(self):
        result = self.app.post('/projects', {'name': 'test_proj'}).json
        new_proj_id = result['id']
        self.app.get('/projects/%s' % new_proj_id)

    def test_project_show(self):
        self.app.get('/projects/999', status=404)

        expected = {'id': PR_ID,
                    'links': {'self': 'http://localhost/projects/%s/' % PR_ID},
                    'name': u'TEST_P3'}
        result = self.app.get('/projects/%s' % PR_ID).json
        self.assertEqual(result, expected)

    def test_project_delete(self):
        self.app.delete('/projects/%s' % PR_ID)
        self.app.delete('/projects/%s' % PR_ID, status=404)

    def test_project_update(self):
        self.app.patch('/projects/999', {'name': 'new_name'}, status=404)
        self.app.patch('/projects/%s' % PR_ID, {'name': 'new_name'})

        expected = {'id': PR_ID,
                    'links': {'self': 'http://localhost/projects/%s/' % PR_ID},
                    'name': u'new_name'}
        result = self.app.get('/projects/%s' % PR_ID).json
        self.assertEqual(result, expected)
