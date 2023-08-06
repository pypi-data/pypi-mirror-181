from typing import List
from tests.main import Web3CliTest
from web3cli.core.models.contract import Contract
from web3cli.helpers.seed import seed_contracts
from web3cli.core.models.types import ContractFields


def test_contract_list(contracts: List[ContractFields]) -> None:
    """Add contracts and check that they are listed from oldest to newest"""
    contracts = sorted(contracts, key=lambda t: t["created_at"], reverse=True)
    with Web3CliTest() as app:
        seed_contracts(app, contracts)
        app.set_args(["db", "contract", "list"]).run()
        data, output = app.last_rendered
        for i in range(0, len(contracts)):
            assert data[i][0] == contracts[i]["hash"]
            assert data[i][1] == str(contracts[i]["chain"])


def test_contract_get(contracts: List[ContractFields]) -> None:
    for t in contracts:
        with Web3CliTest() as app:
            seed_contracts(app, contracts)
            app.set_args(
                [
                    "db",
                    "contract",
                    "get",
                    t["hash"],
                ]
            ).run()
            data, output = app.last_rendered
            assert t["hash"] in output
            assert str(t["gas"]) in output
            assert t["gas_price"] in output


def test_contract_add(contracts: List[ContractFields]) -> None:
    for t in contracts:
        with Web3CliTest() as app:
            app.set_args(
                [
                    "db",
                    "contract",
                    "add",
                    t["hash"],
                    t["from_"],
                    t["to"],
                ]
            ).run()
            contract = Contract.get_by_hash(t["hash"])
            assert contract.select().count() == 1
            assert Contract.from_ == t["from_"]
            assert Contract.to == t["to"]


def test_contract_update(contracts: List[ContractFields]) -> None:
    """Create contract 0, then update it with the data of contract 1,
    while keeping the same hash"""
    with Web3CliTest() as app:
        seed_contracts(app, [contracts[0]])
        app.set_args(
            argv=[
                "db",
                "contract",
                "add",
                contracts[0]["hash"],
                contracts[1]["from_"],
                contracts[1]["to"],
                "--update",
            ]
        ).run()
        contract = Contract.get_by_hash(contracts[0]["hash"])
        assert Contract.from_ == contracts[1]["from_"]
        assert Contract.to == contracts[1]["to"]


def test_contract_delete(contracts: List[ContractFields]) -> None:
    for t in contracts:
        with Web3CliTest() as app:
            seed_contracts(app, contracts)
            app.set_args(
                [
                    "db",
                    "contract",
                    "delete",
                    t["hash"],
                ]
            ).run()
            assert Contract.select().count() == len(contracts) - 1
