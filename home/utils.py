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


def extract_elements_recursive(container, results, check_method, id_based=False):
    for element in container:
        if check_method(element):
            element = getattr(element, 'value', element)
            if id_based:
                results[element['block_id']] = element
            else:
                results.append(element)
        elif isinstance(element.block, ListBlock) or isinstance(element.block, StreamBlock):
            extract_elements_recursive(element.value, results, check_method, id_based)


def find_block_value(page_id, block_id):
    page = Page.objects.get(pk=page_id).specific
    fields = [
        getattr(page, field.name)
        for field in page._meta.fields
        if isinstance(field, StreamField)
    ]
    form_blocks = {}

    def _formblock_check(element):
        from home.blocks import FormBlock
        return isinstance(element.block, FormBlock)

    for field in fields:
        extract_elements_recursive(field, form_blocks, _formblock_check, True)

    return form_blocks[block_id]
