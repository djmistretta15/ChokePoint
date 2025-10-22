# ⚡ Tollbooth Seeker - Quick Start Guide

## 🚀 Get Running in 2 Minutes

### Step 1: Install
```bash
pip install -r requirements.txt --break-system-packages
```

### Step 2: Run
```bash
./start.sh
```

or

```bash
python3 main.py
```

That's it! The engine will start detecting infrastructure signals.

---

## 📊 First Run - What to Expect

### Menu Options
When you start, you'll see:
```
1. Start detection cycle
2. View top signals
3. View sector breakdown  
4. View watchlist
```

**First time?** Just press Enter to start detection.

### What Happens Next

The engine will:
1. Scan HackerNews, GitHub, Reddit, ArXiv
2. Detect infrastructure signals
3. Calculate scores (inevitability, moat, timing)
4. Save high-scoring signals (7.0+)
5. Display dashboard and new opportunities
6. Repeat every hour

---

## 🎯 Understanding the Output

### Dashboard
```
Active Signals: 23
Average Score: 7.8
High Priority: 5
Hidden Gems: 12
New (24h): 8
```

### Signal Display
```
🎯 SIGNAL #15: Multi-Agent API Orchestration Layer

Score: 9.2/10
  • Inevitability: 95%
  • Moat Potential: 85%
  • Timing Window: 90%

Toll Mechanism: API
Sector: AI

Breadcrumbs:
  • api_complaints: rate limit
  • integration_pain: multiple APIs
  • adoption_signals: becoming standard
```

---

## 🔧 Quick Config Tweaks

### Want More Signals?
Lower the minimum score in `config.json`:
```json
"min_signal_score": 6.5  // Was 7.0
```

### Want Faster Scanning?
```json
"scan_interval_minutes": 30  // Was 60
```

### Focus on Specific Sectors?
Increase sector weights:
```json
"AI": { "weight": 1.5 }
```

---

## 📈 Check Your Data

### View Top Signals Anytime
```python
from database import SignalDatabase

db = SignalDatabase()
signals = db.get_active_signals(10)

for s in signals:
    print(f"[{s['total_score']:.1f}] {s['title']}")
```

### Check Sector Stats
```python
stats = db.get_sector_stats()
for sector, data in stats.items():
    print(f"{sector}: {data['count']} signals, avg {data['avg_score']:.1f}")
```

---

## 💡 Pro Tips

### First 24 Hours
- Let it run continuously
- Build up signal database
- Don't tweak settings yet

### After 24 Hours
- Review top signals
- Identify interesting patterns
- Adjust sector focus if needed

### After 7 Days
- Analyze sector trends
- Deep dive on high-priority signals
- Research early movers

---

## 🎓 Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 9.0+ | Exceptional | Research immediately |
| 8.5-8.9 | High Priority | Add to watchlist |
| 7.5-8.4 | Hidden Gem | Monitor closely |
| 7.0-7.4 | Qualified | Periodic check |
| <7.0 | Filtered | Not saved |

---

## 🔍 Common First Questions

### "Why aren't I seeing signals immediately?"
- First cycle scans all sources (takes 2-3 minutes)
- Signals need score >= 7.0 to display
- HackerNews/Reddit may be quiet at certain times

### "Can I run this 24/7?"
- Yes! Designed for continuous operation
- Logs to `logs/tollbooth_seeker.log`
- Database grows over time

### "How do I stop it?"
- Press `Ctrl+C`
- Shows final summary before exiting
- Database is saved automatically

---

## 🚨 Troubleshooting

### No signals detected
- Check internet connection
- Verify sources aren't rate-limited
- Lower `min_signal_score` in config

### Script won't start
- Ensure Python 3.9+
- Check dependencies installed
- Review logs for errors

### Database errors
- Ensure `data/` directory exists
- Check file permissions
- Delete `data/signals.db` to reset

---

## 📊 What to Do With Signals

### For Investors
1. Filter by sector interest
2. Check inevitability score
3. Research early movers
4. Validate market size
5. Track over time

### For Builders
1. Look for high inevitability + low moat
2. Gaps = opportunities
3. Check early mover activity
4. Validate pain points
5. Time your entry

### For Researchers
1. Monitor academic signals (ArXiv)
2. Track commercial interest
3. Identify tech transitions
4. Spot collaboration opportunities

---

## 📁 File Reference

| File | Purpose |
|------|---------|
| `config.json` | All settings |
| `data/signals.db` | Signal database |
| `logs/tollbooth_seeker.log` | Detailed logs |
| `README.md` | Full documentation |

---

## 🔄 Next Actions

1. ✅ Run for 24 hours
2. ✅ Review top 10 signals
3. ✅ Check sector breakdown
4. ✅ Add favorites to watchlist
5. ✅ Deep dive on 9.0+ signals

---

**Built by Daniel James Mistretta**

**Ready to find tomorrow's tollbooths today.**
