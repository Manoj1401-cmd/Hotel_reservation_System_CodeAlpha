from occupancy_analytics import OccupancyAnalytics
from revenue_analytics import RevenueAnalytics
from booking_analytics import BookingAnalytics
from datetime import datetime, timedelta

def main():
    print("="*70)
    print("HOTEL RESERVATION SYSTEM - ANALYTICS DASHBOARD")
    print("="*70)
    
    # Occupancy Analytics
    print("\n[1] Generating Occupancy Reports...")
    occupancy = OccupancyAnalytics()
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    occupancy.plot_occupancy_trend(start_date, end_date)
    
    # Revenue Analytics
    print("\n[2] Generating Revenue Reports...")
    revenue = RevenueAnalytics()
    current_year = datetime.now().year
    revenue.plot_monthly_revenue(current_year)
    revenue.generate_revenue_report(current_year)
    
    # Booking Analytics
    print("\n[3] Generating Booking Pattern Reports...")
    booking = BookingAnalytics()
    booking.plot_booking_patterns()
    
    print("\n" + "="*70)
    print("All reports generated successfully!")
    print("="*70)

if __name__ == "__main__":
    main()
