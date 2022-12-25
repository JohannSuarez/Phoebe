from pydantic import BaseModel

class PKCEItemBase(BaseModel):
    state: str

class PKCEItemCreate(PKCEItemBase):
    code_verifier: str

class PKCEItem(PKCEItemBase):
    code_verifier: str

    class Config:
        orm_mode = True
