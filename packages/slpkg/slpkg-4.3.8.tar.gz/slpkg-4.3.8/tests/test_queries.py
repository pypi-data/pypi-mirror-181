import unittest
from slpkg.queries import SBoQueries


class TestSBoQueries(unittest.TestCase):

    def setUp(self):
        self.query = SBoQueries('slpkg')

    def test_slackbuild(self):
        self.assertEqual('slpkg', self.query.slackbuild())

    def test_location(self):
        self.assertEqual('system', self.query.location())

    def test_sources(self):
        self.assertEqual('https://gitlab.com/dslackw/slpkg/-/archive'
                         '/4.3.0/slpkg-4.3.0.tar.gz', self.query.sources())

    def test_requires(self):
        self.assertEqual(['SQLAlchemy'], self.query.requires())

    def test_version(self):
        self.assertEqual('4.3.0', self.query.version())

    def test_checksum(self):
        self.assertListEqual(['ab03d0543b74abfce92287db740394c4'],
                             self.query.checksum())

    def test_files(self):
        self.assertEqual(5, len(self.query.files().split()))

    def test_description(self):
        self.assertEqual('slpkg (Slackware Packaging Tool)',
                         self.query.description())

    def test_names(self):
        self.assertIn('slpkg', self.query.names())


if __name__ == '__main__':
    unittest.main()
