import sys
import os
from fido2.hid import CtapHidDevice
from fido2.client import Fido2Client
from fido2.server import Fido2Server
from fido2.webauthn import (
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
)
from utils.logger import logger
import base64

class FidoManager:
    """Handles FIDO2 / WebAuthn hardware key operations."""
    
    RP_ID = "shellixa.local"
    RP_NAME = "Shellixa SSH"
    
    def __init__(self):
        self.rp = PublicKeyCredentialRpEntity(id=self.RP_ID, name=self.RP_NAME)
        self.server = Fido2Server(self.rp)

    def find_device(self):
        """Find the first available FIDO2 HID device."""
        for dev in CtapHidDevice.list_devices():
            return dev
        return None

    def register(self, user_id, user_name):
        """Perform FIDO2 registration (Make Credential)."""
        device = self.find_device()
        if not device:
            raise Exception("No FIDO2 device found.")

        client = Fido2Client(device, f"https://{self.RP_ID}")
        
        user = PublicKeyCredentialUserEntity(
            id=user_id.encode(),
            name=user_name,
            display_name=user_name
        )

        # Registration options
        options, state = self.server.register_begin(
            user,
            authenticator_selection=AuthenticatorSelectionCriteria(
                user_verification=UserVerificationRequirement.DISCOURAGED
            )
        )

        try:
            logger.info("Touch your security key to register...")
            result = client.make_credential(options["publicKey"])
            auth_data = self.server.register_complete(state, result)
            
            # Extract credential ID and public key for storage
            credential_id = auth_data.credential_data.credential_id
            public_key = auth_data.credential_data.public_key
            
            return {
                "credential_id": base64.b64encode(credential_id).decode(),
                "public_key": base64.b64encode(public_key).decode()
            }
        except Exception as e:
            logger.error(f"FIDO2 Registration failed: {e}")
            raise e

    def authenticate(self, credential_id_base64):
        """Perform FIDO2 authentication (Get Assertion)."""
        device = self.find_device()
        if not device:
            raise Exception("No FIDO2 device found.")

        client = Fido2Client(device, f"https://{self.RP_ID}")
        credential_id = base64.b64decode(credential_id_base64.encode())

        # Authentication options
        options, state = self.server.authenticate_begin(
            allow_credentials=[{"type": "public-key", "id": credential_id}]
        )

        try:
            logger.info("Touch your security key to authenticate...")
            result = client.get_assertion(options["publicKey"])
            # Verify assertion (though locally we mostly care if it passed)
            self.server.authenticate_complete(
                state,
                credential_id,
                result.get_assertions()[0]
            )
            return True
        except Exception as e:
            logger.error(f"FIDO2 Authentication failed: {e}")
            return False
