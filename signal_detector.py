"""
Signal Detection Module - Monitors sources for infrastructure chokepoint signals
"""
import asyncio
import aiohttp
import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class InfrastructureSignal:
    """Represents a detected infrastructure chokepoint signal"""
    title: str
    description: str
    source: str
    sector: str
    url: str
    timestamp: datetime
    
    # Breadcrumbs that triggered detection
    breadcrumbs: List[str]
    
    # Raw scores (0-100)
    inevitability_score: float
    moat_score: float
    timing_score: float
    
    # Composite score
    total_score: float
    
    # Classification
    toll_mechanism: str
    early_movers: List[str]

class SignalDetector:
    def __init__(self, config: Dict):
        self.config = config
        self.sources = config.get('signal_sources', {})
        self.sectors = config.get('sectors', {})
        self.detection_patterns = config.get('detection_patterns', {})
        
    async def run_detection_cycle(self) -> List[InfrastructureSignal]:
        """Run one cycle of signal detection across all sources"""
        signals = []
        
        tasks = []
        
        # HackerNews
        if self.sources.get('hackernews', {}).get('enabled'):
            tasks.append(self._scan_hackernews())
        
        # GitHub Trending
        if self.sources.get('github', {}).get('enabled'):
            tasks.append(self._scan_github_trending())
        
        # Reddit
        if self.sources.get('reddit', {}).get('enabled'):
            tasks.append(self._scan_reddit())
        
        # ArXiv
        if self.sources.get('arxiv', {}).get('enabled'):
            tasks.append(self._scan_arxiv())
        
        # Gather all results
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Detection error: {result}")
            elif result:
                signals.extend(result)
        
        # Filter and score signals
        qualified_signals = []
        for signal in signals:
            if signal.total_score >= self.config.get('min_signal_score', 7.0):
                qualified_signals.append(signal)
        
        # Sort by score
        qualified_signals.sort(key=lambda x: x.total_score, reverse=True)
        
        return qualified_signals
    
    async def _scan_hackernews(self) -> List[InfrastructureSignal]:
        """Scan HackerNews for infrastructure signals"""
        signals = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get top stories
                async with session.get(
                    'https://hacker-news.firebaseio.com/v0/topstories.json',
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status != 200:
                        return signals
                    story_ids = await resp.json()
                
                # Check top 30 stories
                for story_id in story_ids[:30]:
                    try:
                        async with session.get(
                            f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json',
                            timeout=aiohttp.ClientTimeout(total=5)
                        ) as resp:
                            if resp.status != 200:
                                continue
                            story = await resp.json()
                            
                            if not story or 'title' not in story:
                                continue
                            
                            # Analyze story
                            signal = self._analyze_content(
                                title=story.get('title', ''),
                                text=story.get('text', ''),
                                url=story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                                source='HackerNews'
                            )
                            
                            if signal:
                                signals.append(signal)
                    
                    except Exception as e:
                        logger.debug(f"Error fetching HN story {story_id}: {e}")
                        continue
        
        except Exception as e:
            logger.error(f"Error scanning HackerNews: {e}")
        
        return signals
    
    async def _scan_github_trending(self) -> List[InfrastructureSignal]:
        """Scan GitHub trending for infrastructure signals"""
        signals = []
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc&per_page=30',
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status != 200:
                        return signals
                    
                    data = await resp.json()
                    repos = data.get('items', [])
                    
                    for repo in repos:
                        signal = self._analyze_content(
                            title=repo.get('name', ''),
                            text=repo.get('description', ''),
                            url=repo.get('html_url', ''),
                            source='GitHub'
                        )
                        
                        if signal:
                            signals.append(signal)
        
        except Exception as e:
            logger.error(f"Error scanning GitHub: {e}")
        
        return signals
    
    async def _scan_reddit(self) -> List[InfrastructureSignal]:
        """Scan Reddit for infrastructure signals"""
        signals = []
        subreddits = self.sources.get('reddit', {}).get('subreddits', [])
        
        try:
            async with aiohttp.ClientSession() as session:
                for subreddit in subreddits:
                    try:
                        async with session.get(
                            f'https://www.reddit.com/r/{subreddit}/hot.json?limit=25',
                            headers={'User-Agent': 'TollboothSeeker/1.0'},
                            timeout=aiohttp.ClientTimeout(total=10)
                        ) as resp:
                            if resp.status != 200:
                                continue
                            
                            data = await resp.json()
                            posts = data.get('data', {}).get('children', [])
                            
                            for post in posts:
                                post_data = post.get('data', {})
                                
                                signal = self._analyze_content(
                                    title=post_data.get('title', ''),
                                    text=post_data.get('selftext', ''),
                                    url=f"https://reddit.com{post_data.get('permalink', '')}",
                                    source=f'Reddit/{subreddit}'
                                )
                                
                                if signal:
                                    signals.append(signal)
                    
                    except Exception as e:
                        logger.debug(f"Error scanning r/{subreddit}: {e}")
                        continue
        
        except Exception as e:
            logger.error(f"Error scanning Reddit: {e}")
        
        return signals
    
    async def _scan_arxiv(self) -> List[InfrastructureSignal]:
        """Scan ArXiv for infrastructure signals"""
        signals = []
        categories = self.sources.get('arxiv', {}).get('categories', [])
        
        try:
            async with aiohttp.ClientSession() as session:
                for category in categories:
                    try:
                        query = f'cat:{category}'
                        url = f'http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results=20'
                        
                        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                            if resp.status != 200:
                                continue
                            
                            content = await resp.text()
                            
                            # Simple XML parsing (in production, use proper XML parser)
                            entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
                            
                            for entry in entries:
                                title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
                                summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
                                link_match = re.search(r'<id>(.*?)</id>', entry)
                                
                                if title_match and summary_match:
                                    signal = self._analyze_content(
                                        title=title_match.group(1).strip(),
                                        text=summary_match.group(1).strip(),
                                        url=link_match.group(1).strip() if link_match else '',
                                        source=f'ArXiv/{category}'
                                    )
                                    
                                    if signal:
                                        signals.append(signal)
                    
                    except Exception as e:
                        logger.debug(f"Error scanning ArXiv {category}: {e}")
                        continue
        
        except Exception as e:
            logger.error(f"Error scanning ArXiv: {e}")
        
        return signals
    
    def _analyze_content(self, title: str, text: str, url: str, source: str) -> Optional[InfrastructureSignal]:
        """Analyze content to determine if it's an infrastructure signal"""
        combined_text = f"{title} {text}".lower()
        
        # Check if this is infrastructure-related
        breadcrumbs = []
        
        # Look for detection patterns
        for pattern_type, keywords in self.detection_patterns.items():
            for keyword in keywords:
                if keyword.lower() in combined_text:
                    breadcrumbs.append(f"{pattern_type}: {keyword}")
        
        # Need at least 2 breadcrumbs to be interesting
        if len(breadcrumbs) < 2:
            return None
        
        # Determine sector
        sector = self._classify_sector(combined_text)
        
        # Calculate scores
        inevitability = self._calculate_inevitability(combined_text, breadcrumbs)
        moat = self._calculate_moat_potential(combined_text, breadcrumbs)
        timing = self._calculate_timing(combined_text, breadcrumbs)
        
        # Calculate weighted total score
        weights = self.config.get('scoring_weights', {})
        total_score = (
            inevitability * weights.get('inevitability', 0.4) +
            moat * weights.get('moat_potential', 0.35) +
            timing * weights.get('timing_window', 0.25)
        ) * 10  # Scale to 0-10
        
        # Determine toll mechanism
        toll_mechanism = self._identify_toll_mechanism(combined_text)
        
        # Extract early movers (simplified)
        early_movers = self._extract_early_movers(combined_text)
        
        return InfrastructureSignal(
            title=title[:200],
            description=text[:500] if text else title[:500],
            source=source,
            sector=sector,
            url=url,
            timestamp=datetime.now(),
            breadcrumbs=breadcrumbs[:10],
            inevitability_score=inevitability,
            moat_score=moat,
            timing_score=timing,
            total_score=total_score,
            toll_mechanism=toll_mechanism,
            early_movers=early_movers
        )
    
    def _classify_sector(self, text: str) -> str:
        """Classify content into a sector"""
        sector_scores = {}
        
        for sector_name, sector_config in self.sectors.items():
            keywords = sector_config.get('keywords', [])
            weight = sector_config.get('weight', 1.0)
            
            score = sum(1 for kw in keywords if kw.lower() in text)
            sector_scores[sector_name] = score * weight
        
        if not sector_scores or max(sector_scores.values()) == 0:
            return 'General'
        
        return max(sector_scores, key=sector_scores.get)
    
    def _calculate_inevitability(self, text: str, breadcrumbs: List[str]) -> float:
        """Calculate inevitability score (0-100)"""
        score = 50.0  # Base score
        
        # Boost for adoption signals
        adoption_keywords = ['mandatory', 'required', 'standard', 'everyone', 'industry adoption']
        score += sum(10 for kw in adoption_keywords if kw in text)
        
        # Boost for pain points
        pain_keywords = ['frustrating', 'difficult', 'need better', 'lack of']
        score += sum(5 for kw in pain_keywords if kw in text)
        
        # Boost based on breadcrumb count
        score += len(breadcrumbs) * 3
        
        return min(score, 100.0)
    
    def _calculate_moat_potential(self, text: str, breadcrumbs: List[str]) -> float:
        """Calculate moat potential score (0-100)"""
        score = 50.0
        
        # Boost for moat indicators
        moat_keywords = ['network effects', 'switching costs', 'protocol', 'standard', 'data advantage']
        score += sum(15 for kw in moat_keywords if kw in text)
        
        # Boost for funding/validation
        funding_keywords = ['series a', 'series b', 'funding', 'investment']
        score += sum(10 for kw in funding_keywords if kw in text)
        
        return min(score, 100.0)
    
    def _calculate_timing(self, text: str, breadcrumbs: List[str]) -> float:
        """Calculate timing window score (0-100)"""
        score = 50.0
        
        # Boost for early-stage indicators
        early_keywords = ['emerging', 'new', 'early', 'beta', 'just launched']
        score += sum(10 for kw in early_keywords if kw in text)
        
        # Lower score for mature indicators
        mature_keywords = ['established', 'mature', 'legacy', 'traditional']
        score -= sum(15 for kw in mature_keywords if kw in text)
        
        return max(min(score, 100.0), 0.0)
    
    def _identify_toll_mechanism(self, text: str) -> str:
        """Identify the likely toll mechanism"""
        if any(kw in text for kw in ['api', 'request', 'endpoint']):
            return 'API'
        elif any(kw in text for kw in ['network', 'transaction', 'blockchain']):
            return 'Network'
        elif any(kw in text for kw in ['data', 'storage', 'query']):
            return 'Data'
        elif any(kw in text for kw in ['platform', 'marketplace', 'revenue share']):
            return 'Platform'
        elif any(kw in text for kw in ['protocol', 'standard', 'specification']):
            return 'Protocol'
        else:
            return 'Other'
    
    def _extract_early_movers(self, text: str) -> List[str]:
        """Extract potential early mover companies/projects"""
        # Simplified - just look for capitalized words that might be companies
        words = text.split()
        candidates = []
        
        for word in words:
            # Simple heuristic: capitalized words 3-20 chars
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word and clean_word[0].isupper() and 3 <= len(clean_word) <= 20:
                candidates.append(clean_word)
        
        # Return unique, limited list
        return list(set(candidates))[:5]
