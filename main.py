#!/usr/bin/env python3
"""
Main entry point for the Multi-Platform E-commerce Scraper.
Clean, professional interface for Malaysian market analysis.
Focused on finding best-selling affordable items.
"""

import os
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Any

from config import get_config, SUPPORTED_PLATFORMS, MESSAGES, OUTPUT_DIRS
from logger import get_logger, log_configuration
from multi_platform_scraper import MultiPlatformScraper
from advanced_analyzer import AdvancedAnalyzer


def setup_output_directories():
    """Create necessary output directories."""
    for dir_name in OUTPUT_DIRS.values():
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)


def display_banner():
    """Display application banner."""
    print("=" * 60)
    print("  MULTI-PLATFORM E-COMMERCE SCRAPER")
    print("  Malaysian Market - Best Seller Analyzer")
    print("  Find Top 50 Best-Selling Items Under RM 50")
    print("=" * 60)
    print()


def display_supported_platforms():
    """Display supported platforms."""
    print("Supported platforms:")
    for platform, config in SUPPORTED_PLATFORMS.items():
        status = "✓ Active" if config['enabled'] else "✗ Disabled"
        print(f"  • {config['name']} ({platform}) - {status}")
    print()


def search_products_interactive():
    """Interactive product search mode."""
    logger = get_logger(__name__)
    scraper = MultiPlatformScraper()
    
    print("\n=== PENCARIAN PRODUK INTERAKTIF ===\n")
    
    while True:
        try:
            # Get search parameters
            keyword = input("Masukkan kata kunci pencarian (atau 'quit' untuk keluar): ").strip()
            if keyword.lower() in ['quit', 'exit', 'q']:
                break
            
            if not keyword:
                print("Kata kunci tidak boleh kosong!")
                continue
            
            # Get platform selection
            print("\nPilih platform:")
            print("1. Semua platform")
            print("2. Shopee saja")
            print("3. Tokopedia saja") 
            print("4. Lazada saja")
            print("5. Platform khusus")
            
            choice = input("Pilihan (1-5): ").strip()
            
            # Get result limit
            try:
                limit = int(input("Jumlah hasil per platform (default 20): ") or "20")
            except ValueError:
                limit = 20
            
            # Perform search based on selection
            if choice == "1":
                print(f"\n{MESSAGES['search_started']}")
                results = scraper.search_all_platforms(keyword, limit)
            elif choice == "2":
                results = scraper.search_specific_platforms(keyword, ['shopee'], limit)
            elif choice == "3":
                results = scraper.search_specific_platforms(keyword, ['lazada'], limit)
            elif choice == "4":
                results = scraper.search_specific_platforms(keyword, ['mudah'], limit)
            elif choice == "5":
                platforms = input("Enter platforms (shopee,lazada,mudah): ").split(',')
                platforms = [p.strip() for p in platforms]
                results = scraper.search_specific_platforms(keyword, platforms, limit)
            else:
                print("Pilihan tidak valid!")
                continue
            
            # Display results summary
            display_search_results(results)
            
            # Offer analysis
            if any(results.values()):
                analyze = input("\nApakah Anda ingin melakukan analisis? (y/n): ").lower() == 'y'
                if analyze:
                    perform_analysis(results, keyword, scraper)
            
            # Offer export
            export = input("\nApakah Anda ingin mengekspor hasil? (y/n): ").lower() == 'y'
            if export:
                export_results(results, keyword, scraper)
            
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nProgram dihentikan oleh pengguna.")
            break
        except Exception as e:
            logger.error(f"Error in interactive mode: {str(e)}")
            print(f"Terjadi kesalahan: {str(e)}")


def display_search_results(results: Dict[str, List[Dict]]):
    """Display search results summary."""
    print(f"\n{MESSAGES['search_completed']}")
    print("\nRingkasan Hasil:")
    print("-" * 30)
    
    total_products = 0
    for platform, products in results.items():
        count = len(products)
        total_products += count
        print(f"  {SUPPORTED_PLATFORMS.get(platform, {}).get('name', platform)}: {count} produk")
    
    print(f"\nTotal: {total_products} produk ditemukan")
    
    if total_products > 0:
        # Show sample products
        print("\nContoh produk ditemukan:")
        print("-" * 25)
        count = 0
        for platform, products in results.items():
            for product in products[:3]:  # Show first 3 from each platform
                if count >= 5:  # Limit total samples
                    break
                print(f"  • {product.get('name', 'N/A')[:50]}...")
                print(f"    Platform: {platform} | Price: RM {product.get('price', 0):,.2f} | Sold: {product.get('sold', 0)}")
                count += 1
            if count >= 5:
                break
        if total_products > 5:
            print(f"    ... dan {total_products - 5} produk lainnya")


