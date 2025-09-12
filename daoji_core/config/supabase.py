from pydantic import Field, PostgresDsn

from .base import BaseConfig


class SupabaseConfig(BaseConfig):
    SUPABASE_URL: str = Field(..., description="Supabase URL")
    SUPABASE_SERCET_KEY: str = Field(..., description="Supabase Secret Key")
    SUPABASE_ANNO_KEY: str = Field(..., description="Supabase Anno Key")
    SUPABASE_PROJECT_ID: str = Field(..., description="Supabase Project ID")

    # postgres 配置
    SUPABASE_USER: str | None = Field(None, description="Supabase User")
    SUPABASE_PASSWORD: str | None = Field(None, description="Supabase Password")
    SUPABASE_HOST: str | None = Field(None, description="Supabase Host")
    SUPABASE_PORT: int | None = Field(None, description="Supabase Port")
    SUPABASE_DBNAME: str | None = Field(None, description="Supabase DB Name")

    @property
    def postgres_url(self) -> PostgresDsn | None:
        if not any(
            [self.SUPABASE_USER, self.SUPABASE_PASSWORD, self.SUPABASE_HOST, self.SUPABASE_PORT, self.SUPABASE_DBNAME]
        ):
            return None

        return PostgresDsn.build(
            scheme="postgresql",
            username=self.SUPABASE_USER,
            password=self.SUPABASE_PASSWORD,
            host=self.SUPABASE_HOST,
            port=self.SUPABASE_PORT,
            path=f"/{self.SUPABASE_DBNAME}",
        )
