from enum import Enum


class PresenterErrorCode(Enum):
    # Success, no error
    kNone = 0
    # parameter check error
    kInvalidParam = 1
    # Connect to presenter server error
    kConnection = 2
    # SSL certification error
    kSsl = 3
    # Encode/Decode message error
    kCodec = 4
    # The given channel name is not created in server
    kNoSuchChannel = 5
    # The given channel is opened by another process
    kChannelAlreadyOpened = 6
    # Presenter server return unknown error
    kServerReturnedUnknownError = 7
    # Alloc object error
    kBadAlloc = 8
    # App returned error
    kAppDefinedError = 9
    # Timeout
    kSocketTimeout = 10
    # Uncategorized error
    kOther = 11