def perform_analysis(results: Dict, keyword: str, scraper: MultiPlatformScraper):
    """Perform analysis on search results."""
    logger = get_logger(__name__)
    analyzer = AdvancedAnalyzer()
    
    print(f"\n{MESSAGES['analysis_started']}")
    
    # Prepare combined data
    all_products = []
    for platform, products in results.items():
        for product in products:
            product['platform'] = platform
            all_products.append(product)
    
    if not all_products:
        print(MESSAGES['no_results'])
        return
    
    try:
        # Perform comprehensive analysis
        analysis = analyzer.analyze_products(all_products)
        platform_comparison = analyzer.compare_platforms(all_products)
        
        # Display analysis results
        print(f"\n{MESSAGES['analysis_completed']}")
        print("\nHasil Analisis:")
        print("=" * 20)
        
        # Price analysis
        if 'price_analysis' in analysis:
            price_data = analysis['price_analysis']
            print(f"\nPrice Analysis:")
            print(f"  Average: RM {price_data.get('average_price', 0):,.2f}")
            print(f"  Lowest: RM {price_data.get('min_price', 0):,.2f}")
            print(f"  Highest: RM {price_data.get('max_price', 0):,.2f}")
        
        # Rating analysis
        if 'rating_analysis' in analysis:
            rating_data = analysis['rating_analysis']
            print(f"\nRating Analysis:")
            print(f"  Average: {rating_data.get('average_rating', 0):.1f}/5.0")
            print(f"  High rated products (>4.0): {rating_data.get('high_rated_count', 0)}")
        
        # Platform comparison
        if platform_comparison and 'platform_metrics' in platform_comparison:
            print(f"\nPlatform Comparison:")
            for platform, metrics in platform_comparison['platform_metrics'].items():
                platform_name = SUPPORTED_PLATFORMS.get(platform, {}).get('name', platform)
                print(f"  {platform_name}: Score {metrics.get('score', 0):.1f}/100")
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        print(f"Analisis gagal: {str(e)}")


def export_results(results: Dict, keyword: str, scraper: MultiPlatformScraper):
    """Export results to file."""
    print(f"\n{MESSAGES['export_started']}")
    
    print("Format ekspor:")
    print("1. JSON")
    print("2. CSV") 
    print("3. TXT (Laporan)")
    
    choice = input("Pilih format (1-3): ").strip()
    format_map = {'1': 'json', '2': 'csv', '3': 'txt'}
    format_type = format_map.get(choice, 'json')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"hasil_pencarian_{keyword.replace(' ', '_')}_{timestamp}.{format_type}"
    
    # Prepare export data
    export_data = {
        'keyword': keyword,
        'timestamp': timestamp,
        'results': results,
        'summary': {
            'total_platforms': len(results),
            'total_products': sum(len(products) for products in results.values())
        }
    }
    
    try:
        success = scraper.export_results(export_data, format_type, filename)
        if success:
            print(f"\n{MESSAGES['export_completed']}: {filename}")
        else:
            print(f"Ekspor gagal!")
    except Exception as e:
        print(f"Ekspor gagal: {str(e)}")


