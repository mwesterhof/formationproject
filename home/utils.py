# TODO: investigate if it makes sense to just generate random key and iv
# this would invalidate a token open restart
from base64 import b64encode, b64decode
from collections.abc import Iterable
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from wagtail.core.blocks import ListBlock, StreamBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class TokenProcessor:
    def __init__(self):
        key = os.urandom(32)
        self.iv = os.urandom(16)
        self.cipher = Cipher(algorithms.AES(key), modes.CBC(self.iv))

    def generate_token(self, page_id, block_id):
        to_encrypt = bytes(f'{str(page_id).ljust(11)}:{block_id}', 'utf-8')
        encryptor = self.cipher.encryptor()
        return str(
            b64encode(encryptor.update(to_encrypt) + encryptor.finalize()),
            'utf-8'
        )

    def unpack_token(self, token_encoded):
        token = b64decode(token_encoded)
        decryptor = self.cipher.decryptor()
        decrypted = decryptor.update(token) + decryptor.finalize()
        page_id, block_id = str(decrypted, 'utf-8').split(':')
        page_id = int(page_id)
        return page_id, block_id


token_processor = TokenProcessor()


def _extract_formblocks_recursive(container, form_blocks):
    from home.blocks import FormBlock
    for element in container:
        if isinstance(element.block, FormBlock):
            element = getattr(element, 'value', element)
            form_blocks[element['block_id']] = element
        elif isinstance(element.block, ListBlock) or isinstance(element.block, StreamBlock):
            _extract_formblocks_recursive(element.value, form_blocks)


def find_block(page_id, block_id):
    page = Page.objects.get(pk=page_id).specific
    fields = [
        getattr(page, field.name)
        for field in page._meta.fields
        if isinstance(field, StreamField)
    ]
    form_blocks = {}

    for field in fields:
        _extract_formblocks_recursive(field, form_blocks)

    return form_blocks[block_id]
