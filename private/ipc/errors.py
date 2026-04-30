
from typing import Optional, Any, Dict
from web3.exceptions import ContractLogicError


class ContractError(Exception):
    """Named sentinel exception for on-chain contract errors.

    Instances are singletons defined at module level so callers can use
    ``isinstance(err, ContractError)`` or identity comparison (``err is
    ErrBucketNotFound``) instead of fragile string matching.
    """


# Named sentinel instances — one per contract error.
ErrBucketAlreadyExists = ContractError('BucketAlreadyExists')
ErrBucketInvalid = ContractError('BucketInvalid')
ErrBucketInvalidOwner = ContractError('BucketInvalidOwner')
ErrBucketNonexists = ContractError('BucketNonexists')
ErrBucketNonempty = ContractError('BucketNonempty')
ErrFileAlreadyExists = ContractError('FileAlreadyExists')
ErrFileInvalid = ContractError('FileInvalid')
ErrFileNonexists = ContractError('FileNonexists')
ErrFileNonempty = ContractError('FileNonempty')
ErrFileNameDuplicate = ContractError('FileNameDuplicate')
ErrFileFullyUploaded = ContractError('FileFullyUploaded')
ErrFileChunkDuplicate = ContractError('FileChunkDuplicate')
ErrBlockAlreadyExists = ContractError('BlockAlreadyExists')
ErrBlockInvalid = ContractError('BlockInvalid')
ErrBlockNonexists = ContractError('BlockNonexists')
ErrInvalidArrayLength = ContractError('InvalidArrayLength')
ErrInvalidFileBlocksCount = ContractError('InvalidFileBlocksCount')
ErrInvalidLastBlockSize = ContractError('InvalidLastBlockSize')
ErrInvalidEncodedSize = ContractError('InvalidEncodedSize')
ErrInvalidFileCID = ContractError('InvalidFileCID')
ErrIndexMismatch = ContractError('IndexMismatch')
ErrNoPolicy = ContractError('NoPolicy')
ErrFileNotFilled = ContractError('FileNotFilled')
ErrBlockAlreadyFilled = ContractError('BlockAlreadyFilled')
ErrChunkCIDMismatch = ContractError('ChunkCIDMismatch')
ErrNotBucketOwner = ContractError('NotBucketOwner')
ErrBucketNotFound = ContractError('BucketNotFound')
ErrFileDoesNotExist = ContractError('FileDoesNotExist')
ErrNotThePolicyOwner = ContractError('NotThePolicyOwner')
ErrCloneArgumentsTooLong = ContractError('CloneArgumentsTooLong')
ErrCreate2EmptyBytecode = ContractError('Create2EmptyBytecode')
ErrECDSAInvalidSignatureS = ContractError('ECDSAInvalidSignatureS')
ErrECDSAInvalidSignatureLength = ContractError('ECDSAInvalidSignatureLength')
ErrECDSAInvalidSignature = ContractError('ECDSAInvalidSignature')
ErrAlreadyWhitelisted = ContractError('AlreadyWhitelisted')
ErrInvalidAddress = ContractError('InvalidAddress')
ErrNotWhitelisted = ContractError('NotWhitelisted')
ErrMathOverflowedMulDiv = ContractError('MathOverflowedMulDiv')
ErrInvalidBlocksAmount = ContractError('InvalidBlocksAmount')
ErrInvalidBlockIndex = ContractError('InvalidBlockIndex')
ErrLastChunkDuplicate = ContractError('LastChunkDuplicate')
ErrFileNotExists = ContractError('FileNotExists')
ErrNotSignedByBucketOwner = ContractError('NotSignedByBucketOwner')
ErrNonceAlreadyUsed = ContractError('NonceAlreadyUsed')
ErrOffsetOutOfBounds = ContractError('OffsetOutOfBounds')

_error_map = {
    "0x497ef2c2": ErrBucketAlreadyExists,
    "0x4f4b202a": ErrBucketInvalid,
    "0xdc64d0ad": ErrBucketInvalidOwner,
    "0x938a92b7": ErrBucketNonexists,
    "0x89fddc00": ErrBucketNonempty,
    "0x6891dde0": ErrFileAlreadyExists,
    "0x77a3cbd8": ErrFileInvalid,
    "0x21584586": ErrFileNonexists,
    "0xc4a3b6f1": ErrFileNonempty,
    "0xd09ec7af": ErrFileNameDuplicate,
    "0xd96b03b1": ErrFileFullyUploaded,
    "0x702cf740": ErrFileChunkDuplicate,
    "0xc1edd16a": ErrBlockAlreadyExists,
    "0xcb20e88c": ErrBlockInvalid,
    "0x15123121": ErrBlockNonexists,
    "0x856b300d": ErrInvalidArrayLength,
    "0x17ec8370": ErrInvalidFileBlocksCount,
    "0x5660ebd2": ErrInvalidLastBlockSize,
    "0x1b6fdfeb": ErrInvalidEncodedSize,
    "0xfe33db92": ErrInvalidFileCID,
    "0x37c7f255": ErrIndexMismatch,
    "0xcefa6b05": ErrNoPolicy,
    "0x5c371e92": ErrFileNotFilled,
    "0xdad01942": ErrBlockAlreadyFilled,
    "0x4b6b8ec8": ErrChunkCIDMismatch,
    "0x0d6b18f0": ErrNotBucketOwner,
    "0xc4c1a0c5": ErrBucketNotFound,
    "0x3bcbb0de": ErrFileDoesNotExist,
    "0xa2c09fea": ErrNotThePolicyOwner,
    "0x94289054": ErrCloneArgumentsTooLong,
    "0x4ca249dc": ErrCreate2EmptyBytecode,
    "0xf3714a9b": ErrECDSAInvalidSignatureS,
    "0x367e2e27": ErrECDSAInvalidSignatureLength,
    "0xf645eedf": ErrECDSAInvalidSignature,
    "0xb73e95e1": ErrAlreadyWhitelisted,
    "0xe6c4247b": ErrInvalidAddress,
    "0x584a7938": ErrNotWhitelisted,
    "0x227bc153": ErrMathOverflowedMulDiv,
    "0xe7b199a6": ErrInvalidBlocksAmount,
    "0x59b452ef": ErrInvalidBlockIndex,
    "0x55cbc831": ErrLastChunkDuplicate,
    "0x2abde339": ErrFileNotExists,
    "0x48e0ed68": ErrNotSignedByBucketOwner,
    "0x923b8cbb": ErrNonceAlreadyUsed,
    "0x9605a010": ErrOffsetOutOfBounds,
}


def error_hash_to_error(error_data: Any) -> Exception:
    if hasattr(error_data, 'args') and error_data.args:
        error_str = str(error_data.args[0]) if error_data.args else str(error_data)
    else:
        error_str = str(error_data)
    hash_code = None
    if isinstance(error_str, str):
        import re
        hex_match = re.search(r'0x[a-fA-F0-9]{8}', error_str)
        if hex_match:
            hash_code = hex_match.group(0).lower()

    if hash_code and hash_code in _error_map:
        return _error_map[hash_code]
    return error_data if isinstance(error_data, Exception) else Exception(str(error_data))


def ignore_offset_error(error: Exception) -> Optional[Exception]:
    mapped_error = error_hash_to_error(error)
    if mapped_error and str(mapped_error) == "OffsetOutOfBounds":
        return None
    return error


def parse_errors_to_hashes() -> None:
    pass