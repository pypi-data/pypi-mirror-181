# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ckms.core import get_default_keychain
from ckms.core import Keychain
from ckms.core import KeySpecification
from ckms.jose import PayloadCodec
from ckms.utils import b64encode_str


class PersistenceSecurity:
    """Provides an interface to encrypt/decrypt the data persistence layer
    (data-at-rest).
    """
    __module__: str = 'cbra.ext.service'
    keychain: Keychain = get_default_keychain()

    @property
    def codec(self) -> PayloadCodec:
        return PayloadCodec(
            decrypter=self.keychain,
            encrypter=self.keychain,
            encryption_keys=['pii']
        )

    async def index(
        self,
        value: bytes | str,
        encoding: str = 'utf-8',
        key: KeySpecification | None = None
    ) -> str:
        """Create a secure index of `value`.
        
        If `value` is of type :class:`str`, use `encoding` as the character
        encoding when converting the string to bytes.
        """
        key = key or self.keychain.get('idx')
        if isinstance(value, str):
            value = str.encode(value, encoding=encoding)
        return b64encode_str(await key.sign(value))