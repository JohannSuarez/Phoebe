from ..schemas.pkce import PKCEItemCreate
from ..utils.app_exceptions import AppException

from ..services.main import AppService, AppCRUD
from ..models.pkce import PKCEState
from ..utils.service_result import ServiceResult

class PKCECRUD(AppCRUD):
    def create_item(self, item: PKCEItemCreate) -> PKCEState:
        pkce_item = PKCEState(state=item.state, code_verifier=item.code_verifier)
        self.db.add(pkce_item)
        self.db.commit()
        self.db.refresh(pkce_item)
        return pkce_item

    def get_item(self, state_str: str) -> PKCEState | None:
        pkce_item = self.db.query(PKCEState).filter(PKCEState.state == state_str).first()
        if pkce_item:
            return pkce_item
        return None

class PKCEService(AppService):
    def create_item(self, item: PKCEItemCreate) -> ServiceResult:
        pkce_item = PKCECRUD(self.db).create_item(item)
        if not pkce_item:
            return ServiceResult(AppException.PKCECreateItem())
        return ServiceResult(pkce_item)

    def get_item(self, item_id: str) -> ServiceResult:
        pkce_item = PKCECRUD(self.db).get_item(item_id)
        if not pkce_item:
            return ServiceResult(AppException.PKCEGetItem({"item_id": item_id}))
        return ServiceResult(pkce_item)


