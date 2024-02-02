def truncate_text(text, max_length):
    """
    Truncate a text to a maximum number of characters, adding an ellipsis if the text is too long.

    Args:
    text (str): The text to be truncated.
    max_length (int): The maximum length of the text including the ellipsis.

    Returns:
    str: The truncated text.
    """
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    else:
        return text
