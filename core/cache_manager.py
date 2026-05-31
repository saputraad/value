from pathlib import Path
import joblib
import time

CACHE_DIR = Path("cache")

CACHE_DIR.mkdir(
    exist_ok=True
)


class CacheManager:

    @staticmethod
    def cache_path(key):

        return CACHE_DIR / f"{key}.pkl"

    @staticmethod
    def save(
        key,
        data
    ):

        path = CacheManager.cache_path(
            key
        )

        payload = {

            "timestamp":
                time.time(),

            "data":
                data
        }

        joblib.dump(
            payload,
            path
        )

    @staticmethod
    def load(
        key,
        max_age_hours=24
    ):

        path = CacheManager.cache_path(
            key
        )

        if not path.exists():

            return None

        try:

            payload = joblib.load(
                path
            )

            age = (
                time.time()
                -
                payload["timestamp"]
            )

            if age > (
                max_age_hours * 3600
            ):

                return None

            return payload["data"]

        except:

            return None

    @staticmethod
    def clear():

        for file in CACHE_DIR.glob(
            "*.pkl"
        ):

            file.unlink()