# Create the HTML template generator
html_generator = '''import json
import os
from datetime import datetime

def generate_level_list(levels, level_type):
    """Generate HTML for support/resistance levels"""
    if not levels:
        return '<p class="text-muted mb-0">No levels identified</p>'
    
    html = '<div class="level-list">'
    for i, level in enumerate(levels):
        html += f'<div class="level-item d-flex justify-content-between align-items-center mb-2">'
        html += f'<span class="badge bg-secondary me-2">{i+1}</span>'
        html += f'<span class="fw-bold">₹{level:,.2f}</span>'
        html += f'</div>'
    html += '</div>'
    
    return html

def create_html_page(report):
    """Create the main HTML page with analysis results"""
    
    trend_color = {
        'BULLISH': '#28a745',
        'BEARISH': '#dc3545', 
        'NEUTRAL': '#ffc107'
    }.get(report['technical_analysis']['overall_trend'], '#6c757d')
    
    recommendation_color = {
        'STRONG BUY': '#155724',
        'BUY': '#28a745',
        'WEAK BUY': '#6c757d',
        'HOLD': '#ffc107',
        'WEAK SELL': '#6c757d',
        'SELL': '#dc3545',
        'STRONG SELL': '#721c24'
    }.get(report['recommendation'], '#6c757d')
    
    # Generate strength bars for each timeframe
    def strength_bars(strength):
        active_bars = '🟢' * strength
        inactive_bars = '⚪' * (2 - strength)
        return active_bars + inactive_bars
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nifty 50 Technical Analysis - {report['market_data']['date']}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        .main-container {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            margin: 20px auto;
            padding: 30px;
            max-width: 1200px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }}
        
        .header-section {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .price-display {{
            font-size: 3rem;
            font-weight: bold;
            color: #2c3e50;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        
        .trend-badge {{
            font-size: 1.5rem;
            padding: 10px 20px;
            border-radius: 50px;
            color: white;
            background: {trend_color};
            display: inline-block;
            margin: 10px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .recommendation-badge {{
            font-size: 1.2rem;
            padding: 8px 16px;
            border-radius: 25px;
            color: white;
            background: {recommendation_color};
            display: inline-block;
            margin: 5px 0;
        }}
        
        .analysis-card {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border: 2px solid transparent;
            transition: all 0.3s ease;
            height: 100%;
        }}
        
        .analysis-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
        }}
        
        .signal-buy {{
            border-color: #28a745;
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
        }}
        
        .signal-sell {{
            border-color: #dc3545;
            background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
            color: white;
        }}
        
        .signal-neutral {{
            border-color: #ffc107;
            background: linear-gradient(135deg, #ffc107 0%, #ffca2c 100%);
            color: #212529;
        }}
        
        .metric-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .metric-row:last-child {{
            border-bottom: none;
        }}
        
        .level-card {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 20px;
            height: 100%;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .stat-item {{
            text-align: center;
            padding: 20px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 12px;
            border: 2px solid #e9ecef;
        }}
        
        .disclaimer-section {{
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border-radius: 15px;
            padding: 25px;
            margin-top: 40px;
            border: 2px solid #ffc107;
        }}
        
        .auto-refresh {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 10px 15px;
            border-radius: 25px;
            font-size: 0.9rem;
        }}
        
        @media (max-width: 768px) {{
            .main-container {{
                margin: 10px;
                padding: 20px;
            }}
            
            .price-display {{
                font-size: 2rem;
            }}
            
            .trend-badge {{
                font-size: 1.2rem;
                padding: 8px 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="auto-refresh">
        <i class="fas fa-sync-alt me-2"></i>
        Auto-updated every market day
    </div>

    <div class="main-container">
        <!-- Header Section -->
        <div class="header-section">
            <h1 class="display-4 mb-3">
                <i class="fas fa-chart-line me-3"></i>
                Nifty 50 Technical Analysis
            </h1>
            <div class="price-display">₹{report['market_data']['current_price']:,.2f}</div>
            <div class="trend-badge">{report['technical_analysis']['overall_trend']}</div>
            <div class="recommendation-badge">{report['recommendation']}</div>
            <div class="text-muted mt-2">
                <i class="fas fa-calendar me-2"></i>
                Analysis Date: {report['analysis_date']} | Market Date: {report['market_data']['date']}
            </div>
        </div>

        <!-- Technical Analysis Grid -->
        <div class="row mb-4">
            <div class="col-12">
                <h3 class="mb-4">
                    <i class="fas fa-chart-bar me-2"></i>
                    Multi-Timeframe Analysis
                </h3>
            </div>
            
            <!-- Short-term Analysis -->
            <div class="col-md-4">
                <div class="analysis-card signal-{report['technical_analysis']['short_term']['signal'].lower()}">
                    <h5 class="mb-3">
                        <i class="fas fa-tachometer-alt me-2"></i>
                        Short-term (5D)
                    </h5>
                    <div class="text-center mb-3">
                        <h4>{report['technical_analysis']['short_term']['signal']}</h4>
                        <div class="fs-5">{strength_bars(report['technical_analysis']['short_term']['strength'])}</div>
                        <small>Signal Strength: {report['technical_analysis']['short_term']['strength']}/2</small>
                    </div>
                    <div class="metric-row">
                        <span>5DMA:</span>
                        <span>₹{report['technical_analysis']['short_term']['ma_values']['5DMA']:,.2f}</span>
                    </div>
                    <div class="metric-row">
                        <span>5DEMA:</span>
                        <span>₹{report['technical_analysis']['short_term']['ma_values']['5DEMA']:,.2f}</span>
                    </div>
                    <div class="metric-row">
                        <span>Price vs MA:</span>
                        <span>{report['technical_analysis']['short_term']['price_vs_5dma']:+.2f}%</span>
                    </div>
                </div>
            </div>

            <!-- Medium-term Analysis -->
            <div class="col-md-4">
                <div class="analysis-card signal-{report['technical_analysis']['medium_term']['signal'].lower()}">
                    <h5 class="mb-3">
                        <i class="fas fa-chart-line me-2"></i>
                        Medium-term (50D)
                    </h5>
                    <div class="text-center mb-3">
                        <h4>{report['technical_analysis']['medium_term']['signal']}</h4>
                        <div class="fs-5">{strength_bars(report['technical_analysis']['medium_term']['strength'])}</div>
                        <small>Signal Strength: {report['technical_analysis']['medium_term']['strength']}/2</small>
                    </div>
                    <div class="metric-row">
                        <span>50DMA:</span>
                        <span>₹{report['technical_analysis']['medium_term']['ma_values']['50DMA']:,.2f}</span>
                    </div>
                    <div class="metric-row">
                        <span>Price vs MA:</span>
                        <span>{report['technical_analysis']['medium_term']['price_vs_50dma']:+.2f}%</span>
                    </div>
                    <div class="metric-row">
                        <span>MA Trend:</span>
                        <span>{report['technical_analysis']['medium_term']['ma_trend']:+.2f}%</span>
                    </div>
                </div>
            </div>

            <!-- Long-term Analysis -->
            <div class="col-md-4">
                <div class="analysis-card signal-{report['technical_analysis']['long_term']['signal'].lower()}">
                    <h5 class="mb-3">
                        <i class="fas fa-chart-area me-2"></i>
                        Long-term (200D)
                    </h5>
                    <div class="text-center mb-3">
                        <h4>{report['technical_analysis']['long_term']['signal']}</h4>
                        <div class="fs-5">{strength_bars(report['technical_analysis']['long_term']['strength'])}</div>
                        <small>Signal Strength: {report['technical_analysis']['long_term']['strength']}/2</small>
                    </div>
                    <div class="metric-row">
                        <span>200DMA:</span>
                        <span>₹{report['technical_analysis']['long_term']['ma_values']['200DMA']:,.2f}</span>
                    </div>
                    <div class="metric-row">
                        <span>Price vs MA:</span>
                        <span>{report['technical_analysis']['long_term']['price_vs_200dma']:+.2f}%</span>
                    </div>
                    <div class="metric-row">
                        <span>MA Trend:</span>
                        <span>{report['technical_analysis']['long_term']['ma_trend']:+.2f}%</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Support & Resistance -->
        <div class="row mb-4">
            <div class="col-12">
                <h3 class="mb-4">
                    <i class="fas fa-layer-group me-2"></i>
                    Support & Resistance Levels
                </h3>
            </div>
            <div class="col-md-6">
                <div class="level-card">
                    <h5 class="text-danger mb-3">
                        <i class="fas fa-arrow-up me-2"></i>
                        Resistance Levels
                    </h5>
                    {generate_level_list(report['support_resistance']['resistance'], 'resistance')}
                </div>
            </div>
            <div class="col-md-6">
                <div class="level-card">
                    <h5 class="text-success mb-3">
                        <i class="fas fa-arrow-down me-2"></i>
                        Support Levels
                    </h5>
                    {generate_level_list(report['support_resistance']['support'], 'support')}
                </div>
            </div>
        </div>

        <!-- Market Statistics -->
        <div class="stats-grid">
            <div class="stat-item">
                <h4 class="text-primary">{report['market_data']['volume']:,}</h4>
                <small class="text-muted">Trading Volume</small>
            </div>
            <div class="stat-item">
                <h4 class="text-warning">{report['market_data']['volatility']:.1f}%</h4>
                <small class="text-muted">Annual Volatility</small>
            </div>
            <div class="stat-item">
                <h4 class="text-info">{report['risk_assessment']['level']}</h4>
                <small class="text-muted">Risk Level</small>
            </div>
            <div class="stat-item">
                <h4 class="text-secondary">NSE</h4>
                <small class="text-muted">Exchange</small>
            </div>
        </div>

        <!-- Research Background -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="analysis-card">
                    <h5 class="mb-3">
                        <i class="fas fa-graduation-cap me-2"></i>
                        Research Methodology
                    </h5>
                    <p class="mb-2">
                        This analysis is based on the peer-reviewed research paper 
                        <strong>"Comparative Technical Analysis and Prediction of Nifty-50 Performance"</strong>.
                    </p>
                    <div class="row text-center mt-3">
                        <div class="col-md-4">
                            <div class="border rounded p-2 mb-2">
                                <strong>5DMA & 5DEMA</strong><br>
                                <small class="text-muted">Short-term prediction</small>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="border rounded p-2 mb-2">
                                <strong>50DMA</strong><br>
                                <small class="text-muted">Medium-term analysis</small>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="border rounded p-2 mb-2">
                                <strong>200DMA</strong><br>
                                <small class="text-muted">Long-term trends</small>
                            </div>
                        </div>
                    </div>
                    <p class="mt-3 mb-0">
                        <small class="text-muted">
                            <i class="fas fa-check-circle me-1"></i>
                            Statistical significance confirmed (p &lt; 0.05) | 
                            <i class="fas fa-robot me-1"></i>
                            Automated via GitHub Actions | 
                            <i class="fas fa-sync me-1"></i>
                            Updated daily at 6:30 AM IST
                        </small>
                    </p>
                </div>
            </div>
        </div>

        <!-- Disclaimer -->
        <div class="disclaimer-section">
            <h5 class="text-warning mb-3">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Important Disclaimer
            </h5>
            <p class="mb-0">
                This analysis is for <strong>educational purposes only</strong> and should not be considered as financial advice. 
                The technical analysis is based on historical price data and mathematical indicators. 
                Always conduct your own research and consult with a qualified financial advisor before making investment decisions.
                <strong>Past performance does not guarantee future results.</strong>
            </p>
        </div>

        <!-- Footer -->
        <div class="text-center mt-4 pt-4 border-top">
            <p class="text-muted mb-0">
                <i class="fab fa-github me-2"></i>
                Powered by GitHub Actions | 
                <i class="fas fa-chart-line me-2"></i>
                Research-based Analysis | 
                <i class="fas fa-heart text-danger me-2"></i>
                Made for the Indian Investment Community
            </p>
            <small class="text-muted">
                Open Source Project | MIT License | 
                <a href="https://github.com/yourusername/nifty-analysis" class="text-decoration-none">
                    View on GitHub
                </a>
            </small>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Auto-refresh page every 30 minutes during market hours
        setTimeout(function() {{
            window.location.reload();
        }}, 30 * 60 * 1000);
        
        // Add smooth scroll behavior
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // Add loading animation
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.analysis-card');
            cards.forEach((card, index) => {{
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => {{
                    card.style.transition = 'all 0.5s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }}, index * 150);
            }});
        }});
    </script>
</body>
</html>'''
    
    return html_content

def main():
    """Generate HTML page from JSON data"""
    try:
        # Load the analysis data
        with open('data.json', 'r') as f:
            report = json.load(f)
        
        # Generate HTML page
        html_content = create_html_page(report)
        
        # Save HTML file
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("HTML page generated successfully!")
        return True
        
    except FileNotFoundError:
        print("Error: data.json not found. Run main_web.py first.")
        return False
    except Exception as e:
        print(f"Error generating HTML: {str(e)}")
        return False

if __name__ == "__main__":
    main()
'''

# Save the HTML generator
with open('generate_html.py', 'w') as f:
    f.write(html_generator)

print("✅ Created generate_html.py - HTML page generator")