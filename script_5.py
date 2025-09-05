# Create updated README for web deployment
web_readme = '''# Nifty 50 Technical Analysis - Web Dashboard

🏦 **Automated Nifty 50 technical analysis with live web dashboard based on research paper "Comparative Technical Analysis and Prediction of Nifty-50 Performance"**

[![GitHub Pages](https://github.com/yourusername/nifty-analysis/workflows/Nifty%2050%20Web%20Analysis/badge.svg)](https://yourusername.github.io/nifty-analysis/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌐 Live Dashboard

**View the live analysis at: [https://yourusername.github.io/nifty-analysis/](https://yourusername.github.io/nifty-analysis/)**

The dashboard updates automatically every weekday morning at 6:30 AM IST with fresh technical analysis.

## 📋 Overview

This project implements an automated technical analysis system for the Nifty 50 index that displays results on a professional web dashboard. The system runs on GitHub Actions and deploys to GitHub Pages, providing a beautiful, mobile-responsive interface for viewing daily technical analysis.

### Key Features

- 🌐 **Live Web Dashboard**: Professional, mobile-responsive interface
- 🤖 **Automated Analysis**: Runs every morning at 6:30 AM IST (weekdays only)
- 📊 **Multi-timeframe Analysis**: Short, medium, and long-term trend analysis
- 🎯 **Support/Resistance Levels**: Automatically calculated key levels
- 📈 **Moving Average Signals**: 5DMA, 5DEMA, 50DMA, and 200DMA analysis
- ☁️ **GitHub Pages Hosting**: Free, reliable hosting with automatic updates
- 📱 **Mobile Optimized**: Works perfectly on all devices

## 🧮 Technical Methodology

Based on the research paper's findings, the system implements:

### Moving Average Analysis
- **Short-term prediction**: 5-day Moving Average (5DMA) and 5-day Exponential Moving Average (5DEMA)
- **Medium-term prediction**: 50-day Moving Average (50DMA)
- **Long-term prediction**: 200-day Moving Average (200DMA)

### Signal Generation
- **BUY/SELL/NEUTRAL** signals for each timeframe
- **Strength indicators** (1-2 scale) based on multiple confirmations
- **Overall trend determination** using consensus approach

### Web Dashboard Features
- **Real-time Price Display**: Current Nifty 50 price with trend indicators
- **Visual Signal Cards**: Color-coded analysis for each timeframe
- **Interactive Design**: Smooth animations and hover effects
- **Market Statistics**: Volume, volatility, and risk assessment
- **Support/Resistance Levels**: Key technical levels for trading decisions

## 🚀 Quick Deployment (5 Minutes)

### Step 1: Fork this Repository
Click the "Fork" button at the top right of this repository.

### Step 2: Enable GitHub Pages
1. Go to your forked repository → **Settings** → **Pages**
2. Under "Source", select **GitHub Actions**
3. GitHub will automatically suggest workflows - choose "Static HTML"

### Step 3: Enable GitHub Actions
1. Go to the **Actions** tab in your repository
2. Click "I understand my workflows, go ahead and enable them"

### Step 4: Test the Setup
1. Go to **Actions** → **Nifty 50 Web Analysis**
2. Click **"Run workflow"** → **"Run workflow"** (green button)
3. Wait 3-4 minutes for completion
4. Visit **https://yourusername.github.io/nifty-analysis/** to see your live dashboard

## 📊 Dashboard Features

### Main Dashboard Elements

#### 🎯 Market Summary
- **Current Price**: Real-time Nifty 50 price
- **Overall Trend**: BULLISH/BEARISH/NEUTRAL with color coding
- **Recommendation**: STRONG BUY/BUY/HOLD/SELL/STRONG SELL
- **Risk Level**: HIGH/MODERATE/LOW based on volatility

#### 📈 Technical Analysis Cards
- **Short-term (5D)**: 5DMA & 5DEMA analysis with signal strength
- **Medium-term (50D)**: 50DMA analysis with trend indicators
- **Long-term (200D)**: 200DMA analysis with momentum signals

#### 🎪 Support & Resistance
- **Resistance Levels**: Top 3 overhead resistance points
- **Support Levels**: Top 3 underlying support points
- **Automatic Calculation**: Using pivot point analysis

#### 📊 Market Statistics
- **Trading Volume**: Daily volume with historical context
- **Annual Volatility**: Risk measurement indicator
- **Market Date**: Last trading session date
- **Exchange**: NSE (National Stock Exchange)

### 🎨 Design Features
- **Gradient Background**: Professional purple gradient design
- **Glass Morphism**: Modern frosted glass card effects
- **Responsive Layout**: Perfect on desktop, tablet, and mobile
- **Color Coding**: Green (bullish), red (bearish), yellow (neutral)
- **Smooth Animations**: Loading effects and hover interactions
- **Auto-refresh**: Page refreshes every 30 minutes during market hours

## ⏰ Scheduling

The system automatically runs:
- **Time**: Every weekday at 6:30 AM IST (1:00 AM UTC)
- **Frequency**: Monday to Friday (market days only)
- **Deployment**: Results automatically deploy to GitHub Pages
- **Manual**: You can trigger manually anytime via GitHub Actions

## 🔧 Customization Options

### Change Schedule Time
Edit `.github/workflows/nifty-web-analysis.yml`:
```yaml
schedule:
  - cron: '30 1 * * 1-5'  # 7:00 AM IST
```

### Modify Dashboard Colors
Edit the CSS in `generate_html.py` to change:
- Background gradients
- Signal colors
- Card styling
- Typography

### Add Custom Analytics
Extend `main_web.py` to include:
- Additional technical indicators
- Custom signal logic
- Extended market data
- Social sentiment analysis

## 📂 Project Structure

```
nifty-analysis/
├── main_web.py                     # Web analysis engine
├── generate_html.py                # HTML dashboard generator
├── requirements.txt                # Python dependencies
├── .github/workflows/
│   └── nifty-web-analysis.yml     # GitHub Pages deployment
├── README.md                       # This file
├── LICENSE                         # MIT License
└── .gitignore                      # Git ignore rules
```

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/nifty-analysis.git
cd nifty-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run analysis and generate dashboard
python main_web.py
python generate_html.py

# Open index.html in your browser
```

## 🔍 Monitoring & Logs

### Check Execution Status
1. Go to **Actions** tab
2. Click on latest **"Nifty 50 Web Analysis"** run
3. Review logs for any issues

### Dashboard Health Check
- Visit your GitHub Pages URL
- Check if price and date are current
- Verify all sections load correctly
- Test mobile responsiveness

### Common Issues & Solutions

**❌ Dashboard not updating**
- Check if GitHub Actions workflow is running
- Verify GitHub Pages is enabled in repository settings
- Review workflow logs for any errors

**❌ Analysis showing old data**
- Check if Yahoo Finance API is accessible
- Verify workflow is running on scheduled time
- Review Python script logs for data fetch errors

**❌ Dashboard not loading**
- Confirm GitHub Pages is properly configured
- Check if index.html is being generated
- Verify all dependencies are installed

## 🛡️ Security & Privacy

- ✅ **No sensitive data**: Analysis uses only public market data
- ✅ **No user tracking**: Dashboard doesn't collect user information
- ✅ **Open source**: Full transparency of analysis methods
- ✅ **GitHub hosting**: Reliable, secure hosting platform

## 📈 Advanced Features

### API Endpoint
The system also generates `data.json` which can be used as an API endpoint:
```
https://yourusername.github.io/nifty-analysis/data.json
```

This JSON contains all analysis data and can be consumed by:
- Mobile apps
- Trading bots
- Custom dashboards
- Third-party integrations

### Custom Domain Setup
To use your own domain:
1. Go to **Settings** → **Pages**
2. Add your custom domain
3. Configure DNS records with your domain provider
4. Enable HTTPS enforcement

### Performance Optimization
The dashboard is optimized for:
- **Fast loading**: Minimal external dependencies
- **Mobile performance**: Responsive design with touch optimization
- **SEO friendly**: Proper meta tags and semantic HTML
- **Accessibility**: WCAG compliant color contrast and navigation

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

### Dashboard Enhancements
- [ ] **Dark mode toggle**
- [ ] **Historical chart integration**
- [ ] **Comparison with other indices**
- [ ] **Advanced filtering options**

### Technical Improvements
- [ ] **Additional indicators**: RSI, MACD, Bollinger Bands
- [ ] **Backtesting module**: Historical strategy performance
- [ ] **Multi-asset support**: Bank Nifty, sector indices
- [ ] **Alert system**: Email/SMS notifications for signals

### Integration Features
- [ ] **WhatsApp notifications**
- [ ] **Discord/Slack bots**
- [ ] **Mobile app development**
- [ ] **API rate limiting**

## 📋 Troubleshooting

### GitHub Pages Setup Issues
1. **Repository Settings**: Ensure Pages is enabled with GitHub Actions source
2. **Workflow Permissions**: Check that Actions have write permissions for Pages
3. **Branch Protection**: Make sure main branch allows Actions to push

### Analysis Data Issues
1. **Yahoo Finance Access**: API may have temporary issues or rate limits
2. **Market Holidays**: Analysis won't run on non-trading days
3. **Time Zone Confusion**: Remember schedule is in UTC, not IST

### Dashboard Display Issues
1. **Browser Cache**: Hard refresh (Ctrl+F5) to clear cached files
2. **Mobile Rendering**: Test on multiple devices and browsers
3. **Content Blocking**: Some ad blockers may interfere with external fonts/styles

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**Important**: This analysis is for educational purposes only and should not be considered as financial advice. Always conduct your own research and consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.

The technical analysis provided by this system is based on historical price data and mathematical indicators from the research paper "Comparative Technical Analysis and Prediction of Nifty-50 Performance". Market conditions, economic factors, and unforeseen events can significantly impact stock prices regardless of technical indicators.

## 🙏 Acknowledgments

- Research paper authors for the technical methodology
- Yahoo Finance for providing free market data
- GitHub for free hosting and automation platform
- Bootstrap and Font Awesome for UI components
- Open source community for Python libraries

---

**Made with ❤️ for the Indian investment community**

*Star ⭐ this repository if you find it helpful!*

## 🔗 Quick Links

- 🌐 **Live Dashboard**: [https://yourusername.github.io/nifty-analysis/](https://yourusername.github.io/nifty-analysis/)
- 📊 **API Endpoint**: [https://yourusername.github.io/nifty-analysis/data.json](https://yourusername.github.io/nifty-analysis/data.json)
- 🐛 **Report Issues**: [GitHub Issues](https://github.com/yourusername/nifty-analysis/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/nifty-analysis/discussions)
- 📧 **Contact**: Create an issue for support
'''

# Save the updated README
with open('README_WEB.md', 'w') as f:
    f.write(web_readme)

print("✅ Created README_WEB.md - Web deployment documentation")