"""Exercise the complete public candidate plan without credentials or network."""
import sys,json,copy,tempfile,collections,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from test_metadata_execution import FakeAPI,REPO
import metadata
from metadata_execution import _MetadataWriter
base=Path(__file__).resolve().parents[1]/'metadata/audits/2026-09-08'
p=json.loads((base/'fleet-plan.json').read_text())
snap=metadata.normalize_snapshot(json.loads((Path(__file__).resolve().parent/'fixtures/metadata-rollout-20260908.json').read_text()))
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
            self.assertEqual(109,w.apply(p,execute=True)['writes'])
            checked=metadata.verify_plan(p,a.snapshot())
            self.assertTrue(checked['ok'],checked)
            from metadata_drift import report
            root=Path(__file__).resolve().parents[1]
            drift=report(metadata.read_document(root/'metadata/repositories.yml'),
                         metadata.read_document(root/'labels.yml'),a.snapshot())
            self.assertTrue(drift['ok'],drift)
            self.assertEqual(0,w.apply(p,execute=True)['writes'])
            self.assertEqual(0,w.apply(p,execute=True,resume=True)['writes'])
            rolled=w.rollback(p,execute=True)
            self.assertEqual([],rolled['conflicts'])
            self.assertEqual(55,rolled['writes'])
            self.assertEqual(54,len(rolled['retained_labels']))
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

    def test_scheduled_workflows_check_out_only_workspace_relative_consumers(self):
        """actions/checkout rejects any `path` outside $GITHUB_WORKSPACE.

        The scheduled drift job previously passed `${{ runner.temp }}/...` as
        the checkout path, which fails the whole job before any report runs.
        Also assert that every scheduled consumer lock corresponds to the
        ledger's listed consumers, so a checkout cannot silently drift away
        from the set the validator actually reads.
        """
        import yaml
        root=Path(__file__).resolve().parents[1]
        listed={row['repository'].rsplit('/',1)[1] for row in
                json.loads((root/'metadata/standards-adoption.json').read_text())['consumers']}
        checked=set()
        for name in ('metadata-validation.yml','metadata-drift.yml'):
            workflow=yaml.load((root/'.github/workflows'/name).read_text(),Loader=yaml.BaseLoader)
            for job in workflow['jobs'].values():
                for step in job['steps']:
                    path=step.get('with',{}).get('path')
                    if path is None:
                        continue
                    self.assertNotIn('runner.temp',path,name)
                    self.assertFalse(path.startswith('/'),name)
                    self.assertNotIn('..',path.split('/'),name)
                    checked.add(path.rsplit('/',1)[1])
        self.assertTrue(checked <= listed, checked-listed)

    def test_drift_job_reports_every_signal_even_when_the_first_check_fails(self):
        """One failing report must not hide the others.

        `metadata_drift.py` intentionally exits nonzero when it finds drift.
        Without `if: always()` the default step gating would skip the
        standards-adoption check after it, so a scheduled run would reveal
        only the first signal. The job stays red because the drift step keeps
        its exit status; it just must not mask the remaining checks.
        """
        import yaml
        root=Path(__file__).resolve().parents[1]
        workflow=yaml.load((root/'.github/workflows/metadata-drift.yml').read_text(),Loader=yaml.BaseLoader)
        steps=[step for job in workflow['jobs'].values() for step in job['steps']]
        runs=[i for i,step in enumerate(steps) if 'run' in step]
        self.assertTrue(runs,'the drift job must run a check')
        drift=max(i for i in runs if 'metadata_drift.py' in steps[i]['run'])
        later=[steps[i] for i in runs if i>drift]
        self.assertTrue(later,'expected a check after the drift report')
        for step in later:
            self.assertEqual('always()',step.get('if'),step.get('name'))

    def test_validation_suite_reads_the_checked_out_consumers(self):
        """The credential-free suite must see the consumer locks it needs.

        `test_standards_adoption` falls back to the checkout's parent when
        STANDARDS_CONSUMER_ROOT is unset. The hosted consumer checkouts live
        at `<workspace>/consumers`, so the discovery step must point there;
        otherwise the suite errors out before asserting anything.
        """
        import yaml
        root=Path(__file__).resolve().parents[1]
        workflow=yaml.load((root/'.github/workflows/metadata-validation.yml').read_text(),Loader=yaml.BaseLoader)
        steps=[step for job in workflow['jobs'].values() for step in job['steps']]
        discover=[step for step in steps if 'run' in step and 'unittest discover' in step['run']]
        self.assertEqual(1,len(discover),'expected exactly one suite step')
        env=discover[0].get('env',{})
        self.assertIn('STANDARDS_CONSUMER_ROOT',env)
        self.assertIn('github.workspace',env['STANDARDS_CONSUMER_ROOT'])

if __name__=='__main__':
    unittest.main()
