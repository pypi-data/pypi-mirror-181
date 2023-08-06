from negate import Negator

negator = Negator(use_transformers=True)

ns = negator.negate_sentence("A small Python module that doesn't negate sentences.")

print(ns)

