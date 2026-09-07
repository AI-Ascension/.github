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

if __name__=='__main__':
    unittest.main()
