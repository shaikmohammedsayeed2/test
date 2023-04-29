import unittest
from api.home import get_resarch_metrics

class TestMyModule(unittest.TestCase):
    def test_get_resarch_metrics(self):
        # Create a mock SQLAlchemy Session object
        mock_session = Mock(spec=Session)

        # Create some mock data to be returned by the database queries
        mock_patent_count = 5
        mock_poster_demo_count = 10
        mock_conference_count = 15
        mock_journal_count = 20

        # Set up the mock session to return the mock data for each query
        mock_session.query.return_value.filter.return_value.count.side_effect = [
            mock_patent_count,
            mock_poster_demo_count,
            mock_conference_count,
            mock_journal_count
        ]

        # Call the function being tested with the mock lab_id and session
        results = get_resarch_metrics(lab_id=1, db=mock_session)

        # Check that the function returns the expected results
        self.assertEqual(results["patentCount"], mock_patent_count)
        self.assertEqual(results["posterDemoCount"], mock_poster_demo_count)
        self.assertEqual(results["conferencesCount"], mock_conference_count + mock_session.query.return_value.filter.return_value.count.return_value)
        self.assertEqual(results["journalCount"], mock_journal_count)

if __name__ == '__main__':
    unittest.main()
