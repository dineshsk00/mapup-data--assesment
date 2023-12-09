import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
   pivot_df = df.pivot(index='id_1', columns='id_2', values='car')
   for i in range(min(pivot_df.shape)):
        pivot_df.iloc[i, i] = 0.0
   return df


def get_type_count(df)->dict:
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25) ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.np.select(conditions, choices, default='Unknown')
    type_count = df['car_type'].value_counts().to_dict()
    dict= dict(sorted(type_count.items()))
    return dict()


def get_bus_indexes(df)->list:
    mean_bus = df['bus'].mean()
    list = df[df['bus'] > 2 * mean_bus].index.tolist()
    list.sort()
    
    return list()


def filter_routes(df)->list:
    route_avg_truck = df.groupby('route')['truck'].mean()
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    filtered_routes.sort()
    return filtered_routes


def multiply_matrix(matrix)->pd.DataFrame:
    modified_matrix = matrix.copy()
    for index, row in modified_matrix.iterrows():
        for col in modified_matrix.columns:
            value = modified_matrix.at[index, col]
            if value > 20:
                modified_matrix.at[index, col] = round(value * 0.75, 1)   
            else:
                modified_matrix.at[index, col] = round(value * 1.25, 1)   
    
    return modified_matrix
    

   


def time_check(df)->pd.Series:
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['duration_hours'] = (df['end_datetime'] - df['start_datetime']).dt.total_seconds() / 3600
    result = df.groupby(['id', 'id_2']).apply(lambda x: (
        x['duration_hours'].sum() >= 168  # Check if spans all 7 days (168 hours in a week)
        and (x['start_datetime'].min().time() == pd.Timestamp('00:00:00').time())  # Check if starts at 12:00:00 AM
        and (x['end_datetime'].max().time() == pd.Timestamp('23:59:59').time())  # Check if ends at 11:59:59 PM
    ))

    return result




