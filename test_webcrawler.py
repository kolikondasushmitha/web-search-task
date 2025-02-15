from main import WebCrawler
import unittest
from unittest.mock import patch, MagicMock
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse

class WebCrawlerTests(unittest.TestCase):
    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
            <a href="https://www.external.com/about">External Link</a>
            <a href="https://www.external.com">External Link</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://www.external.com")

        # Assert that 'about' was added to visited URLs
        self.assertIn("https://www.external.com/about", crawler.visited)

    @patch('requests.get')
    def test_crawl_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        # Assertions to check if the error was logged (you'll
        # likely need to set up logging capture in your tests)
    @patch('requests.get')
    def test_crawl_external_link(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
            <a href="https://www.external.com">External Link</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response


    def test_search(self):
        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        # Assert that external links are not added to visited URLs
        self.assertNotIn("https://www.external.com", crawler.visited)
   
   
        crawler.index["page1"] = "This has the keyword"
        crawler.index["page2"] = "No keyword here"

    
        results = crawler.search("keyword")
        self.assertEqual(results, ["page1", "page2"]) 

    def test_search_with_keyword_present(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This page contains the keyword multiple times. Keyword Keyword"
        crawler.index["page2"] = "No keyword here"

        results = crawler.search("keyword")
        self.assertEqual(results, ["page1", "page2"])
    
    def test_search_with_keyword_present_different_case(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This page contains the keyword in lowercase"
        crawler.index["page2"] = "No keyword here"

        results = crawler.search("KEYWORD")
        self.assertEqual(results, ["page1", "page2"])
        
    
    def test_search_with_keyword_not_present(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This page does not contain the keyword"
        crawler.index["page2"] = "No keyword here"

        results = crawler.search("nonexistent")
        self.assertEqual(results, [])
       
        
    
    def test_search_with_keyword_present_multiple_urls(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This page contains the keyword"
        crawler.index["page2"] = "This page also contains the keyword"

        results = crawler.search("keyword")
        self.assertEqual(results, ["page1", "page2"])
        

    def test_search_with_empty_index(self):
        crawler = WebCrawler()
        results = crawler.search("keyword")
        self.assertEqual(results, [])
    

    def test_search_with_empty_keyword(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This page contains the keyword"
        crawler.index["page2"] = "No keyword here"

        results = crawler.search("")
        self.assertEqual(results, ['page1', 'page2'])
        

    def test_search_with_whitespace_keyword(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This page contains the keyword"
        crawler.index["page2"] = "No keyword here"

        results = crawler.search("   ")
        self.assertEqual(results, []) 

    @patch('sys.stdout')
    def test_print_results(self, mock_stdout):
        crawler = WebCrawler()
        crawler.print_results(["https://test.com/result"])

        # Assert that the output was captured correctly by mock_stdout

if __name__ == "__main__":
    unittest.main()  # Run unit tests
    