import logging
from typing import List

from empiric.core.contract import Contract
from empiric.core.entry import Entry
from empiric.core.types import AggregationMode
from empiric.core.utils import str_to_felt
from starknet_py.contract import InvokeResult
from starknet_py.net.client import Client

logger = logging.getLogger(__name__)


class OracleMixin:
    publisher_registry: Contract
    client: Client

    async def publish_spot_entry(
        self,
        pair_id: int,
        value: int,
        timestamp: int,
        source: int,
        publisher: int,
        volume: int = 0,
        max_fee: int = int(1e16),
    ) -> InvokeResult:
        if not self.is_user_client:
            raise AttributeError(
                "Must set account.  You may do this by invoking self._setup_account_client(private_key, account_contract_address)"
            )
        invocation = await self.oracle.publish_spot_entry.invoke(
            {
                "pair_id": pair_id,
                "value": value,
                "timestamp": timestamp,
                "source": source,
                "publisher": publisher,
            },
            max_fee=max_fee,
        )
        return invocation

    async def publish_many(
        self, entries: List[Entry], pagination=0, max_fee=int(1e18)
    ) -> List[InvokeResult]:
        if len(entries) == 0:
            logger.warn("Skipping publishing as entries array is empty")
            return

        invocations = []
        # TODO (this PR) filter by entry.type and publish Spot, Future and Generic entries separately
        if pagination:
            ix = 0
            while ix < len(entries):
                invocation = await self.oracle.publish_spot_entries.invoke(
                    Entry.serialize_entries(entries[ix : ix + pagination]),
                    callback=self.track_nonce,
                    max_fee=max_fee,
                )
                logger.info(str(invocation))
                ix += pagination
                invocations.append(invocation)
        else:
            invocation = await self.oracle.publish_spot_entries.invoke(
                Entry.serialize_entries(entries), max_fee=max_fee
            )
            invocations.append(invocation)
            logger.info(str(invocation))

        logger.info(
            f"Sent {len(entries)} updated entries with transaction {invocation.hash}"
        )

        return invocations

    async def get_entries(self, pair_id, sources=[]) -> List[Entry]:
        if isinstance(pair_id, str):
            pair_id = str_to_felt(pair_id)
        elif not isinstance(pair_id, int):
            raise TypeError(
                "Pair ID must be string (will be converted to felt) or integer"
            )
        response = await self.oracle.get_entries.call(pair_id, sources)

        return [Entry.from_dict(entry) for entry in response.entries]

    async def get_spot(
        self,
        pair_id,
        aggregation_mode: AggregationMode = AggregationMode.MEDIAN,
        sources=None,
    ) -> Entry:
        if isinstance(pair_id, str):
            pair_id = str_to_felt(pair_id)
        elif not isinstance(pair_id, int):
            raise TypeError(
                "Pair ID must be string (will be converted to felt) or integer"
            )
        if sources is None:
            response = await self.oracle.get_spot.call(
                pair_id,
                aggregation_mode.value,
            )
        else:
            response = await self.oracle.get_spot_entries_for_sources.call(
                pair_id, aggregation_mode.value, sources
            )

        return (
            response.price,
            response.decimals,
            response.last_updated_timestamp,
            response.num_sources_aggregated,
        )

    async def get_future(
        self,
        pair_id,
        expiry_timestamp,
        aggregation_mode: AggregationMode = AggregationMode.MEDIAN,
        # TODO Add sources on the oracle contract and then in the client here
        # sources=None,
    ) -> Entry:
        if isinstance(pair_id, str):
            pair_id = str_to_felt(pair_id)
        elif not isinstance(pair_id, int):
            raise TypeError(
                "Pair ID must be string (will be converted to felt) or integer"
            )

        response = await self.oracle.get_futures.call(
            pair_id,
            expiry_timestamp,
            aggregation_mode.value,
        )

        return (
            response.price,
            response.decimals,
            response.last_updated_timestamp,
            response.num_sources_aggregated,
        )

    async def set_checkpoint(
        self,
        pair_id: int,
        aggregation_mode: int = str_to_felt("MEDIAN"),
        max_fee=int(1e16),
    ) -> InvokeResult:
        if not self.is_user_client:
            raise AttributeError(
                "Must set account.  You may do this by invoking self._setup_account_client(private_key, account_contract_address)"
            )
        invocation = await self.oracle.set_checkpoint.invoke(
            pair_id,
            aggregation_mode,
            callback=self.track_nonce,
            max_fee=max_fee,
        )
        return invocation

    async def set_checkpoints(
        self,
        pair_ids: List[int],
        aggregation_mode: int = str_to_felt("MEDIAN"),
        max_fee=int(1e18),
    ) -> InvokeResult:
        if not self.is_user_client:
            raise AttributeError(
                "Must set account.  You may do this by invoking self._setup_account_client(private_key, account_contract_address)"
            )
        invocation = await self.oracle.set_checkpoints.invoke(
            pair_ids,
            aggregation_mode,
            callback=self.track_nonce,
            max_fee=max_fee,
        )
        return invocation
