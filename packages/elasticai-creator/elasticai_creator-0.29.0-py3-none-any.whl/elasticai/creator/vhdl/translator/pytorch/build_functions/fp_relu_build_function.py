from elasticai.creator.nn.relu import FixedPointReLU
from elasticai.creator.vhdl.translator.abstract.layers.fp_relu_module import (
    FPReLUModule,
)


def build_fp_relu(fp_relu: FixedPointReLU, layer_id: str) -> FPReLUModule:
    return FPReLUModule(
        layer_id=layer_id,
    )
