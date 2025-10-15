def format_duration(seconds):

    if seconds == 0:
        return "now"

    years = seconds // 3600 // 24 // 365
    days = seconds // 3600 // 24 % 365
    hours = (seconds // 3600) % 24
    minutes = (seconds % 3600) // 60
    seconds_rest = seconds % 60

    output_items = []
    if years > 0:
        output_items.append(f"{years} year{'s' if years > 1 else ''}")
    if days > 0:
        output_items.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        output_items.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        output_items.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds_rest > 0:
        output_items.append(f"{seconds_rest} second{'s' if seconds_rest > 1 else ''}")

    comma_separated_output = ", ".join(output_items)
    parts = comma_separated_output.rsplit(", ", 1) ## separe the last element

    return " and ".join(parts)



print(format_duration(242062374))