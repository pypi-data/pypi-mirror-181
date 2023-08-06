from __future__ import annotations

from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage
from bitcoin.base58 import Base58Error
from Cryptodome.Random import get_random_bytes
from enum import Enum

# from aiotinyrpc.transports.socketmessages import Message

# from dataclasses import dataclass

from aiotinyrpc.transports.socketmessages import (
    ChallengeMessage,
    ChallengeReplyMessage,
    AuthReplyMessage,
)


class AuthProvider:
    """All auth providers inherit from this"""

    def auth_message(self):
        raise NotImplementedError

    def verify_auth_message(self):
        raise NotImplementedError


class SignatureAuthProvider(AuthProvider):
    def __init__(self, key: str | None = None, address: str | None = None):
        self.key = key
        self.address = address

        self.to_sign = None

    def auth_message(self, msg):
        """Creates a message (non serialized) to be sent to the authenticator.
        In this case the message is a Bitcoin signed message"""
        # this happens if someone passes in bad key data. Upper layer can
        # catch ValueError
        try:
            secret = CBitcoinSecret(self.key)
        except Base58Error:
            raise ValueError

        message = BitcoinMessage(msg)
        return ChallengeReplyMessage(SignMessage(secret, message))

    def verify_auth(self, auth_msg: ChallengeReplyMessage):
        sig = auth_msg.signature
        msg = BitcoinMessage(self.to_sign)
        self.auth_state = VerifyMessage(self.address, msg, sig)
        return self.auth_state

    def challenge_message(self):
        if not self.address:
            raise ValueError("Address must be provided")

        self.to_sign = get_random_bytes(16).hex()
        return ChallengeMessage(self.to_sign, self.address)

    def auth_reply_message(self):
        return AuthReplyMessage(self.auth_state)
