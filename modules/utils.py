def split_genres(genre_str):
    """Split genres separated by |"""
    if isinstance(genre_str, str):
        return genre_str.split('|')
    return []
