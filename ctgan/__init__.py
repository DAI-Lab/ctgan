# -*- coding: utf-8 -*-

"""Top-level package for ctgan."""

__author__ = 'MIT Data To AI Lab'
__email__ = 'dailabmit@gmail.com'
__version__ = '0.2.2.dev2'

from ctgan.demo import load_demo
from ctgan.synthesizer import CTGANSynthesizer
from ctgan.tvae import TVAESynthesizer
from ctgan.tablegan import TableganSynthesizer
from ctgan.tablegan_original import TableganSynthesizerOriginal

__all__ = (
    'CTGANSynthesizer',
    'TVAESynthesizer',
    'TableganSynthesizer',
    'TableganSynthesizerOriginal',
    'load_demo'
)
