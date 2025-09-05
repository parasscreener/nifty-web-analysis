# Create the main web-based analysis script (fixed encoding issues)
web_main_script = '''import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NiftyWebAnalyzer:
    """
    Nifty Technical Analysis for Web Display
    Based on research paper: 'Comparative Technical Analysis and Prediction of Nifty-50 Performance'
    """
    
    def __init__(self):
        self.symbol = "^NSEI"  # Nifty 50 Yahoo Finance symbol
        self.data = None
        self.results = {}
        
    def fetch_data(self, period="1y", max_retries=3):
        """Fetch Nifty 50 data from Yahoo Finance with retry logic"""
        for attempt in range(max_retries):
            try:
                logger.info(f"Fetching Nifty 50 data (attempt {attempt + 1}/{max_retries})")
                ticker = yf.Ticker(self.symbol)
                self.data = ticker.history(period=period)
                
                if self.data.empty:
                    raise ValueError("No data received from Yahoo Finance")
                    
                logger.info(f"Data fetched successfully. Shape: {self.data.shape}")
                return True
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error("All fetch attempts failed")
                    return False
                
        return False
    
    def calculate_moving_averages(self):
        """Calculate moving averages as per research paper methodology"""
        if self.data is None:
            logger.error("No data available. Please fetch data first.")
            return False
            
        try:
            # Simple Moving Averages
            self.data['5DMA'] = self.data['Close'].rolling(window=5).mean()
            self.data['50DMA'] = self.data['Close'].rolling(window=50).mean() 
            self.data['200DMA'] = self.data['Close'].rolling(window=200).mean()
            
            # Exponential Moving Average (5-day)
            self.data['5DEMA'] = self.data['Close'].ewm(span=5, adjust=False).mean()
            
            # Calculate additional indicators
            self.data['Volume_SMA'] = self.data['Volume'].rolling(window=20).mean()
            self.data['Price_Change'] = self.data['Close'].pct_change()
            self.data['Volatility'] = self.data['Price_Change'].rolling(window=20).std() * np.sqrt(252)
            
            logger.info("Moving averages calculated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error calculating moving averages: {str(e)}")
            return False
    
    def generate_signals(self):
        """Generate trading signals based on moving average analysis"""
        if self.data is None:
            return False
            
        try:
            latest = self.data.iloc[-1]
            previous = self.data.iloc[-2]
            
            signals = {
                'date': latest.name.strftime('%Y-%m-%d'),
                'close_price': round(latest['Close'], 2),
                'volume': int(latest['Volume']) if not pd.isna(latest['Volume']) else 0,
                'volatility': round(latest['Volatility'], 2) if not pd.isna(latest['Volatility']) else 0,
                'short_term': self.analyze_short_term(latest, previous),
                'medium_term': self.analyze_medium_term(latest, previous),
                'long_term': self.analyze_long_term(latest, previous),
                'overall_trend': None
            }
            
            # Determine overall trend
            signals['overall_trend'] = self.determine_overall_trend(signals)
            
            self.results = signals
            return True
            
        except Exception as e:
            logger.error(f"Error generating signals: {str(e)}")
            return False
    
    def analyze_short_term(self, latest, previous):
        """Analyze short-term trend using 5DMA and 5DEMA"""
        close = latest['Close']
        dma_5 = latest['5DMA']
        ema_5 = latest['5DEMA']
        
        prev_dma_5 = previous['5DMA']
        prev_ema_5 = previous['5DEMA']
        
        signal = "NEUTRAL"
        strength = 0
        
        # Price vs MA analysis
        above_ma = (close > dma_5) and (close > ema_5)
        below_ma = (close < dma_5) and (close < ema_5)
        
        # Momentum analysis
        ma_rising = (dma_5 > prev_dma_5) and (ema_5 > prev_ema_5)
        ma_falling = (dma_5 < prev_dma_5) and (ema_5 < prev_ema_5)
        
        if above_ma and ma_rising:
            signal = "BUY"
            strength = 2
        elif above_ma or ma_rising:
            signal = "BUY"
            strength = 1
        elif below_ma and ma_falling:
            signal = "SELL"
            strength = 2
        elif below_ma or ma_falling:
            signal = "SELL"
            strength = 1
            
        return {
            'signal': signal,
            'strength': strength,
            'price_vs_5dma': round(((close / dma_5) - 1) * 100, 2) if not pd.isna(dma_5) else 0,
            'price_vs_5ema': round(((close / ema_5) - 1) * 100, 2) if not pd.isna(ema_5) else 0,
            'ma_values': {
                '5DMA': round(dma_5, 2) if not pd.isna(dma_5) else 0, 
                '5DEMA': round(ema_5, 2) if not pd.isna(ema_5) else 0
            }
        }
    
    def analyze_medium_term(self, latest, previous):
        """Analyze medium-term trend using 50DMA"""
        close = latest['Close']
        dma_50 = latest['50DMA']
        prev_dma_50 = previous['50DMA']
        
        signal = "NEUTRAL"
        strength = 0
        
        if pd.isna(dma_50) or pd.isna(prev_dma_50):
            return {
                'signal': signal,
                'strength': strength,
                'price_vs_50dma': 0,
                'ma_trend': 0,
                'ma_values': {'50DMA': 0}
            }
        
        price_vs_ma = (close / dma_50) - 1
        ma_trend = (dma_50 / prev_dma_50) - 1
        
        if close > dma_50 and ma_trend > 0:
            signal = "BUY"
            strength = 2 if price_vs_ma > 0.02 else 1
        elif close > dma_50:
            signal = "BUY"
            strength = 1
        elif close < dma_50 and ma_trend < 0:
            signal = "SELL"
            strength = 2 if price_vs_ma < -0.02 else 1
        elif close < dma_50:
            signal = "SELL"
            strength = 1
            
        return {
            'signal': signal,
            'strength': strength,
            'price_vs_50dma': round(price_vs_ma * 100, 2),
            'ma_trend': round(ma_trend * 100, 2),
            'ma_values': {'50DMA': round(dma_50, 2)}
        }
    
    def analyze_long_term(self, latest, previous):
        """Analyze long-term trend using 200DMA"""
        close = latest['Close']
        dma_200 = latest['200DMA']
        prev_dma_200 = previous['200DMA']
        
        signal = "NEUTRAL"
        strength = 0
        
        if pd.isna(dma_200) or pd.isna(prev_dma_200):
            return {
                'signal': signal,
                'strength': strength,
                'price_vs_200dma': 0,
                'ma_trend': 0,
                'ma_values': {'200DMA': 0}
            }
        
        price_vs_ma = (close / dma_200) - 1
        ma_trend = (dma_200 / prev_dma_200) - 1
        
        if close > dma_200 and ma_trend > 0:
            signal = "BUY"
            strength = 2 if price_vs_ma > 0.05 else 1
        elif close > dma_200:
            signal = "BUY"  
            strength = 1
        elif close < dma_200 and ma_trend < 0:
            signal = "SELL"
            strength = 2 if price_vs_ma < -0.05 else 1
        elif close < dma_200:
            signal = "SELL"
            strength = 1
            
        return {
            'signal': signal,
            'strength': strength,
            'price_vs_200dma': round(price_vs_ma * 100, 2),
            'ma_trend': round(ma_trend * 100, 2),
            'ma_values': {'200DMA': round(dma_200, 2)}
        }
    
    def determine_overall_trend(self, signals):
        """Determine overall market trend based on all timeframes"""
        short = signals['short_term']['signal']
        medium = signals['medium_term']['signal']
        long = signals['long_term']['signal']
        
        buy_signals = [short, medium, long].count('BUY')
        sell_signals = [short, medium, long].count('SELL')
        
        if buy_signals >= 2:
            return "BULLISH"
        elif sell_signals >= 2:
            return "BEARISH"
        else:
            return "NEUTRAL"
    
    def calculate_support_resistance(self):
        """Calculate support and resistance levels"""
        if self.data is None:
            return {'resistance': [], 'support': []}
            
        try:
            # Use recent 50 days for S/R calculation
            recent_data = self.data.tail(50).copy()
            
            # Calculate pivot points
            recent_data['Pivot_High'] = recent_data['High'].rolling(window=5, center=True).max()
            recent_data['Pivot_Low'] = recent_data['Low'].rolling(window=5, center=True).min()
            
            resistance_levels = []
            support_levels = []
            
            for i in range(2, len(recent_data) - 2):
                current_high = recent_data.iloc[i]['High']
                current_low = recent_data.iloc[i]['Low']
                
                # Check for pivot highs and lows
                if (current_high > recent_data.iloc[i-2:i+3]['High'].drop(recent_data.index[i]).max()):
                    resistance_levels.append(current_high)
                
                if (current_low < recent_data.iloc[i-2:i+3]['Low'].drop(recent_data.index[i]).min()):
                    support_levels.append(current_low)
            
            # Sort and get top 3 levels
            resistance_levels = sorted(set(resistance_levels), reverse=True)[:3]
            support_levels = sorted(set(support_levels))[-3:]
            
            return {
                'resistance': [round(float(r), 2) for r in resistance_levels],
                'support': [round(float(s), 2) for s in support_levels]
            }
            
        except Exception as e:
            logger.error(f"Error calculating support/resistance: {str(e)}")
            return {'resistance': [], 'support': []}
    
    def get_recommendation(self):
        """Get investment recommendation based on analysis"""
        if not self.results:
            return "Unable to generate recommendation"
            
        trend = self.results['overall_trend']
        short_strength = self.results['short_term']['strength']
        medium_strength = self.results['medium_term']['strength']
        long_strength = self.results['long_term']['strength']
        
        total_strength = short_strength + medium_strength + long_strength
        
        if trend == "BULLISH" and total_strength >= 5:
            return "STRONG BUY"
        elif trend == "BULLISH" and total_strength >= 3:
            return "BUY"
        elif trend == "BULLISH":
            return "WEAK BUY"
        elif trend == "BEARISH" and total_strength >= 5:
            return "STRONG SELL"
        elif trend == "BEARISH" and total_strength >= 3:
            return "SELL"  
        elif trend == "BEARISH":
            return "WEAK SELL"
        else:
            return "HOLD"
    
    def assess_risk(self):
        """Assess current market risk level"""
        if not self.results:
            return {"level": "UNKNOWN", "volatility": 0}
            
        volatility = self.results.get('volatility', 0)
        
        if volatility > 30:
            risk_level = "HIGH"
        elif volatility > 20:
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"
            
        return {
            'level': risk_level,
            'volatility': volatility
        }
    
    def generate_web_report(self):
        """Generate report data for web display"""
        if not self.results:
            logger.error("No analysis results available")
            return None
            
        try:
            sr_levels = self.calculate_support_resistance()
            
            report = {
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'market_data': {
                    'symbol': 'NIFTY 50',
                    'current_price': self.results['close_price'],
                    'volume': self.results['volume'],
                    'volatility': self.results['volatility'],
                    'date': self.results['date']
                },
                'technical_analysis': self.results,
                'support_resistance': sr_levels,
                'recommendation': self.get_recommendation(),
                'risk_assessment': self.assess_risk()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return None

def main():
    """Main execution function for web deployment"""
    logger.info("Starting Nifty 50 Web Analysis")
    
    try:
        # Initialize analyzer
        analyzer = NiftyWebAnalyzer()
        
        # Fetch data
        if not analyzer.fetch_data():
            logger.error("Failed to fetch data")
            return False
        
        # Calculate indicators
        if not analyzer.calculate_moving_averages():
            logger.error("Failed to calculate moving averages")
            return False
        
        # Generate signals
        if not analyzer.generate_signals():
            logger.error("Failed to generate signals")
            return False
        
        # Generate report
        report = analyzer.generate_web_report()
        if not report:
            logger.error("Failed to generate report")
            return False
        
        # Create HTML page content (will be generated by separate function)
        # Save JSON data for the HTML template
        with open('data.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info("Web data generated successfully")
        print(f"Analysis complete: {report['recommendation']} - {report['technical_analysis']['overall_trend']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
'''

# Save the web main script
with open('main_web.py', 'w') as f:
    f.write(web_main_script)

print("✅ Created main_web.py - Web-based analysis engine")