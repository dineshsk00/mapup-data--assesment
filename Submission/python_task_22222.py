import pandas as pd

def calculate_distance_matrix(file_path):
    
    data = pd.read_csv(file_path)

    
    unique_ids = sorted(list(set(data['ID1'].unique()) | set(data['ID2'].unique())))
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids)

    
    distance_matrix.values[[range(len(unique_ids))]*2] = 0

    
    for idx, row in data.iterrows():
        id1, id2, distance = row['ID1'], row['ID2'], row['Distance']
        distance_matrix.loc[id1, id2] = distance
        distance_matrix.loc[id2, id1] = distance  # Making it symmetric

   
    for i in unique_ids:
        for j in unique_ids:
            for k in unique_ids:
                if pd.notnull(distance_matrix.loc[i, k]) and pd.notnull(distance_matrix.loc[k, j]):
                    if pd.isnull(distance_matrix.loc[i, j]):
                        distance_matrix.loc[i, j] = distance_matrix.loc[i, k] + distance_matrix.loc[k, j]
                    else:
                        distance_matrix.loc[i, j] = min(distance_matrix.loc[i, j],
                                                         distance_matrix.loc[i, k] + distance_matrix.loc[k, j])

    return distance_matrix.astype(float)

result_df = calculate_distance_matrix('dataset-3.csv')
print(result_df)





def unroll_distance_matrix(df):
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame): Input DataFrame containing distance matrix.

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_data = []

    for idx, row in df.iterrows():
        id_start = idx
        for col in df.columns:
            if idx != col and not pd.isnull(row[col]):
                unrolled_data.append({'id_start': idx, 'id_end': col, 'distance': df.loc[idx, col]})

    unrolled_df = pd.DataFrame(unrolled_data, columns=['id_start', 'id_end', 'distance'])
    return unrolled_df


unrolled_distances = unroll_distance_matrix(result_df)
print(unrolled_distances)



def find_ids_within_ten_percentage_threshold(df, reference_id):
   
  
    # Calculate the average distance for the reference_id
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()

    # Calculate the lower and upper bounds for the threshold (within 10%)
    lower_bound = reference_avg_distance - (0.1 * reference_avg_distance)
    upper_bound = reference_avg_distance + (0.1 * reference_avg_distance)

    # Filter IDs whose average distance falls within the specified threshold
    within_threshold_ids = df.groupby('id_start')['distance'].mean()
    within_threshold_ids = within_threshold_ids[(within_threshold_ids >= lower_bound) & (within_threshold_ids <= upper_bound)]
    
    # Sort and return the resulting DataFrame
    result_df = pd.DataFrame(within_threshold_ids).reset_index().sort_values('id_start')
    return result_df


reference_id = 123  
result_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_distances, reference_id)
print(result_within_threshold)





import pandas as pd

def calculate_toll_rate(df):
    
    # Define rate coefficients for each vehicle type
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Calculate toll rates for each vehicle type based on distance
    for vehicle_type, rate in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate

    return df
result_with_toll_rates = calculate_toll_rate(unrolled_distances)
print(result_with_toll_rates)



import datetime

def calculate_time_based_toll_rates(df):
    
    weekday_time_ranges = [
        (datetime.time(0, 0, 0), datetime.time(10, 0, 0), 0.8),
        (datetime.time(10, 0, 0), datetime.time(18, 0, 0), 1.2),
        (datetime.time(18, 0, 0), datetime.time(23, 59, 59), 0.8)
    ]
    weekend_time_range = (datetime.time(0, 0, 0), datetime.time(23, 59, 59), 0.7)

    # Create empty lists to store the updated rows
    updated_rows = []

    # Iterate through each row in the DataFrame
    for idx, row in df.iterrows():
        # Extract the start and end days
        start_day = "Monday"  # Replace with actual day value (from Monday to Sunday)
        end_day = "Sunday"    # Replace with actual day value (from Monday to Sunday)

        # Iterate through each time range based on weekdays or weekends
        for time_range in weekday_time_ranges if start_day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] else [weekend_time_range]:
            start_time, end_time, discount_factor = time_range

            # Create a copy of the row and update vehicle columns based on time ranges
            updated_row = row.copy()
            for vehicle_type in ['moto', 'car', 'rv', 'bus', 'truck']:
                if start_time <= row['start_time'] <= end_time:
                    updated_row[vehicle_type] *= discount_factor

            # Append the updated row with time-based toll rates to the list
            updated_row['start_day'] = start_day
            updated_row['end_day'] = end_day
            updated_row['start_time'] = start_time
            updated_row['end_time'] = end_time
            updated_rows.append(updated_row)

    # Create a DataFrame from the updated rows and return the result
    result_df = pd.DataFrame(updated_rows)
    return result_df


result_with_time_based_toll_rates = calculate_time_based_toll_rates(unrolled_distances)
print(result_with_time_based_toll_rates)

