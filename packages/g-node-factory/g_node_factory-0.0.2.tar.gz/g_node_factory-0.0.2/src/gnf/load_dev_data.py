from gnf.api_utils import dict_to_db
from gnf.enums import GNodeStatus


def main():
    gn = {
        "GNodeId": "7b1df82e-10c5-49d9-8d02-1e837e31b87e",
        "Alias": "d1",
        "StatusGtEnumSymbol": "153d3475",
        "RoleGtEnumSymbol": "00000000",
        "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
        "TypeName": "basegnode.gt",
        "Version": "020",
    }

    root = dict_to_db(gn)
    root.status_value = GNodeStatus.Active.value
    root.save()

    gn = {
        "GNodeId": "c0119953-a48f-495d-87cc-58fb92eb4cee",
        "Alias": "d1.isone",
        "StatusGtEnumSymbol": "153d3475",
        "RoleGtEnumSymbol": "86f21dd2",
        "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
        "TypeName": "basegnode.gt",
        "Version": "020",
    }

    isone = dict_to_db(gn)
    isone.status_value = GNodeStatus.Active.value
    isone.save()

    gn = {
        "GNodeId": "b572d571-22cf-4157-8c0f-33e9724d684f",
        "Alias": "d1.isone.ver",
        "StatusGtEnumSymbol": "153d3475",
        "RoleGtEnumSymbol": "4502e355",
        "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
        "TypeName": "basegnode.gt",
        "Version": "020",
    }

    versant = dict_to_db(gn)
    versant.status_value = GNodeStatus.Active.value
    versant.save()

    gn = {
        "GNodeId": "575f374f-8533-4733-baf7-91146c607445",
        "Alias": "d1.isone.ver.keene",
        "StatusGtEnumSymbol": "153d3475",
        "RoleGtEnumSymbol": "86f21dd2",
        "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
        "TypeName": "basegnode.gt",
        "Version": "020",
    }

    keene_rd = dict_to_db(gn)
    keene_rd.status_value = GNodeStatus.Active.value
    keene_rd.save()
