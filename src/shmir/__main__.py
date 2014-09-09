# import os
# import re
# import sys

# # Removing system-wide installed shmir from PYTHONPATH
# sys.path = [
#     directory for directory in sys.path
#     if not re.search(r'shmir', directory)
# ]
#
# # Treating local shmir as a module
# sys.path.insert(
#     0, os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# )

from shmir import run


if __name__ == '__main__':
    run()
