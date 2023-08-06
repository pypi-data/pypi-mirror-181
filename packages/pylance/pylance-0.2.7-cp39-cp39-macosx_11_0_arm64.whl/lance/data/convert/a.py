#!/usr/bin/env python3

import lance
import os

d = lance.dataset(os.path.abspath("oxford_pet.lance"))
d.to_table()
