import monitor


def main():
    # WARNING! Debug mode means the server will accept arbitrary Python code!
    monitor.app.run('0.0.0.0', 5000, debug=True)
