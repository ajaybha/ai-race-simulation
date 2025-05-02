import re
import os
from yaml import SafeLoader

class EnvVarLoader(SafeLoader):
    """Custom YAML loader that replaces environment variables in the YAML file."""

    def __init__(self, stream):
        super().__init__(stream)

    def construct_scalar(self, node):
        value = super().construct_scalar(node)
        if isinstance(value, str):
            # Pattern to match ${VARIABLE_NAME}
            pattern = r'\$\{([^}^{]+)\}'
            matches = re.finditer(pattern, value)
            for match in matches:
                env_var = match.group(1)
                value = value.replace(f'${{{env_var}}}', os.environ.get(env_var, ''))
        return value