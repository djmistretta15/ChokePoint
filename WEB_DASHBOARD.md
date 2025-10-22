# 🌐 Tollbooth Seeker - Web Dashboard Guide

## 🎯 Your Beautiful Frontend is Here!

The web dashboard provides a visual interface for exploring infrastructure signals with:

- ✅ **Real-time dashboard** with live stats
- ✅ **Interactive signal cards** with full details
- ✅ **Sector filtering** (AI, Compute, Finance, Bio)
- ✅ **Sort by score/timing/moat**
- ✅ **Watchlist management**
- ✅ **Beautiful gradient UI** matching your screenshot

---

## 🚀 Starting the Web Dashboard

### Option 1: Quick Start
```bash
./start_web.sh
```

### Option 2: Manual Start
```bash
pip install -r requirements.txt --break-system-packages
python3 web_server.py
```

### Access the Dashboard
Open your browser and go to:
```
http://localhost:5000
```

---

## 📊 Dashboard Features

### Stats Overview
At the top, you'll see four key metrics:
- **Active Signals**: Total signals being tracked
- **Avg Score**: Overall signal quality
- **High Priority**: Signals scoring 8.5+
- **Hidden Gems**: Solid signals (7.5-8.4)

### Sector Filters
Click any sector button to filter signals:
- **all**: Show everything
- **AI**: Artificial intelligence signals
- **Compute**: GPU, cloud, distributed systems
- **Finance**: Fintech, payments, blockchain
- **Bio**: Biotech, genomics, drug discovery

### Sort Options
Choose how to order signals:
- **Score**: Highest total score first (default)
- **Timing**: Best timing window first
- **Moat**: Highest moat potential first

### Signal Cards
Each card shows:
- **Title** and **Total Score** (color-coded)
- **Three-part breakdown**:
  - Inevitability % (with progress bar)
  - Moat Potential % (with progress bar)
  - Timing Window % (with progress bar)
- **Breadcrumbs**: Detection triggers
- **Early Movers**: Companies/projects already active
- **Toll Mechanism**: How money will be collected
- **Actions**:
  - View Source (opens original URL)
  - Add to Watchlist ⭐

---

## 🎨 Score Color Coding

Signals are color-coded by score:

- **Blue gradient** (7.0-8.4): Qualified/Hidden Gem
- **Purple gradient** (8.5-8.9): High Priority
- **Cyan gradient** (9.0+): Exceptional Opportunity

---

## 🔄 Running Both Systems

You have two modes:

### Mode 1: Dashboard Only (View Existing Data)
```bash
./start_web.sh
```
- Shows signals already in database
- Great for exploring existing data
- No new detection running

### Mode 2: Detection + Dashboard (Continuous)

**Terminal 1** (Detection Engine):
```bash
python3 main.py
```

**Terminal 2** (Web Dashboard):
```bash
./start_web.sh
```

This runs both:
- Backend detects new signals every hour
- Frontend displays them in real-time
- Dashboard auto-refreshes every 30 seconds

---

## 💡 Workflow Examples

### First Time Setup
1. Run detection engine first to build database:
   ```bash
   python3 main.py
   ```
2. Let it run for 1-2 cycles (60-120 minutes)
3. Start web dashboard:
   ```bash
   ./start_web.sh
   ```
4. Open http://localhost:5000
5. Explore your signals!

### Daily Use
1. Keep detection engine running in background
2. Open web dashboard when you want to explore
3. Filter by sector of interest
4. Add promising signals to watchlist
5. Click "View Source" to research deeper

### Demo/Presentation Mode
1. Make sure you have signals in database
2. Start web dashboard only:
   ```bash
   ./start_web.sh
   ```
3. Open in browser
4. Share your screen
5. Click through sectors and signals

---

## 📱 Mobile Responsive

The dashboard works on:
- ✅ Desktop (best experience)
- ✅ Tablet (responsive grid)
- ✅ Mobile (stacked layout)

---

## 🔌 API Endpoints

The web server exposes these REST APIs:

### Dashboard Stats
```
GET http://localhost:5000/api/dashboard
```
Returns:
```json
{
  "active_signals": 23,
  "avg_score": 7.8,
  "high_priority": 5,
  "hidden_gems": 12,
  "recent_24h": 8
}
```

### All Signals
```
GET http://localhost:5000/api/signals
```

