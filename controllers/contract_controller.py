from models.sql_models import Contract, User, Client
from typing import List, Optional
from datetime import date
from permission import Permission

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
        if not Permission.can_create_contract(self.current_user):
            raise PermissionError("Permission refusée. Rôle requis: sailor")
            
        if not client_id:
            raise ValueError("client id is required")
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise ValueError("client not found")
        if total_amount <= 0:
            raise ValueError("amount must be greater than 0")
        if outstanding_amount < 0 or outstanding_amount > total_amount:
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

    def update_contract(self, contract_id: int, total_amount: int = None,
                       outstanding_amount: int = None, status_contract: bool = None) -> Optional[Contract]:
        """Update a contract with validation and permission check"""
        contract = self.get_contract(contract_id)
        if not contract:
            raise ValueError("Contract not found")

        if not Permission.can_update_contract(self.current_user, contract):
            raise PermissionError("Permission refusée. Vous ne pouvez modifier que les contrats de vos clients.")
            
        if total_amount is not None:
            if total_amount <= 0:
                raise ValueError("amount must be greater than 0")
            contract.total_amount = total_amount

        if outstanding_amount is not None:
            if outstanding_amount < 0 or outstanding_amount > contract.total_amount:
                raise ValueError("amount must be between 0 and total amount")
            contract.outstanding_amount = outstanding_amount

        if status_contract is not None:
            contract.status_contract = status_contract

        self.db.commit()
        self.db.refresh(contract)
        return contract

    def __del__(self):
        """Close database session when controller is destroyed"""
        self.db.close() 
