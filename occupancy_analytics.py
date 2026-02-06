import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from db_config import DatabaseConnection

class OccupancyAnalytics:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_occupancy_rate(self, start_date, end_date):
        query = f"""
        SELECT 
            DATE(check_in_date) as date,
            COUNT(DISTINCT room_id) as occupied_rooms,
            (SELECT COUNT(*) FROM rooms) as total_rooms,
            ROUND((COUNT(DISTINCT room_id) / (SELECT COUNT(*) FROM rooms) * 100), 2) as occupancy_rate
        FROM reservations
        WHERE status IN ('CONFIRMED', 'COMPLETED')
        AND check_in_date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY DATE(check_in_date)
        ORDER BY date;
        """
        return self.db.fetch_data(query)
    
    def plot_occupancy_trend(self, start_date, end_date):
        df = self.get_occupancy_rate(start_date, end_date)
        
        if df is not None and not df.empty:
            plt.figure(figsize=(12, 6))
            plt.plot(df['date'], df['occupancy_rate'], marker='o', linewidth=2)
            plt.title('Hotel Occupancy Rate Trend', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Occupancy Rate (%)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('occupancy_trend.png')
            print("Occupancy trend chart saved as 'occupancy_trend.png'")
            plt.show()
        else:
            print("No data available for the given date range")
    
    def get_room_type_occupancy(self):
        query = """
        SELECT 
            rt.type_name,
            COUNT(DISTINCT r.reservation_id) as total_bookings,
            ROUND(AVG(DATEDIFF(r.check_out_date, r.check_in_date)), 2) as avg_stay_duration
        FROM reservations r
        JOIN rooms rm ON r.room_id = rm.room_id
        JOIN room_types rt ON rm.room_type_id = rt.room_type_id
        WHERE r.status IN ('CONFIRMED', 'COMPLETED')
        GROUP BY rt.type_name;
        """
        return self.db.fetch_data(query)

# Usage Example
if __name__ == "__main__":
    analytics = OccupancyAnalytics()
    
    # Get occupancy for last 30 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    analytics.plot_occupancy_trend(start_date, end_date)
    
    room_occupancy = analytics.get_room_type_occupancy()
    print("\nRoom Type Occupancy:")
    print(room_occupancy)
