from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from continue_task import scenario


class ScenarioTests(unittest.TestCase):
    def test_reopen_and_continue_with_correction(self):
        with TemporaryDirectory() as tmp:
            result = scenario(Path(tmp)/'demo.sqlite')
        self.assertEqual(result['work']['rev'],2)
        self.assertEqual(result['work']['pending'],['查送达'])
        self.assertEqual(result['stale_index_read'],('known','v2','canonical_fallback'))
        self.assertEqual(result['third_version_permission'][:2],('known',False))
        self.assertEqual(result['resume'],('lookup_delivery','v2'))


if __name__ == '__main__':
    unittest.main()
