"""Exercise the complete public candidate plan without credentials or network."""
import sys,json,copy,tempfile,collections,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from test_metadata_execution import FakeAPI,REPO
import metadata
from metadata_execution import _MetadataWriter
base=Path(__file__).resolve().parents[1]/'metadata/audits/2026-09-07'
p=json.loads((base/'fleet-plan.json').read_text())
snap=metadata.normalize_snapshot(json.loads((base/'public-before.json').read_text()))
class Fleet:
    def __init__(self):
        self.rows={r['full_name']:copy.deepcopy(r) for r in snap['repositories'] if r['full_name'] in {t['repository'] for t in p['targets']}}
        self.states={}
        for name,row in self.rows.items():
            api=FakeAPI();api.labels=copy.deepcopy(row['labels']);api.issues=copy.deepcopy(row['issues']);api.topics=metadata._current_topics(row)
            self.states[name]=api
    def _run(self,endpoint,**kwargs):
        name='/'.join(endpoint.split('/')[1:3]);row=self.rows[name];suffix=endpoint[len('repos/'+name):]
        if kwargs.get('method','GET')=='GET':
            if not suffix:return {k:row[k] for k in ('id','full_name','default_branch','archived','visibility')}
            if suffix.startswith('/commits/'):return {'sha':metadata._commit_sha(row)}
        return self.states[name]._run('repos/'+REPO+suffix,**kwargs)
    def snapshot(self):
        rows=[]
        for name,row in self.rows.items():
            r=copy.deepcopy(row);a=self.states[name];r.update(labels=copy.deepcopy(a.labels),issues=copy.deepcopy(a.issues),topics={'names':a.topics});rows.append(r)
        return {'repositories':rows}
class FleetTests(unittest.TestCase):
    def test_complete_candidate_apply_verify_repeat_resume_rollback(self):
        a=Fleet()
        with tempfile.TemporaryDirectory() as temp:
            w=_MetadataWriter(a,Path(temp)/'journal',state_dir=Path(temp)/'keys',minimum_write_interval=0)
            self.assertEqual(122,w.apply(p,execute=True)['writes'])
            checked=metadata.verify_plan(p,a.snapshot())
            self.assertTrue(checked['ok'],checked)
            self.assertEqual(0,w.apply(p,execute=True)['writes'])
            self.assertEqual(0,w.apply(p,execute=True,resume=True)['writes'])
            rolled=w.rollback(p,execute=True)
            self.assertEqual([],rolled['conflicts'])
            self.assertEqual(48,rolled['writes'])
            self.assertEqual(74,len(rolled['retained_labels']))
            for name,original in a.rows.items():
                self.assertEqual(metadata._current_topics(original),a.states[name].topics)
                self.assertEqual(original['issues'],a.states[name].issues)

    def test_shared_form_defaults_exist_at_changed_transition_and_after_provision(self):
        import yaml
        root=Path(__file__).resolve().parents[1]
        names=set()
        for form in (root/'.github/ISSUE_TEMPLATE').glob('*.yml'):
            value=yaml.safe_load(form.read_text())
            names.update(value.get('labels',[]))
        self.assertIn('bug',names)
        for row in snap['repositories']:
            before={label['name'] for label in row['labels']}
            self.assertIn('bug',before,row['full_name'])
            operations=next(t['operations'] for t in p['targets'] if t['repository']==row['full_name'])
            after=before|{op['after']['name'] for op in operations if op['kind']=='create_label'}
            self.assertFalse(names-after,(row['full_name'],names-after))

    def test_metadata_workflows_have_read_only_credentials_and_no_secret_inputs(self):
        import yaml
        root=Path(__file__).resolve().parents[1]
        for name in ('metadata-validation.yml','metadata-drift.yml'):
            path=root/'.github/workflows'/name
            raw=path.read_text(); workflow=yaml.load(raw,Loader=yaml.BaseLoader)
            self.assertTrue(set(workflow['permissions']) <= {'contents','issues','pull-requests'})
            self.assertTrue(all(value=='read' for value in workflow['permissions'].values()))
            self.assertNotIn('pull_request_target',workflow['on'])
            self.assertNotIn('secrets.',raw)
            for job in workflow['jobs'].values():
                self.assertNotIn('permissions',job)
                for step in job['steps']:
                    if 'uses' in step:
                        self.assertRegex(step['uses'],r'^[^@]+@[0-9a-f]{40}$')
                    self.assertNotIn('--execute',step.get('run',''))

if __name__=='__main__':
    unittest.main()
