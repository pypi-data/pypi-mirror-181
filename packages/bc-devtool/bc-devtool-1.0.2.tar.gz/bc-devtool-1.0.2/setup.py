# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

import setuptools


def package_files(package_name, glob):
  package_path = Path(f'./{package_name}').resolve()
  return [str(path.relative_to(package_path)) for path in package_path.glob(glob)]


setuptools.setup(package_data={'bc_devtool': package_files('src/bc_devtool', 'locale/**/*.mo')})
