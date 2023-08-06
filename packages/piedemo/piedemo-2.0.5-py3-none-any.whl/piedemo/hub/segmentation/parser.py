import json
import random
from itertools import product
from copy import deepcopy

import cv2
from munch import Munch
import torch
from functools import reduce
import numpy as np
from skimage.io import imread, imsave
from typing import Dict, Tuple, Optional, List, Union
from itertools import permutations


class MaskParser(object):
    """
    class for mask process
    """
    def __init__(self,
                 colors_dict: Union[Dict[Tuple[int, int, int], int], List[Tuple[int, int, int]]],
                 classes: Dict[int, str],
                 other_colors_as_background=False,
                 other_colors_as_nearest=False,
                 background_idx=0):
        super(MaskParser, self).__init__()
        if isinstance(colors_dict, list):
            colors_dict = {color: idx for idx, color in enumerate(colors_dict)}

        self.classes_idx = set(colors_dict.values())
        self.classes = classes
        self.classes2idx: Dict[str, int] = {class_name: idx for idx, class_name in classes.items()}
        self.num_classes = len(self.classes_idx)

        if not set(self.classes_idx) == set(range(self.num_classes)) == set(self.classes.keys()):
            raise ValueError((self.num_classes, self.classes_idx, self.classes))

        self.colors_dict: Dict[Tuple[int, int, int], int] = colors_dict
        self.other_colors_as_background = other_colors_as_background
        self.other_colors_as_nearest = other_colors_as_nearest
        self.background_idx = background_idx
        self.background_color = [c for c, i in self.colors_dict.items() if i == background_idx][0]

    def parse_path(self, mask_path: str):
        """
        reads and parse mask
        :param mask_path:
        :return:
        """
        try:
            mask = cv2.cvtColor(cv2.imread(str(mask_path),
                                           cv2.IMREAD_UNCHANGED),
                                cv2.COLOR_BGR2RGB)
        except Exception as e:
            raise RuntimeError(f"Can't parse {mask_path}")
        return self.parse(mask)

    def compose_path(self, mask: np.ndarray, mask_path: str):
        """

        :param mask: np.int32
        :param mask_path: path
        :return:
        """
        image = self.compose_color(mask)
        imsave(mask_path, image)

    def compose_color(self, mask):
        """
        from mask classes to colors
        :param mask: np.int32
        :return:
        """
        assert np.all(mask <= self.num_classes - 1) and np.all(mask >= 0)
        image = np.zeros(mask.shape + (3, ), dtype=np.uint8)
        for color, class_idx in self.colors_dict.items():
            image[mask == class_idx] = np.array(color)
        return image

    def compose_color_torch(self, mask, drange=(-1, 1)):
        """
        from mask classes to colors
        :param mask: np.int32
        :return:
        """
        return reduce(lambda x, y: x + y,
                      [(mask == class_idx).float().unsqueeze(1) * torch.from_numpy((drange[1] - drange[0]) * np.array(color, dtype=np.float32).reshape((1, 3, 1, 1)) / 255 + drange[0]).to(mask.device)
                       for color, class_idx in self.colors_dict.items()])

    def compose_color_softmax(self, mask):
        """
        soft color approximation on classes edges
        :param mask: (num_classes, h, w) np.float32 (after softmax)
        :return:
        """
        image = np.zeros(mask.shape + (3, ), dtype=np.uint8)
        image = sum([(mask[class_idx, ..., None] * np.array([[[color]]])).astype(np.uint8) for color, class_idx in self.colors_dict.items()], image)
        return image

    def parse(self, mask,
              with_stats_per_class=False):
        """
        parse uint8 mask to (h, w), dtype=np.int32, range(0, num_classes-1)
        :param mask:
        :param with_stats_per_class:
        :return:
        """
        colors_dict = deepcopy(self.colors_dict)
        colors_keys = list(self.colors_dict.keys())
        colors_keys.remove(self.background_color)
        colors_keys = [self.background_color] + colors_keys

        if self.other_colors_as_nearest or not self.other_colors_as_background:
            colors = set(map(tuple, np.unique(mask.reshape((-1, 3)), axis=0).tolist()))
            for color in colors:
                if not self.other_colors_as_nearest:
                    assert color in self.colors_dict, f"color: {color}, colors: {set(self.colors_dict.keys())}"
                else:
                    if color not in self.colors_dict:
                        dists = [abs(color[0] - c[0]) + abs(color[1] - c[1]) + abs(color[2] - c[2])
                                 for c in colors_keys]
                        min_idx = np.argmin(dists)
                        max_idx = np.argmax(dists)
                        if dists[min_idx] / dists[max_idx] < 0.2:
                            colors_dict[color] = self.colors_dict[colors_keys[min_idx]]
                        else:
                            colors_dict[color] = self.colors_dict[self.background_color]

        parsed_mask = np.zeros(mask.shape[:2], dtype=np.int32) + self.background_idx

        stats = [0 for _ in range(self.num_classes)] if with_stats_per_class else None
        for color, target_idx in colors_dict.items():
            color_mask = np.all(mask == np.array([[color]]), axis=-1)
            color_mask_int32 = color_mask.astype('int32') if with_stats_per_class else None

            if with_stats_per_class:
                stats[target_idx] += np.sum(color_mask_int32)

            parsed_mask[color_mask] = target_idx

        if with_stats_per_class:
            return parsed_mask, stats
        return parsed_mask

    def threshold_mask(self,
                       mask,
                       background_classes_idx: Optional[List] = None,
                       foreground_classes_idx: Optional[List] = None):
        """
        treat some classes as foreground, some - as background
        :param mask:
        :param background_classes_idx:
        :param foreground_classes_idx:
        :return: [0, 1] np.ndarray
        """
        assert background_classes_idx is not None or foreground_classes_idx is not None

        output_mask = np.zeros(mask.shape, dtype=np.int32)
        if background_classes_idx is not None and foreground_classes_idx is None:
            foreground_classes_idx = [i for i in range(self.num_classes) if i not in background_classes_idx]
        if foreground_classes_idx is not None:
            output_mask = sum([(mask == class_idx).astype(np.int32) for class_idx in foreground_classes_idx], output_mask)
        return output_mask

    def threshold_mask_by_class(self, mask,
                                background_classes = None,
                                foreground_classes = None):
        return self.threshold_mask(mask,
                                   [self.classes2idx[class_name] for class_name in background_classes] if background_classes is not None else None,
                                   [self.classes2idx[class_name] for class_name in foreground_classes] if foreground_classes is not None else None)

    def show_image_with_mask(self,
                             image, *masks,
                             title: Optional[str] = None):
        """
        shows image with mask
        :param image: np.uint8, rgb
        :param mask: np.int32, range(0, num_classes- 1)
        :param title:
        :return:
        """
        import matplotlib.pyplot as plt

        if title is not None:
            plt.title(title)

        image = np.array(image)
        colored_masks = [self.compose_color(mask) for mask in masks]
        to_show = np.concatenate([np.concatenate([image,
                                                  (0.8 * image + 0.2 * colored_mask).astype('uint8'),
                                                  colored_mask],
                                                 axis=1)
                                  for colored_mask in colored_masks],
                                 axis=0)
        plt.imshow(to_show)
        plt.show()

    @staticmethod
    def bounding_box(mask,
                     class_idxs: List[int],
                     squared: bool = False,
                     format: str = 'xyhw'):
        assert format in ['xyhw', 'xyxy']
        mask_points = cv2.findNonZero(sum([255 * np.uint8(mask == class_idx) for class_idx in class_idxs],
                                          np.zeros(mask.shape, dtype=np.uint8)))
        rect = cv2.boundingRect(mask_points)
        if rect[2] == 0 or rect[3] == 0:
            size = (mask.shape[1], mask.shape[0])
            if not squared or size[0] == size[1]:
                return [0, 0, size[0], size[1]]
            pad = np.random.randint(0, 1 + abs(size[1] - size[0]))
            if size[0] < size[1]:
                if format == 'xyxy':
                    return [pad, 0, pad + size[0], size[1]]
                else:
                    return [pad, 0, size[0], size[1]]
            else:
                if format == 'xyxy':
                    return [0, pad, size[0], pad + size[1]]
                else:
                    return [0, pad, size[0], size[1]]

        if squared:
            x1, y1, w, h = rect
            pad = np.abs(w - h)
            x1 -= pad // 2 if w < h else 0
            y1 -= pad // 2 if h < w else 0
            w += pad if w < h else 0
            h += pad if h < w else 0
            rect = (x1, y1, w, h)

        rect = list(rect)
        if rect[2] == 0:
            rect[0] = mask.shape[1] // 2

        if rect[3] == 0:
            rect[1] = mask.shape[0] // 2

        if format == 'xyxy':
            rect = (rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
        return rect

    def to_config(self, path):
        """
        dumps mask parser
        :param path:
        :return:
        """
        with open(path, 'w') as f:
            json.dump({
                'colors_dict': self.colors_dict,
                'loss_mask_list': self.loss_mask_list,
                'other_colors_as_background': self.other_colors_as_background,
                'background_idx': self.background_idx,
                'with_stats_per_class': self.with_stats_per_class,
            }, f)

    @staticmethod
    def from_config(path):
        """
        loads mask parser
        :param path:
        :return:
        """
        with open(path) as f:
            data = json.load(f)
        return MaskParser(**data)

    @staticmethod
    def produce_best_colors_dict(num_classes):
        """
        creates mapping from colour to class_idx
        :param num_classes:
        :return:
        """
        def gen(num):
            """
            generates 3-tuples
            :param num:
            :return:
            """
            k = 0
            p = 0
            while True:
                for i in range(k + 1):
                    for j in range(k - i + 1):
                        if p >= num:
                            return
                        yield i, j, k - i - j
                        p += 1
                k += 1

        return {(255 // 2 ** a[0], 255 // 2 ** a[1], 255 // 2 ** a[2]): i for i, a in enumerate(gen(num_classes))}

    @staticmethod
    def produce_best_colors_dict_v2(num_classes):
        def color_fn(i):
            if i == -1:
                return 0, 0, 0
            part_colors = [[255, 255, 255]] + list(set(permutations([255, 0, 0], 3))) + list(set(permutations([255, 255, 0], 3)))
            r, g, b = part_colors[i % len(part_colors)]
            return r // (2 ** (i // len(part_colors))), g // (2 ** (i // len(part_colors))), b // (2 ** (i // len(part_colors))),
        return {color_fn(i): i + 1 for i in range(-1, num_classes - 1)}

    @staticmethod
    def produce_random_colors_dict(num_classes: int):
        all_colors = list(product(range(256), range(256), range(256)))
        colors = [(0, 0, 0)] + random.sample(all_colors, k=num_classes - 1)
        return {colors[i]: i for i in range(num_classes)}

    @staticmethod
    # @numba.jit() TODO
    def binary_mask2coco_annotations(mask: np.ndarray,
                                     seg_mask: Optional[np.ndarray] = None,
                                     category_id: int = 0,
                                     bbox_padding: float = .1,
                                     split_by_connected_components: bool = False,
                                     choose_single_component_by_max_area: bool = False,
                                     filter_components_by_min_area: float = 1e-4) -> List[Munch]:
        """

        :param choose_single_component_by_max_area:
        :param filter_components_by_min_area:
        :param mask: in np.int [0...1]
        :param seg_mask in np.int [0...1]
        :param category_id: id int
        :param bbox_padding pad bboxes
        :param split_by_connected_components
        :return:
        """
        import detectron2
        from detectron2.structures import BoxMode
        from pycocotools import mask as cocomasktools

        annotations = []
        if split_by_connected_components:

            contours, hierarchy = cv2.findContours(np.uint8(255 * mask), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            if len(contours) == 0:
                return []

            if choose_single_component_by_max_area:
                contours = [max(contours, key=lambda x: cv2.contourArea(x))]

            contours = list(filter(lambda x: cv2.contourArea(x) > filter_components_by_min_area, contours))

            for c in contours:
                c = np.squeeze(c, axis=1)
                bbox = np.concatenate([np.min(c, axis=0), np.max(c, axis=0)])
                size = bbox[2:] - bbox[:2]
                bbox[:2] -= (bbox_padding * size).astype(bbox.dtype)
                bbox[2:] += (bbox_padding * size).astype(bbox.dtype)
                bbox[:2] = np.maximum(bbox[:2], np.zeros_like(bbox[:2]))
                bbox[2:] = np.minimum(bbox[2:], np.array([mask.shape[1], mask.shape[0]]))
                if seg_mask is not None:
                    c_seg_mask = np.zeros_like(seg_mask)
                    c_seg_mask[bbox[1]: bbox[3], bbox[0]: bbox[2]] = seg_mask[bbox[1]: bbox[3], bbox[0]: bbox[2]]
                    segmentation = cocomasktools.encode(np.asfortranarray(c_seg_mask))
                    segmentation['counts'] = segmentation['counts'].decode("utf-8")
                else:
                    segmentation = None

                annotation = Munch(bbox=bbox.tolist(),
                                   bbox_mode=BoxMode.XYXY_ABS,
                                   category_id=category_id)
                if segmentation is not None:
                    annotation.segmentation = segmentation
                annotations.append(annotation)
        else:
            y, x = np.where(mask)
            if len(x) == 0:
                return []
            c = np.stack([x, y], axis=-1)
            bbox = np.concatenate([np.min(c, axis=0), np.max(c, axis=0)])
            size = bbox[2:] - bbox[:2]
            bbox[:2] -= (bbox_padding * size).astype(bbox.dtype)
            bbox[2:] += (bbox_padding * size).astype(bbox.dtype)
            bbox[:2] = np.maximum(bbox[:2], np.zeros_like(bbox[:2]))
            bbox[2:] = np.minimum(bbox[2:], np.array([mask.shape[1], mask.shape[0]]))
            if seg_mask is not None:
                c_seg_mask = np.zeros_like(seg_mask)
                c_seg_mask[bbox[1]: bbox[3], bbox[0]: bbox[2]] = seg_mask[bbox[1]: bbox[3], bbox[0]: bbox[2]]
                segmentation = cocomasktools.encode(np.asfortranarray(c_seg_mask))
                segmentation['counts'] = segmentation['counts'].decode("utf-8")
            else:
                segmentation = None
            annotation = Munch(bbox=bbox.tolist(),
                               bbox_mode=BoxMode.XYXY_ABS,
                               category_id=category_id)
            if segmentation is not None:
                annotation.segmentation = segmentation
            annotations.append(annotation)

        return annotations

    @staticmethod
    def mask2coco_annotations(mask: np.ndarray,
                              categories: List,
                              bbox_padding: float = .1,
                              split_by_connected_components: bool = False,
                              choose_single_component_by_max_area: bool = False,
                              filter_components_by_min_area: float = 1e-4) -> List[List[Munch]]:
        """

        :param mask: in np.int [0...num_classes - 1]
        :param categories: {'category_id': 0, 'box_ids': [0, 1], 'seg_ids': [0, 1, 2]}
        :param bbox_padding pad bboxes
        :param split_by_connected_components
        :param choose_single_component_by_max_area: choose single box by max area
        :param filter_components_by_min_area: filter boxes that has small area
        :return:
        """
        annotations = []
        for category in categories:
            category_binary_mask = reduce(lambda x, y: np.bitwise_or(x, y), [mask == i for i in category['box_ids']])
            if 'seg_ids' in category:
                category_seg_binary_mask = reduce(lambda x, y: np.bitwise_or(x, y), [mask == i for i in category['seg_ids']])
            else:
                category_seg_binary_mask = None

            category_annotations = MaskParser.binary_mask2coco_annotations(category_binary_mask,
                                                                           category_seg_binary_mask,
                                                                           category_id=category['category_id'],
                                                                           bbox_padding=bbox_padding,
                                                                           split_by_connected_components=split_by_connected_components,
                                                                           choose_single_component_by_max_area=choose_single_component_by_max_area,
                                                                           filter_components_by_min_area=filter_components_by_min_area)
            annotations.extend(category_annotations)
        return annotations

    def to_dict(self):
        colors_dict = {}
        for k, v in self.colors_dict.items():
            key = f"({k[0]}, {k[1]}, {k[2]})"
            colors_dict[key] = v

        return {
            "colors_dict": colors_dict,
            "classes": self.classes,
            "other_colors_as_background": self.other_colors_as_background,
            "other_colors_as_nearest": self.other_colors_as_nearest,
            "background_idx": self.background_idx
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def __repr__(self):
        return f"!!{self.__class__.__name__}\n" + self.to_json()

    @staticmethod
    def binary_mask2polygon(mask,
                            return_hulled_mask=False):
        """

        :param mask: [0, 1]
        :return:
        """
        mask = np.uint8(255 * mask)
        contours = cv2.findContours(mask,
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]
        hull = []
        for i in range(len(contours)):
            hull.append(cv2.convexHull(contours[i], False))

        mask = np.zeros(mask.shape, np.uint8)
        mask = cv2.drawContours(mask, hull, -1, 255, -1)
        if return_hulled_mask:
            return hull, np.int32(mask > 0)
        return hull
