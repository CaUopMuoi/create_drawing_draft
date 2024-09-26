def check_size_profile(value_size):
    size = str(value_size).lower()
    # list_pipe = ["pipe", "tube"]

    # nếu là ống
    if "pipe" in size or "tube" in size:
        print("là ống")
        return "pipe"
    else:
        print("là thép tấm")
        return "plate"