from models.sql_models import Contract, User, Client
from typing import List, Optional
from datetime import date

class ContractController:
    def __init__(self, current_user: User, db):
        self.current_user = current_user
        self.db = db

    def get_all_contracts(self) -> List[Contract]:
        """Get all contracts with permission check"""
        if self.current_user.role.role not in ["manager", "sailor"]:
            raise PermissionError("Not enough permissions to view contracts")
        return self.db.query(Contract).all()

    def get_contract(self, contract_id: int) -> Optional[Contract]:
        """Get a specific contract with permission check"""
        if self.current_user.role.role not in ["manager", "sailor"]:
            raise PermissionError("Not enough permissions to view contract")
        return self.db.query(Contract).filter(Contract.id == contract_id).first()

    def create_contract(self, client_id: int, total_amount: int, 
                       outstanding_amount: int, status_contract: bool) -> Contract:
        """Create a new contract with validation and permission check"""
        if self.current_user.role.role not in ["manager", "sailor"]:
            raise PermissionError("Not enough permissions to create contract")
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
            client_id=client_id,
            total_amount=total_amount,
            outstanding_amount=outstanding_amount,
            creation_date=date.today(),
            status_contract=status_contract,
            user_id=self.current_user.id
        )

        self.db.add(contract)
        self.db.commit()
        self.db.refresh(contract)
        return contract

    def update_contract(self, contract_id: int, client_id: int = None, 
                       total_amount: int = None, outstanding_amount: int = None,
                       status_contract: bool = None) -> Optional[Contract]:
        """Update a contract with validation and permission check"""
        if self.current_user.role.role not in ["manager", "sailor"]:
            raise PermissionError("Not enough permissions to update contract")

        contract = self.get_contract(contract_id)
        if not contract:
            raise ValueError("contract not found")
        if client_id:
            client = self.db.query(Client).filter(Client.id == client_id).first()
            if not client:
                raise ValueError("client not found")
            contract.client_id = client_id
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