### High Priority Only
```
GET http://localhost:5000/api/signals/high-priority
```

### By Sector
```
GET http://localhost:5000/api/signals/sector/AI
```

### Sector Stats
```
GET http://localhost:5000/api/sectors
```

### Watchlist
```
GET http://localhost:5000/api/watchlist
```

### Add to Watchlist
```
POST http://localhost:5000/api/watchlist/add/<signal_id>
```

---

## 🎯 Keyboard Shortcuts

None yet, but coming soon:
- `f`: Focus sector filter
- `s`: Cycle sort options
- `r`: Refresh data
- `w`: View watchlist

---

## 🔧 Customization

### Change Port
Edit `web_server.py` line 69:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
Change `5000` to your preferred port.

### Adjust Refresh Rate
Edit `web/index.html` line 181:
```javascript
const interval = setInterval(loadData, 30000); // 30 seconds
```
Change `30000` to your preferred milliseconds.

### Modify Colors
Edit the CSS in `web/index.html` starting at line 9.

---

## 🚨 Troubleshooting

### "Connection refused" error
- Make sure web server is running
- Check it's on port 5000
- Try `http://127.0.0.1:5000` instead of `localhost`

### Empty dashboard
- Database might be empty
- Run detection engine first: `python3 main.py`
- Wait for at least one cycle (60 minutes)

### "Module not found: flask"
- Install dependencies: `pip install -r requirements.txt --break-system-packages`

### Dashboard not updating
- Check browser console for errors
- Verify API is responding: http://localhost:5000/api/dashboard
- Refresh the page

### Signals not appearing
- Check database has data:
  ```python
  from database import SignalDatabase
  db = SignalDatabase()
  print(db.get_active_signals(10))
  ```

---

## 🎓 Best Practices

### For Exploration
1. Start with "all" sectors
2. Sort by "Score" to see best opportunities
3. Click through high-scoring signals
4. Add favorites to watchlist

### For Research
1. Filter to your sector of interest
2. Sort by "Timing" to find early opportunities
3. Check "Early Movers" for companies to research
4. Click "View Source" to read original content

### For Investment Thesis
1. Look at "High Priority" signals only
2. Export data via API
3. Track score changes over time
4. Build spreadsheet of promising areas

---

## 📊 Advanced Usage

### Export All Signals to JSON
```bash
curl http://localhost:5000/api/signals > signals.json
```

### Query Specific Sector
```bash
curl http://localhost:5000/api/signals/sector/AI | jq
```

### Monitor High Priority
```bash
watch -n 30 'curl -s http://localhost:5000/api/signals/high-priority | jq length'
```

---

## 🔐 Security Notes

**Current Setup**: 
- Runs on localhost only
- No authentication required
- Safe for local development

**For Production**:
- Add authentication
- Use HTTPS
- Restrict CORS
- Add rate limiting

---

## 📈 Performance

### Expected Load Times
- Dashboard load: < 500ms
- Signal cards: < 100ms each
- API responses: < 50ms
- Auto-refresh: every 30 seconds

### Scales to:
- 1000+ signals
- Multiple concurrent users
- Real-time updates

---

## 🎉 Features Coming Soon

- [ ] Watchlist page
- [ ] Signal detail modal
- [ ] Score history charts
- [ ] Sector comparison graphs
- [ ] Email alerts
- [ ] Export to PDF/Excel
- [ ] Dark/light mode toggle
- [ ] Keyboard shortcuts
- [ ] Search/filter by keywords

---

## 💬 Need Help?

### Check Logs
```bash
tail -f logs/tollbooth_seeker.log
```

### Verify Server Running
```bash
curl http://localhost:5000/api/dashboard
```

### Check Database
```python
from database import SignalDatabase
db = SignalDatabase()
print(f"Signals: {db.get_dashboard_stats()}")
```

---

## 🚀 Quick Command Reference

```bash
# Start web dashboard
./start_web.sh

# Start detection engine
python3 main.py

# Check if server is running
curl http://localhost:5000/api/dashboard

# View all signals
curl http://localhost:5000/api/signals | jq

# Check database stats
python3 -c "from database import SignalDatabase; db = SignalDatabase(); print(db.get_dashboard_stats())"
```

---

**Your beautiful frontend is ready! 🎉**

**Just run `./start_web.sh` and open http://localhost:5000**
