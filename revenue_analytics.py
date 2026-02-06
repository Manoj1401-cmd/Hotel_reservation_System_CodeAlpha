import pandas as pd
import matplotlib.pyplot as plt
from db_config import DatabaseConnection

class RevenueAnalytics:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_monthly_revenue(self, year):
        query = f"""
        SELECT 
            MONTH(payment_date) as month,
            MONTHNAME(payment_date) as month_name,
            SUM(amount) as total_revenue,
            COUNT(payment_id) as total_transactions
        FROM payments
        WHERE YEAR(payment_date) = {year}
        AND payment_status = 'COMPLETED'
        GROUP BY MONTH(payment_date), MONTHNAME(payment_date)
        ORDER BY month;
        """
        return self.db.fetch_data(query)
    
    def get_revenue_by_room_type(self):
        query = """
        SELECT 
            rt.type_name,
            COUNT(r.reservation_id) as bookings,
            SUM(p.amount) as total_revenue,
            ROUND(AVG(p.amount), 2) as avg_revenue_per_booking
        FROM payments p
        JOIN reservations r ON p.reservation_id = r.reservation_id
        JOIN rooms rm ON r.room_id = rm.room_id
        JOIN room_types rt ON rm.room_type_id = rt.room_type_id
        WHERE p.payment_status = 'COMPLETED'
        GROUP BY rt.type_name;
        """
        return self.db.fetch_data(query)
    
    def plot_monthly_revenue(self, year):
        df = self.get_monthly_revenue(year)
        
        if df is not None and not df.empty:
            plt.figure(figsize=(12, 6))
            plt.bar(df['month_name'], df['total_revenue'], color='skyblue', edgecolor='navy')
            plt.title(f'Monthly Revenue for {year}', fontsize=16, fontweight='bold')
            plt.xlabel('Month', fontsize=12)
            plt.ylabel('Revenue (₹)', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.savefig('monthly_revenue.png')
            print(f"Monthly revenue chart saved as 'monthly_revenue.png'")
            plt.show()
        else:
            print("No revenue data available")
    
    def generate_revenue_report(self, year):
        monthly_df = self.get_monthly_revenue(year)
        room_type_df = self.get_revenue_by_room_type()
        
        print(f"\n{'='*60}")
        print(f"REVENUE REPORT - {year}")
        print(f"{'='*60}\n")
        
        if monthly_df is not None and not monthly_df.empty:
            print("Monthly Revenue Summary:")
            print(monthly_df.to_string(index=False))
            print(f"\nTotal Annual Revenue: ₹{monthly_df['total_revenue'].sum():,.2f}")
        
        if room_type_df is not None and not room_type_df.empty:
            print(f"\n{'='*60}")
            print("Revenue by Room Type:")
            print(room_type_df.to_string(index=False))

# Usage Example
if __name__ == "__main__":
    revenue = RevenueAnalytics()
    
    current_year = 2024
    revenue.plot_monthly_revenue(current_year)
    revenue.generate_revenue_report(current_year)
