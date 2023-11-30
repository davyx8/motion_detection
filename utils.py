@staticmethod
def clear_queue(queue, num_to_clear):
    for _ in range(num_to_clear):
        try:
            queue.get_nowait()
        except Exception as e:
            break
def clear_queue(queue, num_to_clear=1):
    while not queue.empty():
        try:
            queue.get_nowait()
        except Exception as e:
            break

