```python
import logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(%(asctime)s %(name)-12s %(levelname)-8s %(message)s)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLever(logging.DEBUG)

logger.debug('debug log')

###############################

import logging

formatter = logging.Formatter(%(asctime)s %(name)-12s %(levelname)-8s %(message)s)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLever(logging.DEBUG)

logger.debug('debug log')



```

