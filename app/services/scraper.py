import requests
import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup


class FinancialScraper:

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def get_financial_tips(self) -> List[Dict[str, str]]:

        tips = [
            {
                "title": "Start an Emergency Fund",
                "content": "Build an emergency fund with 3-6 months of expenses. This protects you from unexpected financial hardships.",
            },
            {
                "title": "Track Your Spending",
                "content": "Monitor all expenses to understand where your money goes and identify areas to cut back.",
            },
            {
                "title": "Create a Budget",
                "content": "Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings and debt repayment.",
            },
            {
                "title": "Automate Your Savings",
                "content": "Set up automatic transfers to savings on payday to make saving effortless.",
            },
            {
                "title": "Reduce Debt",
                "content": "Prioritize paying off high-interest debt first to save money on interest payments.",
            },
            {
                "title": "Invest Early",
                "content": "Start investing in diversified portfolios early to benefit from compound growth.",
            },
        ]
        return tips

    def scrape_exchange_rates(self, base_currency: str = "USD") -> Optional[Dict[str, float]]:
        fallback_rates = {
            "USD": 1.0,
            "EUR": 0.92,
            "GBP": 0.79,
            "JPY": 149.5,
            "CAD": 1.36,
            "AUD": 1.53,
            "CHF": 0.88,
            "CNY": 7.08,
        }

        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("rates", fallback_rates)
        except Exception as e:
            print(f"Exchange rate scraping failed: {e}. Using fallback rates.")
            return fallback_rates

    def scrape_financial_quotes(self) -> List[Dict[str, str]]:
        quotes = [
            {
                "text": "An investment in knowledge pays the best interest.",
                "author": "Benjamin Franklin",
            },
            {
                "text": "Do not save what is left after spending; instead spend what is left after saving.",
                "author": "Warren Buffett",
            },
            {
                "text": "Money is a great servant but a bad master.",
                "author": "Francis Bacon",
            },
            {
                "text": "The best time to plant a tree was 20 years ago. The second best time is now.",
                "author": "Chinese Proverb",
            },
            {
                "text": "Financial peace isn't the acquisition of stuff. It's peace of mind.",
                "author": "Dave Ramsey",
            },
        ]
        return quotes

    def extract_numbers_from_text(self, text: str) -> List[float]:
        pattern = r"-?\d+\.?\d*"
        matches = re.findall(pattern, text)
        return [float(match) for match in matches if match and match != "."]

    def sanitize_html(self, html: str) -> str:
        try:
            soup = BeautifulSoup(html, "html5lib")
            for tag in soup(["script", "style"]):
                tag.decompose()
            text = soup.get_text()
            text = " ".join(text.split())
            return text
        except Exception as e:
            print(f"HTML sanitization failed: {e}")
            return html
