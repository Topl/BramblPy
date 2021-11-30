from brambl.types import RPCEndpoint


class RPC:
    # admin
    admin_unlockKeyfile = RPCEndpoint("admin_unlockKeyfile")
    admin_lockKeyfile = RPCEndpoint("admin_lockKeyfile")
    admin_generateKeyfile = RPCEndpoint("admin_generateKeyfile")
    admin_importSeedPhrase = RPCEndpoint("admin_importSeedPhrase")
    admin_listOpenKeyfiles = RPCEndpoint("admin_listOpenKeyfiles")
    admin_startForging = RPCEndpoint("admin_startForging")
    admin_stopForging = RPCEndpoint("admin_stopForging")
    admin_updateRewardsAddress = RPCEndpoint("admin_updateRewardsAddress")
    admin_getRewardsAddress = RPCEndpoint("admin_getRewardsAddress")

    # topl
    topl_head = RPCEndpoint("topl_head")
    topl_balances = RPCEndpoint("topl_balances"),
    topl_transactionById = RPCEndpoint("topl_transactionById")
    topl_blockById = RPCEndpoint("topl_blockById")
    topl_blockByHeight = RPCEndpoint("topl_blockByHeight")
    topl_mempool = RPCEndpoint("topl_mempool")
    topl_transactionFromMempool = RPCEndpoint("topl_transactionFromMempool")
    topl_info = RPCEndpoint("topl_info")
    topl_rawAssetTransfer = RPCEndpoint("topl_rawAssetTransfer")
    topl_rawArbitTransfer = RPCEndpoint("topl_rawArbitTransfer")
    topl_rawPolyTransfer = RPCEndpoint("topl_rawPolyTransfer")
    topl_broadcastTx = RPCEndpoint("topl_broadcastTx")

    #util
    util_seed = RPCEndpoint("util_seed")
    util_seedOfLength = RPCEndpoint("util_seedOfLength")
    util_hashBlake2b256 = RPCEndpoint("util_hashBlake2b256")
    util_generateAssetCode = RPCEndpoint("util_generateAssetCode")
    util_checkValidAddress = RPCEndpoint("util_checkValidAddress")

    #debug
    debug_delay = RPCEndpoint("debug_delay")
    debug_myBlocks = RPCEndpoint("debug_myBlocks"),
    debug_generators = RPCEndpoint("debug_generators"),
    debug_idsFromHeight = RPCEndpoint("debug_idsFromHeight"),
