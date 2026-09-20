from sqlmodel import Field, SQLModel


class ClienteAPI(SQLModel, table = True):
    client_id: str = Field(primary_key = True)
    hashed_secret: str
    scopes_csv: str

    def scopes(self) -> list[str]:
        return self.scopes_csv.split(",") if self.scopes_csv else []
