
from typing import Optional, Any, Dict
from web3.exceptions import ContractLogicError


class IPCContractError(Exception):
    """Base class for IPC contract errors, enabling isinstance() checks."""
    pass


# Named sentinel constants — one per canonical contract error.
# Callers can use identity comparison: ``err is ErrBucketNotFound``
# or isinstance check: ``isinstance(err, IPCContractError)``.
ErrBucketAlreadyExists = IPCContractError('BucketAlreadyExists')
ErrBucketInvalid = IPCContractError('BucketInvalid')
ErrBucketInvalidOwner = IPCContractError('BucketInvalidOwner')
ErrBucketNonexists = IPCContractError('BucketNonexists')
ErrBucketNonempty = IPCContractError('BucketNonempty')
ErrFileAlreadyExists = IPCContractError('FileAlreadyExists')
ErrFileInvalid = IPCContractError('FileInvalid')
ErrFileNonexists = IPCContractError('FileNonexists')
ErrFileNonempty = IPCContractError('FileNonempty')
ErrFileNameDuplicate = IPCContractError('FileNameDuplicate')
ErrFileFullyUploaded = IPCContractError('FileFullyUploaded')
ErrFileChunkDuplicate = IPCContractError('FileChunkDuplicate')
ErrBlockAlreadyExists = IPCContractError('BlockAlreadyExists')
ErrBlockInvalid = IPCContractError('BlockInvalid')
ErrBlockNonexists = IPCContractError('BlockNonexists')
ErrInvalidArrayLength = IPCContractError('InvalidArrayLength')
ErrInvalidFileBlocksCount = IPCContractError('InvalidFileBlocksCount')
ErrInvalidLastBlockSize = IPCContractError('InvalidLastBlockSize')
ErrInvalidEncodedSize = IPCContractError('InvalidEncodedSize')
ErrInvalidFileCID = IPCContractError('InvalidFileCID')
ErrIndexMismatch = IPCContractError('IndexMismatch')
ErrNoPolicy = IPCContractError('NoPolicy')
ErrFileNotFilled = IPCContractError('FileNotFilled')
ErrBlockAlreadyFilled = IPCContractError('BlockAlreadyFilled')
ErrChunkCIDMismatch = IPCContractError('ChunkCIDMismatch')
ErrNotBucketOwner = IPCContractError('NotBucketOwner')
ErrBucketNotFound = IPCContractError('BucketNotFound')
ErrFileDoesNotExist = IPCContractError('FileDoesNotExist')
ErrNotThePolicyOwner = IPCContractError('NotThePolicyOwner')
ErrCloneArgumentsTooLong = IPCContractError('CloneArgumentsTooLong')
ErrCreate2EmptyBytecode = IPCContractError('Create2EmptyBytecode')
ErrECDSAInvalidSignatureS = IPCContractError('ECDSAInvalidSignatureS')
ErrECDSAInvalidSignatureLength = IPCContractError('ECDSAInvalidSignatureLength')
ErrECDSAInvalidSignature = IPCContractError('ECDSAInvalidSignature')
ErrAlreadyWhitelisted = IPCContractError('AlreadyWhitelisted')
ErrInvalidAddress = IPCContractError('InvalidAddress')
ErrNotWhitelisted = IPCContractError('NotWhitelisted')
ErrMathOverflowedMulDiv = IPCContractError('MathOverflowedMulDiv')
ErrInvalidBlocksAmount = IPCContractError('InvalidBlocksAmount')
ErrInvalidBlockIndex = IPCContractError('InvalidBlockIndex')
ErrLastChunkDuplicate = IPCContractError('LastChunkDuplicate')
ErrFileNotExists = IPCContractError('FileNotExists')
ErrNotSignedByBucketOwner = IPCContractError('NotSignedByBucketOwner')
ErrNonceAlreadyUsed = IPCContractError('NonceAlreadyUsed')
ErrOffsetOutOfBounds = IPCContractError('OffsetOutOfBounds')

# Map from 4-byte selector hex to pre-declared sentinel instance.
_error_map: Dict[str, IPCContractError] = {
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