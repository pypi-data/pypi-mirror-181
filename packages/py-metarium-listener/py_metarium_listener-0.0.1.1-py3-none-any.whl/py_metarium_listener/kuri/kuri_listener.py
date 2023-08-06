from ..base import BaseListener
from ..utils import KuriQuery


METARIUM_EXTRINSIC = "Metarium"
FUNCTION_CALL_SELF_REGISTER_CONTENT = "self_register_content"
FUNCTION_CALL_ADMIN_UPDATE_SCRIBE_STATUS = "force_update_scribe_authority_status"

class KuriListener(BaseListener):

    def __processed_block(self, block):
        processed_block = {
            "block_number": block["header"]["number"],
            "extrinsics": []
        }
        for extrinsic in block["extrinsics"]:
            extrinsic = extrinsic.serialize()
            if extrinsic["call"]["call_module"] == METARIUM_EXTRINSIC:
                log = {
                    "call_index": extrinsic["call"]["call_index"],
                    "call_function": extrinsic["call"]["call_function"],
                    "caller": extrinsic["address"]
                }
                if log["call_function"] == FUNCTION_CALL_SELF_REGISTER_CONTENT:
                    log["kuri"] = extrinsic["call"]["call_args"][0]["value"]
                if log["call_function"] == FUNCTION_CALL_ADMIN_UPDATE_SCRIBE_STATUS:
                    log["scribe"] = extrinsic["call"]["call_args"][0]["value"]
                
                processed_block["extrinsics"].append(log)
        
        return processed_block

    def __listen(self, direction, block_hash, block_count, query_params={}):
        query_params = query_params or {}
        query=KuriQuery()
        for field, value in query_params.items():
            query.parameters[field] = value

        # print(f"\n\nQUERY IS {query}\n\n")
        for block, is_metarium in super().listen(direction, block_hash, block_count):
            if not is_metarium:
                continue
            block = self.__processed_block(block)
            if len(query.parameters):
                extrinsics = block.pop("extrinsics")
                block["extrinsics"] = []
                for extrinsic in extrinsics:
                    for parameter in list(query.parameters):
                        if (parameter in extrinsic) and \
                            query.parameters[parameter] in ("*", extrinsic[parameter]):
                            block["extrinsics"].append(extrinsic)
                if not len(block["extrinsics"]):
                    continue

            yield block

    def listen(self, direction, block_hash=None, block_count=None, query_params={}):
        for block in self.__listen(direction, block_hash, block_count, query_params=query_params):
            yield block
