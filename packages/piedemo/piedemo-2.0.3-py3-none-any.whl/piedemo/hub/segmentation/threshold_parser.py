import numpy as np

from .parser import MaskParser
from typing import Dict, Tuple, Optional, List, Union


def mid_color(color_range):
    return (color_range[0].start + color_range[0].stop) // 2, (color_range[1].start + color_range[1].stop) // 2, (color_range[2].start + color_range[2].stop) // 2


def color_in_range(color, color_range):
    return all(color[i] in color_range[i] for i in range(3))


def color_in_color_ranges(color, color_ranges):
    return any(color_in_range(color, color_range) for color_range in color_ranges.keys())


def mask_color_ranged(mask, color_range):
    return np.all(np.bitwise_and(mask >= np.array([[[color_range[i].start for i in range(3)]]]), mask < np.array([[[color_range[i].stop for i in range(3)]]])), axis=-1)


class ThresholdMaskParser(MaskParser):
    def __init__(self,
                 colors_ranges_dict: Union[Dict[Tuple[range, range, range], int], List[Tuple[range, range, range]]],
                 classes: Dict[int, str],
                 other_colors_as_background=False,
                 background_idx=0):

        if isinstance(colors_ranges_dict, list):
            colors_ranges_dict = {color_range: idx for idx, color_range in enumerate(colors_ranges_dict)}
        self.colors_ranges_dict = colors_ranges_dict
        colors_dict = {mid_color(color_range): class_idx for color_range, class_idx in colors_ranges_dict.items()}
        super(ThresholdMaskParser, self).__init__(colors_dict=colors_dict,
                                                  classes=classes,
                                                  other_colors_as_background=other_colors_as_background,
                                                  background_idx=background_idx)

    def parse(self, mask,
              with_stats_per_class=False):
        """
        parse uint8 mask to (h, w), dtype=np.int32, range(0, num_classes-1)
        :param mask:
        :param with_stats_per_class:
        :return:
        """
        if not self.other_colors_as_background:
            colors = set(map(tuple, np.unique(mask.reshape((-1, 3)), axis=0).tolist()))
            for color in colors:
                assert color_in_color_ranges(color, self.colors_ranges_dict), f"color: {color}, colors: {set(self.colors_ranges_dict.keys())}"

        parsed_mask = np.zeros(mask.shape[:2], dtype=np.int32) + self.background_idx

        stats = [0 for _ in range(self.num_classes)] if with_stats_per_class else None
        for color_range, target_idx in self.colors_ranges_dict.items():
            color_mask = mask_color_ranged(mask, color_range)
            color_mask_int32 = color_mask.astype('int32') if with_stats_per_class else None

            if with_stats_per_class:
                stats[target_idx] = np.sum(color_mask_int32)

            parsed_mask[color_mask] = target_idx

        if with_stats_per_class:
            return parsed_mask, stats
        return parsed_mask

    def to_dict(self):
        colors_ranges_dict = {}
        for k, v in self.colors_ranges_dict.items():
            key = f"(({k[0].start}, {k[0].stop}), ({k[1].start}, {k[1].stop}), ({k[2].start}, {k[2].stop}))"
            colors_ranges_dict[key] = v
        return {
            "colors_ranges_dict": colors_ranges_dict,
            "classes": self.classes,
            "other_colors_as_background": self.other_colors_as_background,
            "background_idx": self.background_idx
        }
