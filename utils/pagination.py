def paginate(data, page, page_size):
    # Ensure the data is in the right format (list or dictionary with 'records' key)
    if isinstance(data, dict):
        if 'records' in data:
            data = data['records']
        elif 'data' in data and 'records' in data['data']:
            data = data['data']['records']
    
    if not isinstance(data, list):
        raise TypeError("Data must be either a list or a dictionary with 'records' key.")
    
    # Perform pagination
    start = (page - 1) * page_size
    end = start + page_size
    paginated_records = data[start:end]
    paginated_total = len(paginated_records)  # <- changed this

    return {
        "code": 1,
        "msg": "Success",
        "data": {
            "records": paginated_records,
            "total": paginated_total  # Total number of records returned now
        }
    }
