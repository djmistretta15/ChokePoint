"""
Tollbooth Seeker AI - Main Engine
Infrastructure Chokepoint Intelligence System
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List

from signal_detector import SignalDetector, InfrastructureSignal
from database import SignalDatabase

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/tollbooth_seeker.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class TollboothSeeker:
    def __init__(self, config_path: str = 'config.json'):
        """Initialize the Tollbooth Seeker engine"""
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.detector = SignalDetector(self.config)
        self.db = SignalDatabase(self.config.get('logging', {}).get('db_path', 'data/signals.db'))
        
        self.running = False
        
        logger.info("Tollbooth Seeker AI initialized")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    async def run_detection_cycle(self):
        """Execute one complete detection cycle"""
        logger.info("Starting detection cycle...")
        
        # Step 1: Display dashboard
        self._display_dashboard()
        
        # Step 2: Detect new signals
        signals = await self.detector.run_detection_cycle()
        
        if not signals:
            logger.info("No new signals detected this cycle")
            return
        
        logger.info(f"Detected {len(signals)} potential signals")
        
        # Step 3: Process and save signals
        new_count = 0
        for signal in signals:
            # Check for duplicates
            if self.db.signal_exists(signal.title, hours_window=48):
                continue
            
            # Save to database
            signal_id = self.db.save_signal({
                'title': signal.title,
                'description': signal.description,
                'source': signal.source,
                'sector': signal.sector,
                'url': signal.url,
                'inevitability_score': signal.inevitability_score,
                'moat_score': signal.moat_score,
                'timing_score': signal.timing_score,
                'total_score': signal.total_score,
                'toll_mechanism': signal.toll_mechanism,
                'breadcrumbs': signal.breadcrumbs,
                'early_movers': signal.early_movers
            })
            
            new_count += 1
            
            # Display signal
            self._display_signal(signal, signal_id)
            
            # Auto-watchlist high-priority signals
            if signal.total_score >= self.config.get('high_priority_threshold', 8.5):
                self.db.add_to_watchlist(signal_id, "Auto-added: High priority")
                logger.info(f"  ⭐ Auto-added to watchlist (score: {signal.total_score:.1f})")
        
        logger.info(f"Saved {new_count} new signals to database")
    
    def _display_dashboard(self):
        """Display current dashboard statistics"""
        stats = self.db.get_dashboard_stats()
        
        print("\n" + "="*80)
        print("⚡ TOLLBOOTH SEEKER AI - DASHBOARD")
        print("="*80)
        print(f"Active Signals: {stats['active_signals']}")
        print(f"Average Score: {stats['avg_score']:.1f}")
        print(f"High Priority: {stats['high_priority']}")
        print(f"Hidden Gems: {stats['hidden_gems']}")
        print(f"New (24h): {stats['recent_24h']}")
        print("="*80)
    
    def _display_signal(self, signal: InfrastructureSignal, signal_id: int):
        """Display a detected signal"""
        print(f"\n{'─'*80}")
        print(f"🎯 SIGNAL #{signal_id}: {signal.title[:60]}")
        print(f"{'─'*80}")
        print(f"Sector: {signal.sector} | Source: {signal.source}")
        print(f"Score: {signal.total_score:.1f}/10")
        print(f"  • Inevitability: {signal.inevitability_score:.0f}%")
        print(f"  • Moat Potential: {signal.moat_score:.0f}%")
        print(f"  • Timing Window: {signal.timing_score:.0f}%")
        print(f"Toll Mechanism: {signal.toll_mechanism}")
        
        if signal.early_movers:
            print(f"Early Movers: {', '.join(signal.early_movers[:3])}")
        
        print(f"\nBreadcrumbs:")
        for crumb in signal.breadcrumbs[:5]:
            print(f"  • {crumb}")
        
        print(f"\nURL: {signal.url}")
    
    def display_top_signals(self, limit: int = 10):
        """Display top signals by score"""
        signals = self.db.get_active_signals(limit)
        
        print("\n" + "="*80)
        print(f"🏆 TOP {limit} SIGNALS")
        print("="*80)
        
        for i, signal in enumerate(signals, 1):
            print(f"\n{i}. [{signal['total_score']:.1f}] {signal['title'][:60]}")
            print(f"   Sector: {signal['sector']} | {signal['toll_mechanism']}")
            print(f"   Source: {signal['source']}")
    
    def display_sector_breakdown(self):
        """Display signals by sector"""
        stats = self.db.get_sector_stats()
        
        print("\n" + "="*80)
        print("📊 SECTOR BREAKDOWN")
        print("="*80)
        
        for sector, data in sorted(stats.items(), key=lambda x: x[1]['avg_score'], reverse=True):
            print(f"\n{sector}:")
            print(f"  Signals: {data['count']}")
            print(f"  Avg Score: {data['avg_score']:.1f}")
            print(f"  Max Score: {data['max_score']:.1f}")
    
    def display_watchlist(self):
        """Display watchlisted signals"""
        signals = self.db.get_watchlist()
        
        print("\n" + "="*80)
        print("⭐ WATCHLIST")
        print("="*80)
        
        if not signals:
            print("No signals in watchlist")
            return
        
        for signal in signals:
            print(f"\n[{signal['total_score']:.1f}] {signal['title'][:60]}")
            print(f"  Sector: {signal['sector']} | Added: {signal['watchlist_added']}")
            if signal['watchlist_notes']:
                print(f"  Notes: {signal['watchlist_notes']}")
    
    async def run(self):
        """Main run loop"""
        self.running = True
        scan_interval = self.config.get('scan_interval_minutes', 60) * 60
        
        print("\n" + "="*80)
        print("⚡ TOLLBOOTH SEEKER AI - STARTING")
        print("="*80)
        print("Infrastructure Chokepoint Intelligence Engine")
        print("Detecting tomorrow's mandatory rails")
        print(f"Scan Interval: {scan_interval//60} minutes")
        print("="*80 + "\n")
        
        cycle_count = 0
        
        try:
            while self.running:
                cycle_count += 1
                print(f"\n\n{'#'*80}")
                print(f"DETECTION CYCLE {cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'#'*80}")
                
                await self.run_detection_cycle()
                
                # Wait for next cycle
                logger.info(f"Waiting {scan_interval//60} minutes until next cycle...")
                await asyncio.sleep(scan_interval)
                
        except KeyboardInterrupt:
            logger.info("\nShutdown requested by user")
        finally:
            self._shutdown()
    
    def _shutdown(self):
        """Clean shutdown"""
        print("\n" + "="*80)
        print("📊 FINAL SUMMARY")
        print("="*80)
        
        self._display_dashboard()
        self.display_top_signals(5)
        self.display_sector_breakdown()
        
        print("\n" + "="*80)
        print("🛑 Tollbooth Seeker stopped")
        print("="*80)

async def main():
    """Main entry point"""
    print("\n⚡ TOLLBOOTH SEEKER AI")
    print("="*80)
    print("Infrastructure Chokepoint Intelligence Engine")
    print("="*80)
    
    seeker = TollboothSeeker('config.json')
    
    # Check if user wants to see existing data first
    print("\nOptions:")
    print("1. Start detection cycle")
    print("2. View top signals")
    print("3. View sector breakdown")
    print("4. View watchlist")
    
    try:
        choice = input("\nEnter choice (or press Enter to start): ").strip()
        
        if choice == '2':
            seeker.display_top_signals(15)
            return
        elif choice == '3':
            seeker.display_sector_breakdown()
            return
        elif choice == '4':
            seeker.display_watchlist()
            return
    except:
        pass
    
    # Start the engine
    await seeker.run()

if __name__ == "__main__":
    asyncio.run(main())
