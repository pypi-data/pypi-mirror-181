import sys

import torch
from qat.hard_sigmoid import FixedPointHardSigmoid
from qat.relu import FixedPointReLU

from elasticai.creator.vhdl.modules.linear import FixedPointLinear
from elasticai.creator.vhdl.number_representations import FixedPoint, FixedPointFactory
from elasticai.creator.vhdl.translator.abstract.layers.fp_hard_sigmoid_module import (
    FPHardSigmoidTranslationArgs,
)
from elasticai.creator.vhdl.translator.abstract.layers.fp_linear_1d_module import (
    FPLinear1dTranslationArgs,
)
from elasticai.creator.vhdl.translator.abstract.layers.fp_relu_module import (
    FPReLUTranslationArgs,
)
from elasticai.creator.vhdl.translator.build_function_mapping import (
    BuildFunctionMapping,
)
from elasticai.creator.vhdl.translator.pytorch import translator
from elasticai.creator.vhdl.translator.pytorch.build_function_mappings import (
    DEFAULT_BUILD_FUNCTION_MAPPING,
)
from elasticai.creator.vhdl.translator.pytorch.build_functions.fp_hard_sigmoid_build_function import (
    build_fp_hard_sigmoid,
)
from elasticai.creator.vhdl.translator.pytorch.build_functions.fp_linear_1d_build_function import (
    build_fp_linear_1d,
)


class FixedPointModel(torch.nn.Module):
    def __init__(self, fixed_point_factory: FixedPointFactory) -> None:
        super().__init__()

        self.linear1 = FixedPointLinear(
            in_features=3,
            out_features=4,
            fixed_point_factory=fixed_point_factory,
        )
        self.linear2 = FixedPointLinear(
            in_features=4,
            out_features=1,
            fixed_point_factory=fixed_point_factory,
        )
        self.hard_sigmoid = FixedPointHardSigmoid(
            fixed_point_factory=fixed_point_factory
        )
        self.relu1 = FixedPointReLU(fixed_point_factory=fixed_point_factory)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.linear1(x)
        x = self.relu1(x)
        x = self.linear2(x)
        x = self.hard_sigmoid(x)
        return x


def get_custom_build_mapping() -> BuildFunctionMapping:
    return DEFAULT_BUILD_FUNCTION_MAPPING.join_with_dict(
        {
            "elasticai.creator.vhdl.modules.linear.FixedPointLinear": build_fp_linear_1d,
            "elasticai.creator.vhdl.modules.hard_sigmoid.FixedPointHardSigmoid": build_fp_hard_sigmoid,
        }
    )


def main() -> None:
    torch.manual_seed(22)  # make result reproducible

    if len(sys.argv) < 2:
        print("Please supply a build directory path as a program argument.")
        return
    build_path = sys.argv[1]

    fixed_point_factory = FixedPoint.get_factory(total_bits=8, frac_bits=4)

    model = FixedPointModel(fixed_point_factory)

    code_repr = translator.translate_model(
        model=model,
    )

    translator.save_code(code_repr=code_repr, path=build_path)


if __name__ == "__main__":
    main()
