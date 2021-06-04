def str2mdown(str):
    return str.replace("-", "\\-").replace("!", "\\!").replace(".", "\\.")