def analyze_bestsellers(keyword: str, max_price: float, top_n: int, platforms: List[str], limit: int):
    """Analyze and display best-selling affordable items."""
    logger = get_logger(__name__)
    scraper = MultiPlatformScraper()
    analyzer = AdvancedAnalyzer()
    
    print(f"\n{'='*60}")
    print(f"  BEST-SELLER ANALYSIS: '{keyword}'"  )
    print(f"  Max Price: RM{max_price} | Top {top_n} Items")
    print(f"{'='*60}\n")
    
    # Search across platforms
    print(MESSAGES['search_started'])
    if platforms:
        results = scraper.search_specific_platforms(keyword, platforms, limit)
    else:
        results = scraper.search_all_platforms(keyword, limit)
    
    # Combine all products
    all_products = []
    for platform, products in results.items():
        for product in products:
            product['platform'] = platform
            all_products.append(product)
    
    if not all_products:
        print(MESSAGES['no_results'])
        return None
    
    print(f"Found {len(all_products)} total products. Analyzing...\n")
    
    # Perform best-seller analysis
    analysis = analyzer.analyze_affordable_bestsellers(all_products, max_price=max_price, top_n=top_n)
    
    if 'error' in analysis:
        print(f"Error: {analysis['error']}")
        return None
    
    # Display results
    print(f"{MESSAGES['analysis_completed']}\n")
    
    # Summary
    summary = analysis['summary']
    print(f"SUMMARY:")
    print(f"-" * 40)
    print(f"Total affordable products found: {summary['total_affordable_products']}")
    print(f"Top sellers analyzed: {summary['top_sellers_count']}")
    print(f"Price threshold: RM{summary['price_threshold']}")
    
    # Top 10 Products
    print(f"\nTOP 10 BEST-SELLING ITEMS UNDER RM{max_price}:")
    print(f"=" * 80)
    for i, product in enumerate(analysis['top_products'], 1):
        print(f"{i}. {product.get('name', 'N/A')[:60]}")
        print(f"   Price: RM{product.get('price', 0):.2f} | "
              f"Sold: {product.get('sold', 0):,} | "
              f"Rating: {product.get('rating', 0):.1f}/5.0 | "
              f"Platform: {product.get('platform', 'N/A')}")
    
    # Price metrics
    if 'price_metrics' in analysis:
        price = analysis['price_metrics']
        print(f"\nPRICE METRICS:")
        print(f"-" * 40)
        print(f"Average price: RM{price.get('average_price', 0):.2f}")
        print(f"Price range: RM{price.get('min_price', 0):.2f} - RM{price.get('max_price', 0):.2f}")
    
    # Sales metrics
    if 'sales_metrics' in analysis:
        sales = analysis['sales_metrics']
        print(f"\nSALES METRICS:")
        print(f"-" * 40)
        print(f"Total sales volume: {sales.get('total_sales', 0):,} units")
        print(f"Average sales per item: {sales.get('average_sales', 0):.0f} units")
        print(f"Bestseller threshold: {sales.get('bestseller_threshold', 0):.0f} units")
    
    # Category insights
    if 'category_insights' in analysis:
        cat_insights = analysis['category_insights']
        print(f"\nTOP CATEGORIES:")
        print(f"-" * 40)
        for category, stats in sorted(cat_insights['category_stats'].items(), 
                                      key=lambda x: x[1]['total_sales'], reverse=True)[:5]:
            print(f"{category.title()}: {stats['product_count']} items, "
                  f"{stats['total_sales']:,} total sales, "
                  f"RM{stats['avg_price']:.2f} avg price")
    
    # Recommendations
    if 'recommendations' in analysis:
        print(f"\nRECOMMENDATIONS:")
        print(f"-" * 40)
        for rec in analysis['recommendations']:
            print(f"• {rec}")
    
    return analysis



def main():
    """Main application entry point."""
    # Setup
    setup_output_directories()
    config = get_config()
    logger = get_logger(__name__)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Multi-Platform E-commerce Scraper')
    parser.add_argument('--keyword', '-k', help='Search keyword')
    parser.add_argument('--platforms', '-p', help='Comma-separated platform names')
    parser.add_argument('--limit', '-l', type=int, default=100, help='Results per platform (default: 100)')
    parser.add_argument('--export', '-e', choices=['json', 'csv', 'txt'], help='Export format')
    parser.add_argument('--output', '-o', help='Output filename')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    parser.add_argument('--max-price', type=float, default=50, help='Maximum price filter (default: RM 50)')
    parser.add_argument('--sort-by', choices=['sales', 'price', 'rating'], default='sales', 
                       help='Sort by: sales, price, or rating (default: sales)')
    parser.add_argument('--top-n', type=int, default=50, help='Number of top items to return (default: 50)')
    parser.add_argument('--bestsellers', '-b', action='store_true', 
                       help='Best seller analysis mode (find top affordable items)')
    parser.add_argument('--version', '-v', action='version', version='Multi-Platform Scraper v3.0 (Malaysian Edition)')
    
    args = parser.parse_args()
    
    # Log configuration
    log_configuration(config)
    
    # Display banner
    display_banner()
    display_supported_platforms()
    
    try:
        if args.interactive or not args.keyword:
            # Interactive mode
            search_products_interactive()
        elif args.bestsellers:
            # Best-seller analysis mode
            platforms = None
            if args.platforms:
                platforms = [p.strip() for p in args.platforms.split(',')]
            
            analysis = analyze_bestsellers(
                keyword=args.keyword,
                max_price=args.max_price,
                top_n=args.top_n,
                platforms=platforms,
                limit=args.limit
            )
            
            # Export if requested
            if analysis and args.export:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = args.output or f"bestsellers_{args.keyword.replace(' ', '_')}_{timestamp}.{args.export}"
                
                scraper = MultiPlatformScraper()
                scraper.export_results(analysis, args.export, filename)
                print(f"\nResults exported to: {filename}")
        else:
            # Command line mode (standard search)
            scraper = MultiPlatformScraper()
            
            if args.platforms:
                platforms = [p.strip() for p in args.platforms.split(',')]
                results = scraper.search_specific_platforms(args.keyword, platforms, args.limit)
            else:
                results = scraper.search_all_platforms(args.keyword, args.limit)
           
            # Display results
            display_search_results(results)
            
            # Export if requested
            if args.export:
                export_data = {
                    'keyword': args.keyword,
                    'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S'),
                    'results': results
                }
                
                filename = args.output or f"results_{args.keyword.replace(' ', '_')}.{args.export}"
                scraper.export_results(export_data, args.export, filename)
    
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        print(f"Terjadi kesalahan: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
