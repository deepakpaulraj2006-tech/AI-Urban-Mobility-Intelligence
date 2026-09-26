from src.data_generation import generate_data
def test_generated_data():
    df=generate_data(100,42); assert len(df)==100; assert df.congestion_level.isin(['Low','Medium','High']).all(); assert df.vehicle_count.notna().all()
