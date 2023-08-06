import json
from parse import parse
from .parser import MaskParser
from .threshold_parser import ThresholdMaskParser


def load_from_file(mask_parser_path: str) -> MaskParser:
    with open(mask_parser_path) as f:
        content = f.read()

    assert content.startswith("!!")
    content = content.split('\n')
    json_content = '\n'.join(content[1:])
    cls_name = content[0][2:]
    kwargs = json.loads(json_content)
    if "colors_dict" in kwargs:
        colors_dict = kwargs['colors_dict']
        for k in list(colors_dict.keys()):
            r, g, b = parse("({},{},{})", k).fixed
            colors_dict[(int(r), int(g), int(b))] = colors_dict.pop(k)
    if "classes" in kwargs:
        classes = kwargs['classes']
        for k in list(classes.keys()):
            classes[int(k)] = classes.pop(k)

    if "colors_ranges_dict" in kwargs:
        colors_ranges_dict = kwargs['colors_ranges_dict']
        for k in list(colors_ranges_dict.keys()):
            r, g, b = parse("({},{},{})", k).fixed

            r_parsed = parse("({}, {})", r)
            if r_parsed is not None:
                r = range(*r_parsed.fixed)
            else:
                r = range(int(r))

            g_parsed = parse("({}, {})", g)
            if g_parsed is not None:
                g = range(*g_parsed.fixed)
            else:
                g = range(int(g))

            b_parsed = parse("({}, {})", b)
            if b_parsed is not None:
                b = range(*b_parsed.fixed)
            else:
                b = range(int(b))

            colors_ranges_dict[(r, g, b)] = colors_ranges_dict.pop(k)

    return globals()[cls_name](**kwargs)


def save_to_file(mask_parser,
                 mask_parser_path: str):
    with open(mask_parser_path, 'w') as f:
        f.write(f"!!{mask_parser.__class__.__name__}\n" + mask_parser.to_json())
