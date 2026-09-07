import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import update_telemetry as t


class TelemetryTests(unittest.TestCase):
    def setUp(self):
        self.snapshot=json.loads(t.DATA.read_text(encoding='utf-8'))

    def test_same_data_different_time_and_order_writes_nothing(self):
        fresh=copy.deepcopy(self.snapshot)
        fresh['collected_at']='2099-01-01T00:00:00+00:00'
        fresh['repositories'].reverse()
        with tempfile.TemporaryDirectory() as folder:
            file=Path(folder)/'telemetry.json'; file.write_text(json.dumps(self.snapshot))
            before=file.read_bytes()
            with patch.object(t,'DATA',file),patch.object(t,'fetch',return_value=fresh),patch.object(t,'render') as render:
                self.assertFalse(t.update())
                render.assert_not_called()
            self.assertEqual(before,file.read_bytes())

    def test_real_change_updates_snapshot(self):
        fresh=copy.deepcopy(self.snapshot)
        fresh['stars_on_public_original_repositories']+=1
        with tempfile.TemporaryDirectory() as folder:
            file=Path(folder)/'telemetry.json'; file.write_text(json.dumps(self.snapshot))
            with patch.object(t,'DATA',file),patch.object(t,'fetch',return_value=fresh),patch.object(t,'render') as render:
                self.assertTrue(t.update()); render.assert_called_once_with(fresh)
            self.assertEqual(fresh,json.loads(file.read_text(encoding='utf-8')))

    def test_fetch_failure_preserves_snapshot(self):
        with tempfile.TemporaryDirectory() as folder:
            file=Path(folder)/'telemetry.json'; file.write_text(json.dumps(self.snapshot))
            before=file.read_bytes()
            with patch.object(t,'DATA',file),patch.object(t,'fetch',side_effect=OSError('network')),patch.object(t,'render') as render:
                with self.assertRaises(OSError): t.update()
                render.assert_not_called()
            self.assertEqual(before,file.read_bytes())

    def repo(self,name,fork=False,stars=2):
        return {'name':name,'owner':{'login':t.USER},'fork':fork,'private':False,'stargazers_count':stars}

    def test_pagination_and_fork_filter(self):
        pages=[{'login':t.USER,'public_repos':101},[self.repo(str(i)) for i in range(100)],[self.repo('fork',True,1000)]]
        with patch.object(t,'get',side_effect=pages) as get:
            data=t.fetch()
        self.assertEqual(get.call_count,3)
        self.assertEqual(data['public_repositories_including_forks'],101)
        self.assertEqual(data['public_original_repositories'],100)
        self.assertEqual(data['stars_on_public_original_repositories'],200)

    def test_incomplete_duplicate_or_invalid_data_rejected(self):
        for count,batch in [(2,[self.repo('one')]),(2,[self.repo('same'),self.repo('same')]),(1,[self.repo('bad',stars=None)])]:
            with self.subTest(batch=batch),patch.object(t,'get',side_effect=[{'login':t.USER,'public_repos':count},batch]):
                with self.assertRaises(ValueError): t.fetch()

    def test_valid_empty_account_is_zero(self):
        with patch.object(t,'get',side_effect=[{'login':t.USER,'public_repos':0},[]]):
            data=t.fetch()
        self.assertEqual(data['public_repositories_including_forks'],0)
        self.assertEqual(data['stars_on_public_original_repositories'],0)

    def test_render_is_byte_identical_to_current_artwork(self):
        with tempfile.TemporaryDirectory() as folder:
            import build_assets
            with patch.object(build_assets,'OUT',Path(folder)):
                t.render(self.snapshot)
            for name in ['telemetry.svg','telemetry-mobile.svg']:
                self.assertEqual((Path(folder)/name).read_bytes(),(t.DATA.parent/name).read_bytes())

if __name__=='__main__': unittest.main()
