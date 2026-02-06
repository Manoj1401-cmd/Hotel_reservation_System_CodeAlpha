import pandas as pd
import matplotlib.pyplot as plt
from db_config import DatabaseConnection

class BookingAnalytics:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_booking_patterns(self):
        query = """
        SELECT 
            DAYNAME(created_at) as day_of_week,
            COUNT(*) as booking_count,
            ROUND(AVG(total_amount), 2) as avg_booking_value
        FROM reservations
        WHERE status IN ('CONFIRMED', 'COMPLETED')
        GROUP BY DAYNAME(created_at), DAYOFWEEK(created_at)
        ORDER BY DAYOFWEEK(created_at);
        """
        return self.db.fetch_data(query)
    
    def get_customer_statistics(self):
        query = """
        SELECT 
            COUNT(DISTINCT c.customer_id) as total_customers,
            COUNT(r.reservation_id) as total_reservations,
            ROUND(COUNT(r.reservation_id) / COUNT(DISTINCT c.customer_id), 2) as avg_bookings_per_customer,
            ROUND(AVG(r.total_amount), 2) as avg_booking_value
        FROM customers c
        LEFT JOIN reservations r ON c.customer_id = r.customer_id;
        """
        return self.db.fetch_data(query)
    
    def get_cancellation_rate(self):
        query = """
        SELECT 
            status,
            COUNT(*) as count,
            ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reservations)), 2) as percentage
        FROM reservations
        GROUP BY status;
        """
        return self.db.fetch_data(query)
    
    def plot_booking_patterns(self):
        df = self.get_booking_patterns()
        
        if df is not None and not df.empty:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            
            # Booking count by day
            ax1.bar(df['day_of_week'], df['booking_count'], color='coral')
            ax1.set_title('Bookings by Day of Week', fontweight='bold')
            ax1.set_xlabel('Day')
            ax1.set_ylabel('Number of Bookings')
            ax1.tick_params(axis='x', rotation=45)
            
            # Average booking value
            ax2.bar(df['day_of_week'], df['avg_booking_value'], color='lightgreen')
            ax2.set_title('Average Booking Value by Day', fontweight='bold')
            ax2.set_xlabel('Day')
            ax2.set_ylabel('Average Value (₹)')
            ax2.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig('booking_patterns.png')
            print("Booking patterns chart saved as 'booking_patterns.png'")
            plt.show()

# Usage Example
if __name__ == "__main__":
    analytics = BookingAnalytics()
    
    analytics.plot_booking_patterns()
    
    print("\nCustomer Statistics:")
    print(analytics.get_customer_statistics())
    
    print("\nReservation Status Distribution:")
    print(analytics.get_cancellation_rate())
