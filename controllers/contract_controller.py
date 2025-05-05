from models.sql_models import Contract, User, Client
from typing import List, Optional
from datetime import date
from permission import Permission
import sentry_sdk

class ContractController:
    def __init__(self, current_user: User, db):
        self.current_user = current_user
        self.db = db

    def get_all_contracts(self) -> List[Contract]:
        """Get all contracts"""
        return self.db.query(Contract).all()

    def get_contract(self, contract_id: int) -> Optional[Contract]:
        """Get a specific contract by ID"""
        return self.db.query(Contract).filter(Contract.id == contract_id).first()

    def get_contract_by_client_name(self, client_name: str) -> Optional[Contract]:
        """Get a contract by client name"""
        client = self.db.query(Client).filter(Client.name == client_name).first()
        if not client:
            return None
        return self.db.query(Contract).filter(Contract.client == client.id).first()

    def get_contract_by_client(self, client_id: int) -> Optional[Contract]:
        """Get a contract by client ID"""
        return self.db.query(Contract).filter(Contract.client == client_id).first()

    def create_contract(self, client_id: int, total_amount: int, 
                       outstanding_amount: int, status_contract: bool) -> Contract:
        """Create a new contract with validation and permission check"""
        try:
            if not Permission.can_create_contract(self.current_user):
                sentry_sdk.capture_message(f"Tentative de creation de contrat. Permission refusée par {self.current_user.username}. Rôle requis: sailor")
                raise PermissionError("Permission refusée. Rôle requis: sailor")
                
            if not client_id:
                sentry_sdk.capture_message(f"Tentative de création de contrat sans client_id par {self.current_user.username}. client id is required.")
                raise ValueError("client id is required")
            client = self.db.query(Client).filter(Client.id == client_id).first()
            if not client:
                sentry_sdk.capture_message(f"Client non trouvé pour la création de contrat: {client_id} par {self.current_user.username}")
                raise ValueError("client not found")
            if total_amount <= 0:
                sentry_sdk.capture_message(f"Montant total invalide: {total_amount} par {self.current_user.username}")
                raise ValueError("amount must be greater than 0")
            if outstanding_amount < 0 or outstanding_amount > total_amount:
                sentry_sdk.capture_message(f"Montant restant invalide: {outstanding_amount} par {self.current_user.username}")
                raise ValueError("amount must be between 0 and total amount")

            contract = Contract(
                client=client_id,
                total_amount=total_amount,
                outstanding_amount=outstanding_amount,
                creation_date=date.today(),
                status_contract=status_contract
            )

            self.db.add(contract)
            self.db.commit()
            self.db.refresh(contract)
            return contract
        except (ValueError, PermissionError) as e:
            sentry_sdk.capture_exception(e)
            raise

    def update_contract(self, contract_id: int, total_amount: int = None,
                       outstanding_amount: int = None, status_contract: bool = None) -> Optional[Contract]:
        """Update a contract with validation and permission check"""
        try:
            contract = self.get_contract(contract_id)
            if not contract:
                sentry_sdk.capture_message(f"Contrat non trouvé: {contract_id} par {self.current_user.username}")
                raise ValueError("Contract not found")

            if not Permission.can_update_contract(self.current_user, contract):
                sentry_sdk.capture_message(f"Tentative de modification de contrat sans permission par {self.current_user.username} Vous ne pouvez modifier que les contrats de vos clients.")
                raise PermissionError("Permission refusée. Vous ne pouvez modifier que les contrats de vos clients.")
                
            if total_amount is not None:
                if total_amount <= 0:
                    sentry_sdk.capture_message(f"Montant total invalide: {total_amount} par {self.current_user.username}")
                    raise ValueError("amount must be greater than 0")
                contract.total_amount = total_amount

            if outstanding_amount is not None:
                if outstanding_amount < 0 or outstanding_amount > contract.total_amount:
                    sentry_sdk.capture_message(f"Montant restant invalide: {outstanding_amount} par {self.current_user.username}")
                    raise ValueError("amount must be between 0 and total amount")
                contract.outstanding_amount = outstanding_amount

            if status_contract is not None:
                contract.status_contract = status_contract

            self.db.commit()
            self.db.refresh(contract)
            return contract
        except (ValueError, PermissionError) as e:
            sentry_sdk.capture_exception(e)
            raise

    def __del__(self):
        """Close database session when controller is destroyed"""
        self.db.close() 
