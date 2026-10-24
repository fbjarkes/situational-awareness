import unittest

import knowledge


class KnowledgeTests(unittest.TestCase):
    def test_bundle_is_conformant(self):
        concepts = knowledge.load_concepts()
        self.assertTrue(concepts)
        self.assertTrue(all(c["meta"]["type"] for c in concepts.values()))
        self.assertFalse(any(p.endswith(("/index.md", "/log.md")) for p in concepts))

    def test_breadth_retrieval_follows_links_and_stays_in_section(self):
        found = {k["path"]: k["relation"] for k in
                 knowledge.retrieve(knowledge.load_concepts(), "breadth", ("INDEX:MMOH", "INDEX:MMOF"))}
        self.assertEqual(found["/breadth/mmof.md"], "metric")
        self.assertEqual(found["/breadth/extreme-low-breadth.md"], "related")
        self.assertEqual(found["/references/breadth-crossing-study.md"], "linked")
        self.assertNotIn("/sectors/relative-strength.md", found)


if __name__ == "__main__":
    unittest.main()
