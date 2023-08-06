from joblib import Memory
from pydantic import BaseSettings


class SettingsGCS(BaseSettings):
    name_bucket: str
    name_project: str
    name_folder_cache: str = "cache"
    verbosity: int = 0

    class Config:
        env_prefix = "gcs_"

    @property
    def memory(self) -> Memory:
        return Memory(
            f"{self.name_bucket}/{self.name_folder_cache}",
            backend="gcs",
            verbose=self.verbosity,
            backend_options={"project": self.name_project},
        )