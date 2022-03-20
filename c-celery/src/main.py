from datetime import datetime, timedelta
from random import randint

from tasks import wait_required_seconds


def run():
    for _ in range(5):
        """                
        Calling API
            .delay => Shortcut to send a task message, but does’t support execution options.
            .apply_async => Sends a task message, support execution options.
        """
        print(wait_required_seconds.delay(n=randint(1, 5)))
        print(wait_required_seconds.apply_async(kwargs={"n": randint(1, 5)}))


if __name__ == '__main__':
    # run()

    # Countdown
    print(wait_required_seconds.apply_async(args=[randint(1, 5)], countdown=5))

    # ETA
    # eta = datetime.utcnow() + timedelta(seconds=20)
    # print(wait_required_seconds.apply_async(args=[randint(1, 5)], eta=eta))

    # Expiration
    # print(wait_required_seconds.apply_async(args=[randint(10, 20)], countdown=10, expires=5))
