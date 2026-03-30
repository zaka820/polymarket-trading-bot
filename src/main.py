def main():
    # Initialize config
    config = load_config()
    
    # Start the trading bot
    trading_bot = TradingBot(config)
    trading_bot.run()

if __name__ == '__main__':
    main()