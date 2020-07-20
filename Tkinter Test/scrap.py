for index, row in data.iterrows():

    if row['maxf'] == row['4. close']:
        new_point = {'x': row.index, 'y': row['maxf']}
        peak_points = peak_points.append(new_point, ignore_index=True)

    if row['minf'] == row['4. close']:
        new_point = {'x': row.index, 'y': row['maxf']}
        peak_points = peak_points.append(new_point, ignore_index=True)